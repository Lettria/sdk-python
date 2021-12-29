import sys
import os
import json

import jsonlines as jsonl

from .client import Client
from .utils import flatten_lst, StrProperty, ListProperty, DictProperty, IntProperty
from .TextChunk import TextChunk
from .utils import GLOBAL, DOC, SENT, SUB, TOK
from .Document import Document
from .Sentence import Sentence
from .subtypes import Token, Subsentence

class PipelineError(Exception): pass
class RequestError(Exception): pass

class NLP(TextChunk):
    """ Class for data analysis of API return.
        Takes a Client class as input which is used to make api requests.
        Provides both high and low level methods to access data via specific class
        for each key in the api result or methods designed for specific use cases.
        """
    def __init__(self, api_key = None, client = None, data = None, no_print=False):
        super(NLP, self).__init__()
        self.client = None
        if client or api_key:
            self.add_client(client, api_key)
        self.documents = []
        self.max = len(self.documents)
        self.data = self.documents
        self.sentence_fields = [p for p in dir(Sentence) if isinstance(getattr(Sentence,p),property)]
        self.document_fields = [p for p in dir(Document) if isinstance(getattr(Document,p),property) and p.endswith('_doc')]
        self.fields = list(set(self.sentence_fields + self.document_fields))
        self._next_id = 0
        if 'token_flat' not in self.fields:
            self._generate_properties()

        def doNothing(*args):
            pass
        global print
        if no_print:
            print = doNothing

    @ListProperty
    def sentences(self):
        """ Direct access to all sentences """
        return flatten_lst([d.sentences for d in self.documents])

    @ListProperty
    def subsentences(self):
        """ Direct access to all subsentences """
        sentences = flatten_lst([d.sentences for d in self.documents])
        return flatten_lst([s.subsentences for s in sentences])

    @ListProperty
    def tokens(self):
        """ Direct access to all tokens """
        return flatten_lst([s.tokens for s in self.sentences])

    @property
    def nlp(self):
        return [self]

    def _generate_properties(self):
        """ Takes properties of the Sentence class and dynamically create properties for 
            NLP, Document and Subsentence class. """
        #add methods to NLP and Document classes
        for field in self.sentence_fields:
            for _class in [Document, NLP]:
                    if field in ['subsentences', 'tokens', 'sentences']:
                        continue
                    if not hasattr(_class, field):
                        setattr(_class, field, property(self._make_lambda(field)))
                    if not hasattr(_class, field + '_flat'):
                        setattr(_class, field + '_flat', property(self._make_lambda(field, True)))
            
            #add methods to Subsentence class
            filters = ['sentiment_target', 'morphology', 'ner', 'token', 'str', \
                            'lemma', 'lemma_detail', 'detail', 'pos', 'pos_detail', 'dep', 'language', 'meaning', \
                            'sentiment', 'sentiment_ml', 'emotion', 'emotion_ml', 'tokens']
            for _class in [Subsentence]:
                if field in filters:
                    if not hasattr(_class, field):
                        setattr(_class, field, getattr(Sentence, field))
                elif field not in ['subsentences']:
                    if not hasattr(_class, field):
                        setattr(_class, field, property(self._make_lambda_not_available(field)))

            #adding _flat  variants to sentence and subsentence methods for convenience
            for _class in [Sentence, Subsentence]: 
                if not hasattr(_class, field):
                    setattr(_class, field + '_flat', property(self._make_lambda_flat(field)))

        #add documents methods
        for field in self.document_fields:
            for _class in [NLP]:
                if not hasattr(_class, field):
                    setattr(_class, field, property(self._make_lambda(field)))
                if not hasattr(_class, field + '_flat'):
                    setattr(_class, field + '_flat', property(self._make_lambda(field, True)))

    def _make_lambda(self, field, flatten = False):
        """ Returns lambda functions to be added as property to classes """
        if not flatten:
            return lambda c_self : [getattr(s, field) for s in c_self.data]
        else:
            return lambda c_self : flatten_lst([getattr(s, field) for s in c_self.data])

    def _make_lambda_not_available(self, field):
        """ Returns lambda functions to be added as property to classes """
        return lambda x: field + ' not available for subsentences'

    def _make_lambda_flat(self, field):
        """ Returns lambda functions to be added as property to classes """
        return lambda c_self: flatten_lst(getattr(c_self, field))

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            self.n += 1
            return self.documents[self.n - 1]
        else:
            raise StopIteration

    def add_client(self, client = None, api_key = None):
        """ Add/Change the active Client by providing a Client Instance or an api_key
            Args:
                client: Client Instance
                api_key: string representing a valid api_key
        """
        if client and isinstance(client, Client):
            self.client = client
        elif api_key:
            self.client = Client(api_key)
        else:
            print('Please provide a client instance or an api_key.')

    def _missing_api_key():
        print('Failure : Please assign a client or api_key with add_client() in order to make a request. ')

    def _preprocess_document(self, document):
        if isinstance(document, str):
            if document.strip():
                document = document.strip()
                # document = [document] ## Temporary until option split_sentence is available
            else:
                return " "
        elif isinstance(document, list):
            document = [d.strip() for d in flatten_lst(document) if d.strip()]
            document = ' '.join(document) ## Temporary until option split_sentence is available
        else:
            print('document argument should be of type list or str.')
            raise TypeError
        return document

    def add_documents(self, documents, batch_size=32, skip_document=False, document_ids=[], verbose=True):
        """ Performs request to lettria API for multiples documents and stores it.
            This will increase speed by allowing batching to occur across different documents.
            Args:
                skip_document: If False document is added even if empty or request failed.
                batch_size: Number of documents to request at once.
                id: List of Ids given to documents, by default sequential integer """
        if not isinstance(documents, list):
            print("ERROR, 'add_documents' method expects a list of string as first argument.")
            return
        if document_ids:
            if not isinstance(document_ids, list) or len(document_ids) == 0 or len(document_ids) != len(documents):
                print("ERROR, 'document_ids' argument should be a list of string with the same length as the number of documents")
                return
        
        if not self.client:
            self._missing_api_key()
            return
        
        for idx_batch in range(0, len(documents), batch_size):
            batch_documents = documents[idx_batch:idx_batch + batch_size]
            batch_documents = [self._preprocess_document(doc) for doc in batch_documents]
            results = []
            if not batch_documents:
                print("ERROR, documents input is empty.")
                return 
            results, document_ids = self.request_batch_documents(batch_documents, document_ids = document_ids, skip_document=skip_document)
            for idx, (input_document, result) in enumerate(zip(batch_documents, results)):
                if idx_batch + idx < len(document_ids):
                    next_doc_id = document_ids[idx_batch + idx]
                else:
                    next_doc_id = self._next_id
                    self._next_id += 1
                if isinstance(result, list) and result:
                    self.documents.append(Document(result, _id=next_doc_id))
                    if verbose:
                        print("Added document " + str(self.documents[-1].id) + '.')
                else:
                    if not input_document:
                        self.documents.append(Document([], _id=next_doc_id))
                        if verbose:
                            print("Added empty document " + str(self.documents[-1].id) + ': received empty input.')
                    else:
                        self.documents.append(Document([], _id=next_doc_id))
                        if verbose:
                            print("Added empty document " + str(self.documents[-1].id) + ': processing failed.')
                self.max += 1

    def add_document(self, document, skip_document=False, _id=None, verbose=True):
        """ Performs request to lettria API for a document and stores it.
            Args:
                skip_document: If False document is added even if empty or request failed.
                id: Id given to document, by default sequential integer """
        if not self.client:
            self._missing_api_key()
            return
        results = None
        document = self._preprocess_document(document)
        
        if document:
            results = self.client.request_document(document, skip_document=skip_document, verbose=verbose)
        if results is None and skip_document == True:
            if not document:
                print("Skpping document, received empty input.")
            else:
                print("Skpping document, processing failed.")
        else:
            if _id == None:
                next_doc_id = self._next_id
                self._next_id += 1
            else:
                next_doc_id = _id
            if isinstance(results, dict):
                self.documents.append(Document(results, _id=next_doc_id))
                if verbose:
                    print("Added document " + str(self.documents[-1].id) + '.')
            else:
                if not document:
                    self.documents.append(Document([], _id=next_doc_id))
                    print("Added empty document " + str(self.documents[-1].id) + ': received empty input.')
                else:
                    self.documents.append(Document([], _id=next_doc_id))
                    print("Added empty document " + str(self.documents[-1].id) + ': processing failed.')
            self.max += 1

    def add_document_data(self, doc_data, _id=None):
        self.documents.append(Document(doc_data, _id))
        self.max += 1

    def _get_data(self):
        return [d._get_data() for d in self.documents]

    def save_result(self, *args):
        """ Alias for save_result"""
        self.save_results(*args)

    def save_results(self, filename = ''):
        """ Writes json result to a file with the specified name."""
        path_ok = 0
        c = 0
        if not self.data:
            print("No data to save.")
            return
        if not filename:
            filename = 'results'
            while not path_ok:
                path = filename + '_' + str(c) + '.jsonl'
                if not os.path.isfile(path):
                    path_ok = 1
                else:
                    c += 1
        else:
            path = filename
            if path.endswith('.jsonl'):
                path = path[:-6]
            path = path + '.jsonl'
        try:
            with jsonl.open(path, 'w') as fw:
                for d in self.documents:
                    fw.write({'document_id':d.id, 'data':d._get_data()})
            print(f'Results saved to {path}')
        except Exception as e:
            print(e)

    def load_result(self, *args):
        """ Alias for load_results"""
        self.load_results(*args)

    def load_results(self, path = 'results_0', reset = False, chunksize = None):
        """ Loads result from a valid json file."""
        if path.endswith('.json') or path.endswith('.jsonl'):
            pass
        else:
            path = path + '.jsonl'
        try:
            if reset:
                self.reset_data()
            if path.endswith('jsonl'):
                with jsonl.open(path, 'r') as f:
                    for line in f:
                        self.add_document_data(line.get('data'), _id=line.get('document_id', None))
            else:
                raise Exception("Expected jsonl file extension.")
            print(f'Loaded {str(path)} successfully')
        except Exception as e:
            print('Failure to load ' + str(path) + ': ')
            print(e, '\n')

    def split_results(self, input_file, max_document_per_file, output_file=''):
        """ Splits existing json results into multiple files """
        if not output_file:
            output_file = input_file
        with open(input_file, 'r') as f:
            results = json.load(f)
        i = 0
        count = 0
        while i < len(self.documents):
            if isinstance(results, list):
                with open(f"{count}_{output_file}", 'w') as fw:
                    json.dump(result[i:i + max_document_per_file], fw)
            elif isinstance(results, dict):
                with open(f"{count}_{output_file}", 'w') as fw:
                    json.dump({'document_ids':results['document_ids'][i:i + max_document_per_file],\
                            'documents':results['documents'][i:i + max_document_per_file]}, fw)
            i += max_document_per_file
            count += 1
            results['document_ids']

    def reset_data(self):
        """ Erase current data """
        self.documents = []
        self.data = self.documents
        self.max = 0
        self._next_id = 0
    
    def reformat_data(self, filepath, output_file):
        """ Takes the path of a results file with the old sentence format 
            and writes it to a new file with the new document format"""
        data = []
        idx = 0
        if filepath.endswith('jsonl'):
            with jsonl.open(filepath, 'r') as f:
                for l in f:
                    data.append(l)
        elif filepath.endswith('json'):
            with open(filepath, 'r') as f:
                tmp = json.load(f)
                for t in tmp:
                    data.append({'id':idx, 'data':t})
                idx += 1
        new_data = []
        new_format = {
            'coreference': None,
            'type': None, 
            'domain': None,
            'source_pure': None,
            'language': None,
            'emoticon': None,
            'sentiment': None,
            'emotion': None,
            'sentences': None
        }
        ids = []
        for batch in data:
            tmp = new_format.copy()
            tmp_sentences = []
            ids.append(batch.get('document_id', None))
            tmp['source_pure'] = ' '.join([d.get('source_pure', d.get('source', '')) for d in batch['data']])
            tmp['language'] = batch['data'][0].get('language_used', {}).get('predict', 'fr')
            for s in batch['data']:
                new_sentence = {}
                new_sentence['source'] = s.get('source', None)
                new_sentence['source_pure'] = s.get('source_pure', None)
                new_sentence['sentence_indexes'] = s.get('sentence_source_indexes', None)
                new_sentence['subsentences'] = s.get('proposition', None)
                new_sentence['emotion'] = s.get('emotion', None)
                new_sentence['sentiment'] = s.get('sentiment', None)
                new_sentence['sentence_type'] = s.get('sentence_acts', {}).get('predict', None)
                new_sentence['ner'] = s.get('NER', None)
                new_sentence['detail'] = s.get('synthesis', None)
                tmp_sentences.append(new_sentence)
            tmp['sentences'] = tmp_sentences
            new_data.append(tmp)
        if new_data:
            with jsonl.open(output_file, 'w') as f:
                for _id, d in zip(ids, new_data):
                    f.write({'data':d, 'document_id':_id})