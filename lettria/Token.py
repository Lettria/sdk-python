from .utils import StrProperty, ListProperty, DictProperty
from .transform_morph import transform_data

class Token:
    __slots__ = ("data", "idx", "pure_source", "ref_sentence")

    def __init__(self, data, idx, pure_source, ref_sentence):
        """Class for a single token, usually a word or symbol.
        Args:
            data (dict): Dict with the data of the token.
            idx (int): Index of the token in the sentence.
            pure_source (str): Original text of the token.
            ref_sentence (Sentence): Reference to the Sentence object.
        """
        self.data = data
        self.idx = idx
        self.pure_source = pure_source
        self.ref_sentence = ref_sentence

    def __repr__(self):
        return self.str

    def __str__(self) -> str:
        return self.data.get('source', None)

    @StrProperty
    def token(self) -> str:
        return self.data.get('source', None)

    @StrProperty
    def original_text(self) -> str:
        idx = self.data.get('source_indexes', None)
        if idx and len(idx) == 2:
            return self.pure_source[idx[0]:idx[1]]
        else:
            return self.token

    @StrProperty
    def source(self) -> str:
        return self.data.get('source', None)

    @StrProperty
    def str(self) -> str:
        return self.data.get('source', None)

    @StrProperty
    def pos(self) -> str:
        return self.data.get('tag', None)

    @DictProperty
    def ner(self) -> dict:
        type_ = self.data.get('type', '')
        value = self.data.get('value', '')
        return {'type': type_, 'value': value} if type_ else {}

    @ListProperty
    def spans(self) -> list:
        if self.data.get('coreference', []):
            return [span for span in self.ref_sentence.spans if self.idx in span.tokens_idx]
        return []

    @ListProperty
    def clusters(self) -> list:
        if self.data.get('coreference', []):
            return [cluster for cluster in self.ref_sentence.clusters if set(cluster.spans_idx) & set(self.data.get('coreference'))]
        return []

    @StrProperty
    def lemma(self) -> str:
        return self.data.get('lemma', None)

    @ListProperty
    def lemma_detail(self) -> list:
        if 'lemmatizer' in self.data:
            if isinstance(self.data['lemmatizer'], list):
                return self.data['lemmatizer']
            elif isinstance(self.data['lemmatizer'], dict):
                return [self.data['lemmatizer']]
        else:
            return []

    @DictProperty
    def auxiliary(self) -> dict:
        return self.data.get('auxiliary', {})

    @StrProperty
    def gender(self) -> str:
        l_d = self.lemma_detail
        if len(l_d) != 1:
            return None
        else:
            gdr = l_d[0].get('gender', {}).get('female', None)
            return 'feminine' if gdr == True  else 'masculine' if gdr != None else None

    @StrProperty
    def plural(self) -> str:
        l_d = self.lemma_detail
        if len(l_d) != 1:
            return None
        else:
            plr = l_d[0].get('gender', {}).get('plural', None)
            return 'plural' if plr == True  else 'singular' if plr != None else None

    @ListProperty
    def infinitive(self) -> list:
        lst_inf = [detail.get('infinit', None) for detail in self.lemma_detail if detail.get('infinit', None)]
        return lst_inf 

    @StrProperty
    def mode(self) -> str:
        lst_mode = []
        for detail in self.lemma_detail:
            if 'mode' in detail:
                return detail['mode']
        return None

    @ListProperty
    def conjugate(self) -> list:
        lst = []
        for detail in self.lemma_detail:
            if 'conjugate' in detail or 'infinit' in detail:
                lst += [{'infinit': detail.get('infinit', None), **d} for d in detail.get('conjugate', [])]
        return lst

    @StrProperty
    def morphology(self) -> str:
        if self.data.get('lemmatizer', []):
            return transform_data(self.data['lemmatizer'], self.data['source'])
        else:
            return ''

    @StrProperty
    def dep(self) -> str:
        return self.data.get('dep', None)

    @StrProperty
    def ref(self) -> int:
        return self.data.get('ref', None)

    @ListProperty
    def meaning(self) -> list:
        return [(m.get('super', ''), m.get('sub', '')) for m in self.data.get('meaning', [])]

    def __format__(self, format_spec):
        return format(str(self), format_spec)
