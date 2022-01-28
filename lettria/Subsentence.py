from .transform_morph import transform_data
from .utils import StrProperty, ListProperty, DictProperty
from .TextChunk import TextChunk
from .Token import Token

class Subsentence(TextChunk):
    __slots__ = ("data", "n", "max")

    def __init__(self, data_sentence):
        """Class for a subsentence, a group of words part of a sentence.
        Args:
            data_sentence (dict): Dict with the data relative to the subsentence.
        """
        super(Subsentence, self).__init__()
        self.data = data_sentence
        self.max = len(self.data['detail'])

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
    def subsentences(self) -> list:
        return [self]