from .utils import flatten_lst, StrProperty, ListProperty, DictProperty, IntProperty
from .utils import GLOBAL, DOC, SENT, SUB, TOK
from .TextChunk import TextChunk
from .Subsentence import Subsentence
from .Token import Token
from .Span import Span
from .Cluster import Cluster

class Sentence(TextChunk):
    __slots__ = ("data", "n", "max", "_id", "ref_document")

    def __init__(self, data_sentence, idx=0, ref_document=None):
        """ Class that represents a sentence.

        Args:
            data_sentence (dict): dict with sentence data.
            idx (int, optional): Index of the sentence in the document. Defaults to 0.
            ref_document (Document, optional): Reference to the document. Defaults to None.
        """
        super(Sentence, self).__init__()
        self.data = data_sentence
        self.max = len(self.data.get('detail', []))
        self._ner_to_detail()
        self._id = idx
        self.ref_document = ref_document

    @property
    def id(self) -> int:
        return self._id

    @property
    def idx(self) -> int:
        return self.id

    def _ner_to_detail(self):
        """ Inject NER data into the detail key to be used by Token."""
        for m in self.data.get('ml_ner', []):
            if len(self.data.get('detail', [])) > m['index']:
                self.data['detail'][m['index']]['value'] = m['value']
                self.data['detail'][m['index']]['type'] = m['type']

    def __repr__(self):
        return self.str

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> Token:
        if self.n < self.max:
            self.n += 1
            return Token(
                self.data.get('detail', [])[self.n - 1], 
                self.n -1, 
                self.data.get('source_pure', self.data.get('source', None)), 
                self)
        else:
            raise StopIteration

    @ListProperty
    def sentences(self) -> list:
        return [self]

    def _get_subsentence(self, _id, _idx) -> Subsentence:
        """ Divides sentence information to each subsentence."""
        data = {}
        data['detail'] = self.data.get('detail', [])[_idx['start_id']:_idx['end_id'] + 1]
        data['source'] = ' '.join([k.get('source', '') if k.get('source', '') else '' for k in data['detail']])
        data['source_pure'] = self.data.get('source_pure', '')
        if len(self.data.get('sentiment', {}).get('subsentences', [])) > _id:
            data['sentiment'] = self.data['sentiment'].get('subsentences', [])[_id]
        if len(self.data.get('emotion', {}).get('subsentences', [])) > _id:
            data['emotion'] = self.data['emotion'].get('subsentences', [])[_id]
        if len(self.data.get('ml_sentiment', {}).get('subsentence', [])) > _id:
            data['ml_sentiment'] = {'sentence': self.data['ml_sentiment']['sentence'], 'subsentence': {'value': self.data['ml_sentiment']['subsentence'][_id]}}
        if len(self.data.get('ml_emotion', {}).get('subsentence', [])) > _id:
            data['ml_emotion'] = {'sentence': self.data['ml_emotion']['sentence'], 'subsentence': self.data['ml_emotion']['subsentence'][_id]}
        return Subsentence(data)

    @ListProperty
    def tokens(self) -> list:
        return [Token(s, i, self.data.get('source_pure', self.data.get('source', None)), self) for i, s in enumerate(self.data.get('detail', []))]

    @ListProperty
    def subsentences(self) -> list:
        return [self._get_subsentence(_id, idx) for _id, idx in enumerate(self.data.get('subsentences', []))]

    @StrProperty
    def str(self) -> str:
        return self.data.get('source', None)

    @StrProperty
    def original_text(self) -> str:
        return self.data.get('source_pure', self.data.get('source', None))

    @ListProperty
    def synthesis(self) -> list: ## for compatibility purpose
        return self.data.get('detail', [])

    @ListProperty
    def detail(self) -> list:
        return self.data.get('detail', [])

    @ListProperty
    def emotion(self) -> list:
        return [(k, round(v,4)) for k,v in self.data.get('emotion', {}).get('values', {}).items() if v != 0]

    @DictProperty
    def emotion_ml(self) -> list:
        if self.__class__.__name__ == 'Sentence':
            return [(dic['type'], round(dic['value'],4)) for dic in self.data.get('ml_emotion', {}).get('sentence', {}) if dic['value'] != 0]
        elif self.__class__.__name__ == 'Subsentence':
            return [(dic['type'], round(dic['value'],4)) for dic in self.data.get('ml_emotion', {}).get('subsentence', {}) if dic['value'] != 0]
            

    @DictProperty
    def sentiment(self) -> dict:
        return self.data.get('sentiment', {}).get('values', {})

    @DictProperty
    def sentiment_ml(self) -> dict:
        if self.__class__.__name__ == 'Sentence':
            return {'total': self.data.get('ml_sentiment', {}).get('sentence', {}).get('value', 0)}
        elif self.__class__.__name__ == 'Subsentence':
            return {'total': self.data.get('ml_sentiment', {}).get('subsentence', {}).get('value', 0)}

    @StrProperty
    def sentence_type(self) -> str:
        return self.data.get('sentence_type', None)

    @ListProperty
    def token(self) -> list:
        return [s.get('source', None) for s in self.data.get('detail', [])]
    
    @ListProperty
    def spans(self) -> list:
        spans = [self.ref_document.document_data.get('coreference').get('spans', [])[idx] for idx in self.data.get('coreference', [])]
        return [Span(sp, self.ref_document) for sp in spans]

    @ListProperty
    def clusters(self) -> list:
        spans = [self.ref_document.document_data.get('coreference').get('spans', [])[idx] for idx in self.data.get('coreference', [])]
        clusters_idx = list(set([span['cluster_index'] for span in spans]))
        clusters = [(cl, self.ref_document.document_data.get('coreference').get('clusters', [])[cl]) for cl in clusters_idx]
        return [Cluster(cluster_idx, spans_idx, self.ref_document) for cluster_idx, spans_idx in clusters]