from .Token import Token

class Span():

    __slots__ = ["ref_document", "sentence_idx", "tokens_idx", "cluster_idx"]

    def __init__(self, span_data, ref_document):
        """Class for coreference spans

        Args:
            span_data (dict): Span data containing sentence, tokens and cluster indexes. 
            ref_document (Document): Reference to the Document object.
        """        
        self.sentence_idx = span_data['sentence_index']
        self.tokens_idx = span_data['token_indexes']
        self.cluster_idx = span_data['cluster_index']
        self.ref_document = ref_document

    @property    
    def tokens(self) -> Token:
        return self.ref_document.sentences[self.sentence_idx].tokens[self.tokens_idx[0]: self.tokens_idx[-1] + 1]

    def __str__(self):
        return ' '.join([s.str for s in self.tokens])

    def __repr__(self):
        return str(self)

    def get_attributes(self, property):
        return [getattr(s, property) for s in self.tokens]