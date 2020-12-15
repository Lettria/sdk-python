import sys
import os
import json
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

class Sentence(TextChunk):
    __slots__ = ("data", "n", "max")

    def __init__(self, data_sentence):
        super(TextChunk, self).__init__()
        self.data = data_sentence
        self.max = len(self.data.get('synthesis', []))
        self._ner_fix()

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
            self.data['synthesis'][i]['type'] = ner

    def __repr__(self):
        return str(self.data)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            self.n += 1
            return Token(self.data.get('synthesis', [])[self.n - 1])
        else:
            raise StopIteration

    @ListProperty
    def sentences(self):
        return [self]

    def _get_subsentence(self, id, idx):
        ''' Dividing information for each subsentence, then it can use 
        normal Sentence methods to access its data'''
        data = {}
        data['synthesis'] = self.data['synthesis'][idx['start_id']:idx['end_id'] + 1]
        data['source'] = ' '.join([t.get('source', '') for t in data['synthesis']])
        if len(self.data['sentiment'].get('subsentences', [])) > id:
            data['sentiment'] = self.data['sentiment'].get('subsentences', [])[id]
        if len(self.data.get('ml_emotion', {}).get('subsentence', [])) > id:
            data['ml_emotion'] = {'sentence': self.data.get('ml_emotion', {}).get('subsentence', [])[id]}
        if len(self.data.get('ml_sentiment', {}).get('subsentence', [])) > id:
            data['ml_sentiment'] = {'sentence': self.data['ml_sentiment'].get('subsentence', [])[id]}
        return Subsentence(data)

    @ListProperty
    def tokens(self):
        return [Token(s) for s in self.data.get('synthesis', [])]

    @ListProperty
    def subsentences(self):
        return [self._get_subsentence(id, idx) for id, idx in enumerate(self.data.get('proposition', []))]

    @ListProperty
    def token(self):
        return [s.get('source', None) for s in self.data.get('synthesis', [])]

    @StrProperty
    def str(self):
        return self.data.get('source', None)

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
        return [[(m['super'] or '', m['sub'] or '') for m in t.get('meaning', [])] for t in self.data['synthesis']]

    @ListProperty
    def emotion(self):
        return [(e.get('type', None), round(e.get('value', 0), 4)) for e in self.data.get('ml_emotion', {}).get('sentence', [])]

    @DictProperty
    def emotion_ml(self):
        return self.emotion

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
    next_id = 0
    def __init__(self, sentences, id=None):
        super(TextChunk, self).__init__()
        self.sentences = [Sentence(s) for s in sentences]
        self.max = len(self.sentences)
        self.data = self.sentences
        if id is None:
            id = Document.next_id
            Document.next_id += 1
        self.id = str(id)

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
        super(TextChunk, self).__init__()
        self.client = None
        if client or api_key:
            self.add_client(client, api_key)
        self.documents = []
        self.max = len(self.documents)
        self.data = self.documents
        self.fields = [p for p in dir(Sentence) if isinstance(getattr(Sentence,p),property)]
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
            if not r['synthesis']:
                bad_idx.append(i)
        return bad_idx

    def _request(self, data, skip_document = False):
        ''' Input: string or list of string'''
        results = []
        
        for i, seq in enumerate(data):
            try:
                res = self.client.request(seq)
                if res is None:
                    raise RequestError
                results += res
            except RequestError:
                if skip_document:
                    print("WARNING: Skipping document, request error ")
                    return None
                else:
                    print("WARNING request error: Document " + str(Document.next_id) + " skipping sentence " + str(i))

        try:
            bad_idx = self._check_result(results)
            if bad_idx:
                if skip_document:
                    raise PipelineError
                else:
                    for idx in sorted(bad_idx, reverse=True):
                        print("WARNING pipeline error: Document " + str(Document.next_id) + " skipping sentence " + str(idx))
                        results.pop(idx)
        except PipelineError:
            print("WARNING: Skipping document, pipeline error ")
            return None
        return results

    def add_client(self, client = None, api_key = None):
        if client and isinstance(client, Client):
            self.client = client
        elif api_key:
            self.client = Client(api_key)
        else:
            print('Please provide a client instance or an api_key.')

    def add_document(self, document, skip_document=False, id=None):
        """ Performs request to lettria API for a document and stores it.
            skip_document: If False document is added even if empty or request failed.
            id: Id given to document, by default sequential integer """
        
        def preprocess_input(document):
            if isinstance(document, str):
                if document.strip():
                    document = [document.strip()]
                else:
                    return None
            elif isinstance(document, list):
                document = [d.strip() for d in flatten_lst(document) if d.strip()]
            else:
                print('document argument should be of type list or str.')
                raise TypeError
            return document
        
        if not self.client:
            print('Failure : Please assign a client or api_key with add_client() in order to make a request. ')
            return
        
        results = None
        document = preprocess_input(document)
        
        if document:
            results = self._request(document, skip_document=skip_document)

        if results is None and skip_document == True:
            if not document:
                print("Skpping document, received empty input.")
            else:
                print("Skpping document, processing failed.")
        else:
            if isinstance(results, list):
                self.documents.append(Document(results, id=id))
                print("Added document " + str(self.documents[-1].id) + '.')
            else:
                if not document:
                    self.documents.append(Document([], id=id))
                    print("Added empty document " + str(self.documents[-1].id) + ': received empty input.')
                else:
                    self.documents.append(Document([], id=id))
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
                path = file + '_' + str(c) + '.json'
                if not os.path.isfile(path):
                    path_ok = 1
                else:
                    c += 1
        else:
            path = file
            if path.endswith('.json'):
                path = path[:-5]
            path = path + '.json'
        try:
            with open(path, 'w') as f:
                json.dump({'document_ids': [d.id for d in self.documents],'documents':self._get_data()}, f)
            print(f'Results saved to {path}\n')
        except Exception as e:
            print(e)

    def load_result(self, *args):
        """ Alias for load_results"""
        self.load_results(*args)

    def load_results(self, path = 'results_0', reset = False):
        """ Loads result from a valid json file."""
        if path.endswith('.json'):
            path = path[:-5]
        path = path + '.json'
        try:
            with open(path, 'r') as f:
                result = json.load(f)
                if reset:
                    self.reset_data()
                if isinstance(result, dict):
                    assert len(result.get('document_ids', [])) == len(result.get('documents', [])), \
                            "'document_ids' and 'documents' should be of similar length"
                    for id_, r in zip(result['document_ids'], result['documents']):
                        self.add_document_data(r, id=id_)
                else:
                    for r in result:
                        self.add_document_data(r)
            print(f'Loaded {path} successfully\n')
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
        # for n in number:

    def reset_data(self):
        """ Erase current data """
        self.documents = []
        self.data = self.documents
        self.max = 0
        Document.next_id = 0