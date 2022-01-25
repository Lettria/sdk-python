from .utils import flatten_lst, StrProperty, ListProperty, DictProperty, IntProperty
from .utils import GLOBAL, DOC, SENT, SUB, TOK
from .TextChunk import TextChunk
from .Subsentence import Subsentence
from .Token import Token
from .Span import Span
from .Cluster import Cluster

def clear_data(data_json):
    def clean_recursif(node):
        if isinstance(node, list):
            for e in node:
                clean_recursif(e)  
        elif isinstance(node, dict):
            keys = list(node.keys())
            for k in keys:
                if k == 'detail':
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
    data_json = {k:v for k,v in data_json.items() if v and k in ['source', 'language_used', 'source_pure', 'ml_sentiment', 'subsentences', 'sentiment', 'sentence_acts', 'ml_emotion', 'emotion', 'detail']}
    data_json['detail'] = [{k:v for k,v in i.items() if v not in [[], {}, None]} for i in data_json.get('detail', [])]
    clean_recursif(data_json)
    return data_json

class Sentence(TextChunk):
    __slots__ = ("data", "n", "max", "_id", "ref_document")

    def __init__(self, data_sentence, idx=0, ref_document=None):
        super(Sentence, self).__init__()
        # self.data = clear_data(data_sentence)
        self.data = data_sentence
        self.max = len(self.data.get('detail', []))
        # self._ner_fix()
        self._id = idx
        self.ref_document = ref_document

    @property
    def id(self):
        return self._id

    # To modify when desambiguisation is active and only one NER entity is returned for each token
    def _ner_fix(self):
        for i, d in enumerate(self.data.get('detail', [])):
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
                self.data['detail'][i]['type'] = ner

    def __repr__(self):
        return self.str

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            self.n += 1
            return Token(self.data.get('detail', [])[self.n - 1], self.n -1, self.data.get('source_pure', self.data.get('source', None)), self)
        else:
            raise StopIteration

    @ListProperty
    def sentences(self):
        return [self]

    def _get_subsentence(self, _id, _idx):
        ''' Dividing information for each subsentence, then it can use 
        normal Sentence methods to access its data'''
        data = {}
        data['detail'] = self.data.get('detail', [])[_idx['start_id']:_idx['end_id'] + 1]
        data['source'] = ' '.join([k.get('source', '') if k.get('source', '') else '' for k in data['detail']])
        data['source_pure'] = self.data.get('source_pure', '')
        if len(self.data.get('sentiment', {}).get('subsentences', [])) > _id:
            data['sentiment'] = self.data['sentiment'].get('subsentences', [])[_id]
        if len(self.data.get('emotion', {}).get('subsentences', [])) > _id:
            data['emotion'] = self.data['emotion'].get('subsentences', [])[_id]
        return Subsentence(data)

    @ListProperty
    def tokens(self):
        return [Token(s, i, self.data.get('source_pure', self.data.get('source', None)), self) for i, s in enumerate(self.data.get('detail', []))]

    @ListProperty
    def subsentences(self):
        return [self._get_subsentence(_id, idx) for _id, idx in enumerate(self.data.get('subsentences', []))]

    @StrProperty
    def str(self):
        return self.data.get('source', None)

    @StrProperty
    def original_text(self):
        return self.data.get('source_pure', self.data.get('source', None))

    @ListProperty
    def synthesis(self):
        return self.data.get('detail', [])

    @ListProperty
    def detail(self):
        return self.data.get('detail', [])

    @ListProperty
    def emotion(self):
        return [(k, round(v,4)) for k,v in self.data.get('emotion', {}).get('values', {}).items() if v != 0]

    @DictProperty
    def emotion_ml(self):
        return self.emotion

    @DictProperty
    def sentiment(self):
        return self.data.get('sentiment', {}).get('values', {})

    @DictProperty
    def sentiment_ml(self):
        return self.sentiment

    @StrProperty
    def sentence_type(self):
        return self.data.get('sentence_type', None)

    @ListProperty
    def token(self):
        return [s.get('source', None) for s in self.data.get('detail', [])]
    
    @ListProperty
    def spans(self):
        spans = [self.ref_document.document_data.get('coreference').get('spans', [])[idx] for idx in self.data.get('coreference', [])]
        return [Span(sp, self.ref_document) for sp in spans]

    @ListProperty
    def clusters(self):
        spans = [self.ref_document.document_data.get('coreference').get('spans', [])[idx] for idx in self.data.get('coreference', [])]
        clusters_idx = list(set([span['cluster_index'] for span in spans]))
        clusters = [(cl, self.ref_document.document_data.get('coreference').get('clusters', [])[cl]) for cl in clusters_idx]
        return [Cluster(cluster_idx, spans_idx, self.ref_document) for cluster_idx, spans_idx in clusters]