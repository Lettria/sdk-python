from .Span import Span

class Cluster():

    __slots__ = ["cluster_idx", "spans_idx", "ref_document", "spans"]

    def __init__(self, cluster_idx, spans_idx, ref_document):
        self.spans_idx = spans_idx
        self.cluster_idx = cluster_idx
        self.ref_document = ref_document
        self.spans = [Span(self.ref_document.document_data.get('coreference', {}).get('spans', {})[span_idx], ref_document) for span_idx in self.spans_idx]
    
    def __str__(self):
        return ', '.join([str(span) for span in self.spans])

    def __repr__(self):
        return str(self)