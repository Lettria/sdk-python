import sys
import os
import json
import jsonlines as jsonl
from .client import Client
from .subtypes import Token, Subsentence
from .utils import flatten_lst, StrProperty, ListProperty, DictProperty
from .TextChunk import TextChunk

#Accepted arguments for hierarchical levels
GLOBAL =    ['g', 'global', 'glob']
DOC =       ['d', 'doc', 'document', 'documents']
SENT =      ['s', 'sentence', 'sent', 'sentences']
SUB =       ['sub', 'subsentence', 'subsentences']
TOK =       ['t', 'token', 'tok', 'tokens']

class PipelineError(Exception): pass
class RequestError(Exception): pass

def clear_data(data_json):
    def clean_recursif(node):
        if isinstance(node, list):
            for e in node:
                clean_recursif(e)  
        elif isinstance(node, dict):
            keys = list(node.keys())
            for k in keys:
                if k == 'synthesis':
                    continue
                if k == 'confidence' or node[k] in [[], {}, None]:
                    node.pop(k)
                elif isinstance(node[k], dict):
                    clean_recursif(node[k])
                    if not node[k]:
                        node.pop(k)
                elif isinstance(node[k], list):
                    clean_recursif(node[k])
                    if not node[k]:
                        node.pop(k)
        else:
            return None

    if not isinstance(data_json, dict): 
        data_json = {}
    data_json = {k:v for k,v in data_json.items() if v and k in ['source', 'language_used', 'source_pure', 'ml_sentiment', 'proposition', 'sentiment', 'sentence_acts', 'ml_emotion', 'emotion', 'synthesis']}
    data_json['synthesis'] = [{k:v for k,v in i.items() if v not in [[], {}, None]} for i in data_json.get('synthesis', [])]
    clean_recursif(data_json)
    return data_json

class Sentence(TextChunk):
    __slots__ = ("data", "n", "max", "id")

    def __init__(self, data_sentence, idx=0):
        super(Sentence, self).__init__()
        self.data = clear_data(data_sentence)
        self.max = len(self.data.get('synthesis', []))
        self._ner_fix()
        self.id = idx

    # To modify when desambiguisation is active and only one NER entity is returned for each token
    def _ner_fix(self):
        for i, d in enumerate(self.data.get('synthesis', [])):
            ner = []
            for m in d.get('meaning', []):
                if 'super' in m and m['super']:
                    if m['super'].lower() in ['location', 'person', 'organization']:
                        if m['super'].lower() not in ner:
                            ner.append(m['super'].lower())
                    elif m['super'] == 'ENTITY':
                        ner.append(m['sub'])
                if 'sub' in m and m['sub']:
                    if m['sub'] == 'number':
                        ner.append(m['sub'])
            if ner:
                self.data['synthesis'][i]['type'] = ner

    def __repr__(self):
        return self.str

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            self.n += 1
            return Token(self.data.get('synthesis', [])[self.n - 1], self.n -1, self.data.get('source_pure', self.data.get('source', None)))
        else:
            raise StopIteration

    @property
    def idx(self):
        return self.id

    @ListProperty
    def sentences(self):
        return [self]

    def _get_subsentence(self, _id, _idx):
        ''' Dividing information for each subsentence, then it can use 
        normal Sentence methods to access its data'''
        data = {}
        data['synthesis'] = self.data.get('synthesis', [])[_idx['start_id']:_idx['end_id'] + 1]
        data['source'] = ' '.join([k.get('source', '') if k.get('source', '') else '' for k in data['synthesis']])
        data['source_pure'] = self.data.get('source_pure', '')
        if len(self.data.get('sentiment', {}).get('subsentences', [])) > _id:
            data['sentiment'] = self.data['sentiment'].get('subsentences', [])[_id]
        if len(self.data.get('emotion', {}).get('subsentences', [])) > _id:
            data['emotion'] = self.data['emotion'].get('subsentences', [])[_id]
        if len(self.data.get('ml_emotion', {}).get('subsentence', [])) > _id:
            data['ml_emotion'] = {'sentence': self.data.get('ml_emotion', {}).get('subsentence', [])[_id]}
        if len(self.data.get('ml_sentiment', {}).get('subsentence', [])) > _id:
            data['ml_sentiment'] = {'sentence':{'value':self.data['ml_sentiment'].get('subsentence', {})[_id]}}
        return Subsentence(data)

    @ListProperty
    def tokens(self):
        return [Token(s, i, self.data.get('source_pure', self.data.get('source', None))) for i, s in enumerate(self.data.get('synthesis', []))]

    @ListProperty
    def subsentences(self):
        return [self._get_subsentence(_id, idx) for _id, idx in enumerate(self.data.get('proposition', []))]

    @ListProperty
    def token(self):
        return [s.get('source', None) for s in self.data.get('synthesis', [])]

    @StrProperty
    def str(self):
        return self.data.get('source', None)

    @StrProperty
    def original_text(self):
        return self.data.get('source_pure', self.data.get('source', None))

    @ListProperty
    def lemma(self):
        return [s.get('lemma', None) for s in self.data.get('synthesis', [])]

    @ListProperty
    def lemma_detail(self):
        return flatten_lst([s.lemma_detail for s in self.tokens])

    @ListProperty
    def synthesis(self):
        return self.data.get('synthesis', [])

    @ListProperty
    def pos(self):
        return [s.get('tag', None) for s in self.data['synthesis']]

    @ListProperty
    def pos_detail(self):
        return flatten_lst([s.pos_detail for s in self.tokens])

    @ListProperty
    def dep(self):
        return [s.get('dep', None) for s in self.data['synthesis']]

    @DictProperty
    def language(self):
        return self.data.get('language_used', {}).get('sentence_level', {}).get('label', {})

    @ListProperty
    def meaning(self):
        return [[(m.get('super', ''), m.get('sub', '')) for m in t.get('meaning', [])] for t in self.data['synthesis']]

    @ListProperty
    def emotion(self):
        return [(k, round(v,4)) for k,v in self.data.get('emotion', {}).get('values', {}).items() if v != 0]

    @DictProperty
    def emotion_ml(self):
        return [(e.get('type', None), round(e.get('value', 0), 4)) for e in self.data.get('ml_emotion', {}).get('sentence', [])]

    @DictProperty
    def sentiment_ml(self):
        return self.data.get('ml_sentiment', {}).get('sentence', {}).get('value', 0)

    @DictProperty
    def sentiment(self):
        return self.data.get('sentiment', {}).get('values', {})

    @ListProperty
    def sentiment_target(self):
        return [(e.get('target', {}).get('source', None), e.get('source', {}).get('source', None), e.get('value', 0)) for e in self.data.get('sentiment', {}).get('elements', []) if 'target' in e and e['target']]

    @StrProperty
    def sentence_type(self):
        return self.data.get('sentence_acts', {}).get('predict', None)

    @ListProperty
    def ner(self):
        return [t.ner for t in self.tokens]

    @ListProperty
    def morphology(self):
        return [t.morphology for t in self.tokens]

    @ListProperty
    def coreference(self):
        return [t.coreference for t in self.tokens]

class Document(TextChunk):
    __slots__ = ("sentences", "data", "n", "max", "id")
    def __init__(self, sentences, _id):
        super(Document, self).__init__()
        self.sentences = [Sentence(s, i) for i, s in enumerate(sentences)]
        self.max = len(self.sentences)
        self.data = self.sentences
        self.id = str(_id)

    @property
    def idx(self):
        return self.id

    @ListProperty
    def subsentences(self):
        return flatten_lst([s.subsentences for s in self.sentences])

    @ListProperty
    def tokens(self):
        return flatten_lst([s.tokens for s in self.sentences])

    @ListProperty
    def documents(self):
        return [self]

    def add_sentence(self, sentence):
        self.sentences.append(sentence)
        self.max += 1

    def __repr__(self):
        return str(self.sentences)

    def _get_data(self):
        return [s.data for s in self.sentences]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            self.n += 1
            return self.sentences[self.n - 1]
        else:
            raise StopIteration

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
        self.fields = [p for p in dir(Sentence) if isinstance(getattr(Sentence,p),property)]
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
        """ Direct access to all sentences"""
        return flatten_lst([d.sentences for d in self.documents])

    @ListProperty
    def subsentences(self):
        """ Direct access to all subsentences"""
        sentences = flatten_lst([d.sentences for d in self.documents])
        return flatten_lst([s.subsentences for s in sentences])

    @ListProperty
    def tokens(self):
        """ Direct access to all tokens"""
        return flatten_lst([s.tokens for s in self.sentences])

    @property
    def nlp(self):
        return [self]

    def _generate_properties(self):
        """ Takes properties of the Sentence class and dynamically create properties for 
            NLP, Document and Subsentence class."""
        for _class in [Document, NLP]: #adding to nlp and document
            for field in self.fields:
                if field in ['subsentences', 'tokens', 'sentences']:
                    continue
                setattr(_class, field, property(self._make_lambda(field)))
                setattr(_class, field + '_flat', property(self._make_lambda(field, True)))
        for _class in [Subsentence]: #adding specific properties for subsentence
            for field in [p for p in dir(Sentence) if isinstance(getattr(Sentence, p), property)]:
                filters = ['sentiment_target', 'morphology', 'ner', 'token', 'str', \
                            'lemma', 'lemma_detail', 'synthesis', 'pos', 'pos_detail', 'dep', 'language', 'meaning', \
                            'sentiment', 'sentiment_ml', 'emotion', 'emotion_ml', 'tokens']
                if field in filters:
                    setattr(_class, field, getattr(Sentence, field))
                elif field not in ['subsentences']:
                    setattr(_class, field, property(self._make_lambda_sub(field)))
        for _class in [Sentence, Subsentence]: #adding flat variants to sentence and subsentence for convenience
            for field in self.fields:
                setattr(_class, field + '_flat', property(self._make_lambda_sent(field)))

    def _make_lambda(self, field, flatten = False):
        """ Returns lambda functions to be added as property to classes"""
        if not flatten:
            return lambda c_self : [getattr(s, field) for s in c_self.data]
        else:
            return lambda c_self : flatten_lst([getattr(s, field) for s in c_self.data])

    def _make_lambda_sub(self, field):
        """ Returns lambda functions to be added as property to classes"""
        return lambda x: field + ' not available for subsentences'

    def _make_lambda_sent(self, field):
        """ Returns lambda functions to be added as property to classes"""
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

    def _check_result(self, result):
        """ Check if synthesis key is empty """
        bad_idx = []
        for i, r in enumerate(result):
            if not isinstance(r, dict) or not 'synthesis' in r:
                bad_idx.append(i)
        return bad_idx

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

    def _request(self, document, skip_document = False, verbose=False):
        """ Input: string or list of string"""
        results = []
        try:
            results = self.client.request(document)
            if results is None:
                raise RequestError
        except RequestError:
            if skip_document:
                return None
        if isinstance(results, list):
            bad_idx = self._check_result(results)
            if bad_idx:
                if skip_document:
                        print("WARNING: Skipping document, error in sentences processing.")
                        return None
                elif verbose:
                    for i in bad_idx:
                        print("Error processing sentence", i)
        return results

    def _request_batch(self, batch_documents, document_ids, skip_document = False):
        ''' Input: string or list of string'''
        results = self.client.request_batch(batch_documents)
        if skip_document:
            for idx in range(len(results) - 1, -1, -1):
                if not results[idx]:
                    print("WARNING: Skipping document, request error.")
                    results.pop(idx)
                    if document_ids:
                        document_ids.pop(idx)
                elif self._check_result(results[idx]):
                    print("WARNING: Skipping document, error in sentences processing.")
                    results.pop(idx)
                    if document_ids:
                        document_ids.pop(idx)
        return results, document_ids

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
            results, document_ids = self._request_batch(batch_documents, document_ids = document_ids, skip_document=skip_document)
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

    def add_document(self, document, skip_document=False, id=None, verbose=True):
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
            results = self._request(document, skip_document=skip_document, verbose=verbose)

        if results is None and skip_document == True:
            if not document:
                print("Skpping document, received empty input.")
            else:
                print("Skpping document, processing failed.")
        else:
            if id == None:
                next_doc_id = self._next_id
                self._next_id += 1
            else:
                next_doc_id = id
            if isinstance(results, list):
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

    def add_document_data(self, doc_data, id=None):
        self.documents.append(Document(doc_data, id))
        self.max += 1

    def _get_data(self):
        return [d._get_data() for d in self.documents]

    def save_result(self, *args):
        """ Alias for save_result"""
        self.save_results(*args)

    def save_results(self, file = ''):
        """ Writes json result to a file with the specified name."""
        path_ok = 0
        c = 0
        if not self.data:
            print("No data to save.")
            return
        if not file:
            file = 'results'
            while not path_ok:
                path = file + '_' + str(c) + '.jsonl'
                if not os.path.isfile(path):
                    path_ok = 1
                else:
                    c += 1
        else:
            path = file
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
                        self.add_document_data(line.get('data'), id=line.get('document_id', None))
            elif path.endswith('json'):
                with open(path, 'r') as f:
                    result = json.load(f)
                    if isinstance(result, dict):
                        assert len(result.get('document_ids', [])) == len(result.get('documents', [])), \
                                "'document_ids' and 'documents' should be of similar length"
                        for id_, r in zip(result['document_ids'], result['documents']):
                            self.add_document_data(r, id=id_)
                    else:
                        for r in result:
                            self.add_document_data(r)
            print(f'Loaded {path} successfully')
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