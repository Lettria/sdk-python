from .transform_morph import transform_data
from .utils import StrProperty, ListProperty, DictProperty
from .TextChunk import TextChunk

class Subsentence(TextChunk):
    __slots__ = ("data", "n", "max")

    def __init__(self, data_sentence):
        self.data = data_sentence
        self.max = len(self.data['synthesis'])

    def __repr__(self):
        return str(self.data)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            self.n += 1
            return Token(self.data['synthesis'][self.n - 1])
        else:
            raise StopIteration
    
    @ListProperty
    def subsentences(self):
        return [self]

class Token:
    __slots__ = ("data")

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return self.data.get('source', None)

    @StrProperty
    def token(self):
        return self.data.get('source', None)

    @StrProperty
    def source(self):
        return self.data.get('source', None)

    @StrProperty
    def str(self):
        return self.data.get('source', None)

    @StrProperty
    def pos(self):
        return self.data.get('tag', None)

    @StrProperty
    def pos(self):
        return self.data.get('tag', None)

    @ListProperty
    def pos_detail(self):
        if self.data['nlp']:
            return [l.get('tag', None) for l in self.data['nlp']]
        else:
            return [self.data.get('tag', None)]

    @DictProperty
    def ner(self):
        type_ = self.data.get('type', '')
        value = self.data.get('value', '')
        tmp = {}
        if type_:
            tmp['type'] = type_
        if value:
            tmp['value'] = value
        return tmp

    @StrProperty
    def coreference(self):
        if 'coreference' in self.data and self.data['coreference']:
            return self.data['coreference'][0].get('source', None)
        return None

    @StrProperty
    def lemma(self):
        return self.data.get('lemma', None)

    @ListProperty
    def lemma_detail(self):
        lemmas = []
        if self.data.get('nlp', []):
            for l in self.data.get('nlp', []):
                if 'number' in l.get('lemmatizer', {}):
                    lemmas.append(l.get('lemmatizer', {}).get('number', {}))
                elif 'source' in l.get('lemmatizer', {}):
                    lemmas.append(l.get('lemmatizer', {}).get('source', {}))
                else:
                    lemmas.append(l.get('source', ''))
            return lemmas
        else:
            return [self.data.get('lemma', None)]

    @ListProperty
    def morphology(self):
        if self.data.get('nlp', []):
            self.data['nlp']
            return transform_data(self.data['nlp'])
        else:
            return []

    @StrProperty
    def dep(self):
        return self.data.get('dep', None)

    @StrProperty
    def ref(self):
        return self.data.get('ref', None)

    @ListProperty
    def meaning(self):
        return [(m['super'] or '', m['sub'] or '') for m in self.data.get('meaning', [])]

    def __format__(self, format_spec):
        return format(str(self), format_spec)
