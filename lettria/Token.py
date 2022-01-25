from .utils import StrProperty, ListProperty, DictProperty

class Token:
    __slots__ = ("data", "idx", "pure_source", "ref_sentence")

    def __init__(self, data, idx, pure_source, ref_sentence):
        self.data = data
        self.idx = idx
        self.pure_source = pure_source
        self.ref_sentence = ref_sentence

    def __repr__(self):
        return self.str

    def __str__(self):
        return self.data.get('source', None)

    @StrProperty
    def token(self):
        return self.data.get('source', None)

    @StrProperty
    def original_text(self):
        idx = self.data.get('source_indexes', None)
        if idx and len(idx) == 2:
            return self.pure_source[idx[0]:idx[1]]
        else:
            return self.token

    @StrProperty
    def source(self):
        return self.data.get('source', None)

    @StrProperty
    def str(self):
        return self.data.get('source', None)

    @StrProperty
    def pos(self):
        return self.data.get('tag', None)

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

    @ListProperty
    def spans(self):
        if self.data.get('coreference', []):
            return [span for span in self.ref_sentence.spans if self.idx in span.tokens_idx]
        return []

    @ListProperty
    def clusters(self):
        if self.data.get('coreference', []):
            return [cluster for cluster in self.ref_sentence.clusters if set(cluster.spans_idx) & set(self.data.get('coreference'))]
        return []

    @StrProperty
    def lemma(self):
        return self.data.get('lemma', None)

    @ListProperty
    def lemma_detail(self):
        if 'lemmatizer' in self.data:
            if isinstance(self.data['lemmatizer'], list):
                return self.data['lemmatizer']
            elif isinstance(self.data['lemmatizer'], dict):
                return [self.data['lemmatizer']]
        else:
            return []

    @DictProperty
    def auxiliary(self):
        return self.data.get('auxiliary', {})

    @StrProperty
    def gender(self):
        l_d = self.lemma_detail
        if len(l_d) != 1:
            return None
        else:
            gdr = l_d[0].get('gender', {}).get('female', None)
            return 'feminine' if gdr == True  else 'masculine' if gdr != None else None

    @StrProperty
    def plural(self):
        l_d = self.lemma_detail
        if len(l_d) != 1:
            return None
        else:
            plr = l_d[0].get('gender', {}).get('plural', None)
            return 'plural' if plr == True  else 'singular' if plr != None else None

    @ListProperty
    def infinitive(self):
        lst_inf = [detail.get('infinit', None) for detail in self.lemma_detail if detail.get('infinit', None)]
        return lst_inf 

    @StrProperty
    def mode(self):
        lst_mode = []
        for detail in self.lemma_detail:
            if 'mode' in detail:
                return detail['mode']
        return None

    @ListProperty
    def conjugate(self):
        lst = []
        for detail in self.lemma_detail:
            if 'conjugate' in detail or 'infinit' in detail:
                lst += [{'infinit': detail.get('infinit', None), **d} for d in detail.get('conjugate', [])]
        return lst

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
        return [(m.get('super', ''), m.get('sub', '')) for m in self.data.get('meaning', [])]

    def __format__(self, format_spec):
        return format(str(self), format_spec)
