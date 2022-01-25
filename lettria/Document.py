from .utils import flatten_lst, StrProperty, ListProperty, DictProperty, IntProperty
from .TextChunk import TextChunk
from .utils import GLOBAL, DOC, SENT, SUB, TOK
from .Sentence import Sentence
from .Cluster import Cluster
from .Span import Span

class Document(TextChunk):
    __slots__ = ("sentences", "document_data", "n", "max", "_id")
    def __init__(self, document_data, _id):
        super(Document, self).__init__()
        self.sentences = [Sentence(s, i, self) for i, s in enumerate(document_data['sentences'])]
        self.document_data = {k:v for k,v in document_data.items() if k != 'sentences'}
        self.max = len(self.sentences)
        self.data = self.sentences
        self._id = str(_id)


        ## A SUPPRIMER
        self.document_data['coreference'] = {
            "spans": [
                {"sentence_index": 0, "token_indexes": [0, 1], "cluster_index": 0},
                {"sentence_index": 0, "token_indexes": [3, 4, 5, 6], "cluster_index": 0},
                {"sentence_index": 1, "token_indexes": [0], "cluster_index": 1},
                {"sentence_index": 3, "token_indexes": [0, 1, 2], "cluster_index": 2},
                {"sentence_index": 3, "token_indexes": [3], "cluster_index": 1},
                {"sentence_index": 3, "token_indexes": [6], "cluster_index": 3},
                {"sentence_index": 2, "token_indexes": [0,1,2,3,4], "cluster_index": 3},
                {"sentence_index": 2, "token_indexes": [6,7], "cluster_index": 3},
                {"sentence_index": 3, "token_indexes": [11], "cluster_index": 1},
                {"sentence_index": 3, "token_indexes": [14], "cluster_index": 3},

            ],
            "clusters": [
                [0, 1],
                [2, 4, 8],
                [3],
                [5, 6, 7, 9]
            ]
        }

        self.sentences[0].data['coreference'] = [0, 1]
        self.sentences[1].data['coreference'] = [2]
        self.sentences[2].data['coreference'] = []
        self.sentences[3].data['coreference'] = [3, 4, 5]

        self.sentences[0].data['detail'][0]['coreference'] = [0]
        self.sentences[0].data['detail'][1]['coreference'] = [0]
        self.sentences[0].data['detail'][3]['coreference'] = [1]
        self.sentences[0].data['detail'][4]['coreference'] = [1]
        self.sentences[0].data['detail'][5]['coreference'] = [1]
        self.sentences[0].data['detail'][6]['coreference'] = [1]
        
        self.sentences[1].data['detail'][0]['coreference'] = [2]

        self.sentences[3].data['detail'][0]['coreference'] = [3]
        self.sentences[3].data['detail'][1]['coreference'] = [3]
        self.sentences[3].data['detail'][2]['coreference'] = [3]
        self.sentences[3].data['detail'][3]['coreference'] = [4]
        self.sentences[3].data['detail'][6]['coreference'] = [5]

    @property
    def id(self):
        return self._id
    
    def __repr__(self):
        return str(self.sentences)

    def _get_data(self):
        tmp = self.document_data
        tmp['sentences'] = [s.data for s in self.sentences]
        return tmp

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            self.n += 1
            return self.sentences[self.n - 1]
        else:
            raise StopIteration
    
    @ListProperty
    def subsentences(self):
        return flatten_lst([s.subsentences for s in self.sentences])

    @ListProperty
    def tokens(self):
        return flatten_lst([s.tokens for s in self.sentences])

    @ListProperty
    def documents(self):
        return [self]

    @StrProperty
    def str_doc(self):
        return self.document_data.get('source_pure', None)

    @StrProperty
    def original_text_doc(self):
        return self.document_data.get('source_pure', None)

    @DictProperty
    def emotion_doc(self):
        return self.document_data.get('emotion', None)
    
    @IntProperty
    def sentiment_doc(self):
        return self.document_data.get('sentiment', None)
    
    @StrProperty
    def domain_doc(self):
        return self.document_data.get('domain', None)

    @StrProperty
    def type_doc(self):
        return self.document_data.get('type', None)

    @StrProperty
    def original_text_doc(self):
        return self.document_data.get('source_pure', None)

    @ListProperty
    def emoticon_doc(self):
        return self.document_data.get('emoticon_data', {})

    @ListProperty
    def spans(self):
        return [Span(sp, self) for i, sp in enumerate(self.document_data.get('coreference').get('spans', []))]

    @ListProperty
    def clusters(self):
        return [Cluster(i, spans_idx, self) for i, spans_idx in enumerate(self.document_data.get('coreference').get('clusters', []))]