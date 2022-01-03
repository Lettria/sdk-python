from .utils import flatten_lst, StrProperty, ListProperty, DictProperty, IntProperty
from .TextChunk import TextChunk
from .utils import GLOBAL, DOC, SENT, SUB, TOK
from .Sentence import Sentence

class Document(TextChunk):
    __slots__ = ("sentences", "document_data", "n", "max", "_id")
    def __init__(self, document_data, _id):
        super(Document, self).__init__()
        self.sentences = [Sentence(s, i) for i, s in enumerate(document_data['sentences'])]
        self.document_data = {k:v for k,v in document_data.items() if k != 'sentences'}
        self.max = len(self.sentences)
        self.data = self.sentences
        self._id = str(_id)

    @property
    def id(self):
        return self._id
    
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
    
    @ListProperty
    def subsentences(self):
        return flatten_lst([s.subsentences for s in self.sentences])

    @ListProperty
    def tokens(self):
        return flatten_lst([s.tokens for s in self.sentences])

    @ListProperty
    def documents(self):
        return [self]

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
