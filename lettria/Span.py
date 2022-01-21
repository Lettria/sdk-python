class Span():

    __slots__ = ["ref_document", "sentence_idx", "tokens_idx", "cluster_idx"]

    def __init__(self, span_data, ref_document):
        self.sentence_idx = span_data['sentence_index']
        self.tokens_idx = span_data['token_indexes']
        self.cluster_idx = span_data['cluster_index']
        self.ref_document = ref_document
    
    def __str__(self):
        return ' '.join(self.ref_document.sentences[self.sentence_idx].token[self.tokens_idx[0]: self.tokens_idx[-1] + 1])

    def __repr__(self):
        return str(self)