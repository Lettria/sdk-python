from .utils import flatten_lst, StrProperty, ListProperty, DictProperty, IntProperty
from .TextChunk import TextChunk
from .utils import GLOBAL, DOC, SENT, SUB, TOK
from .Sentence import Sentence
from .Cluster import Cluster
from .Span import Span

class Document(TextChunk):
    __slots__ = ("sentences", "document_data", "n", "max", "_id")
    
    def __init__(self, document_data, _id):
        """Class for the document, a collection of sentences with
            additional information at the document level.
        Args:
            document_data (dict): dict with document data.
            _id (int or str): id of the document.
        """
        super(Document, self).__init__()
        self.sentences = [Sentence(s, i, self) for i, s in enumerate(document_data['sentences'])]
        self.document_data = {k:v for k,v in document_data.items() if k != 'sentences'}
        self.max = len(self.sentences)
        self.data = self.sentences
        self._id = str(_id)

    @property
    def id(self):
        return self._id
    
    def __repr__(self):
        return str(self.sentences)

    def _get_data(self) -> dict:
        tmp = self.document_data
        tmp['sentences'] = [s.data for s in self.sentences]
        return tmp

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> Sentence:
        if self.n < self.max:
            self.n += 1
            return self.sentences[self.n - 1]
        else:
            raise StopIteration
    
    @ListProperty
    def subsentences(self) -> list:
        return flatten_lst([s.subsentences for s in self.sentences])

    @ListProperty
    def tokens(self) -> list:
        return flatten_lst([s.tokens for s in self.sentences])

    @ListProperty
    def documents(self) -> list:
        return [self]

    @StrProperty
    def str_doc(self) -> str:
        return self.document_data.get('source_pure', None)

    @StrProperty
    def original_text_doc(self) -> str:
        return self.document_data.get('source_pure', None)

    @DictProperty
    def emotion_doc(self) -> list:
        return self.document_data.get('emotion', None)
    
    @IntProperty
    def sentiment_doc(self) -> float:
        return self.document_data.get('sentiment', None)
    
    @StrProperty
    def domain_doc(self):
        return self.document_data.get('domain', None)

    @StrProperty
    def type_doc(self):
        return self.document_data.get('type', None)

    @StrProperty
    def original_text_doc(self) -> str:
        return self.document_data.get('source_pure', None)

    @ListProperty
    def emoticon_doc(self) -> list:
        return self.document_data.get('emoticon_data', {})

    @ListProperty
    def spans(self) -> list:
        return [Span(sp, self) for i, sp in enumerate(self.document_data.get('coreference').get('spans', []))]

    @ListProperty
    def clusters(self) -> list:
        return [Cluster(i, spans_idx, self) for i, spans_idx in enumerate(self.document_data.get('coreference').get('clusters', []))]

    def replace_coreference(self, attribute = 'source', replace=['CLS']) -> list:
        """Replaces coreference mentions with the head of the cluster in the text

        Args:
            attribute (str, optional): Attribute to get. Defaults to 'source'.
            replace (list, optional): Defines what kind of spans get replaced by head span. Defaults to ['CLS'].

        Returns:
            list: List of sentences with the desired attribute information and replacement.
        """
        text = [[getattr(t, attribute) for t in s ] for s in self.sentences]
        for cl in self.clusters:
            head = cl.head
            children = sorted(cl.children, key=lambda x: x.tokens_idx[-1], reverse=True)
            for child in children:
                if set(replace) & set(child.get_attributes('pos')):
                    text[child.sentence_idx] = text[child.sentence_idx][:child.tokens_idx[0]] \
                    + text[head.sentence_idx][head.tokens_idx[0]:head.tokens_idx[-1] + 1] \
                    + text[child.sentence_idx][child.tokens_idx[-1] + 1:]
        return text