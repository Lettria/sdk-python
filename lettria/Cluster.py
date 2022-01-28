from .Span import Span

hierarchy_pos_cluster = ['NP', ['PD','N'], ['D', 'N'], 'N', 'CLS', 'CLO', 'PRON', 'D', 'PROREL', 'PD', 'P', 'ENTITY'] 

class Cluster():
    __slots__ = ["cluster_idx", "spans_idx", "ref_document", "spans", "n"]

    def __init__(self, cluster_idx, spans_idx, ref_document):
        """
        Class for coreference cluster.
        Args:
            cluster_idx (int): Index of the cluster in the document.
            spans_idx (List): Indexes of the spans of the cluster.
            ref_document (Document): Reference to the Document object
        """
        self.spans_idx = spans_idx
        self.cluster_idx = cluster_idx
        self.ref_document = ref_document
        self.spans = [Span(self.ref_document.document_data.get('coreference', {}).get('spans', {})[span_idx], ref_document) for span_idx in self.spans_idx]
        
    def __str__(self):
        return ', '.join([str(span) for span in self.spans])

    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.spans):
            self.n += 1
            return self.spans[self.n - 1]
        else:
            raise StopIteration
    
    @property
    def head(self) -> Span:
        """Returns the head of a cluster, which is the span that best represent the cluster.
        This is done according to a hierarchy that use the POS tags inside the spans.

        Returns:
            Span: Span of the head of the cluster
        """
        for h in hierarchy_pos_cluster:
            if isinstance(h, list):
                match = [s for s in self.spans if set(h) & set(s.get_attributes('pos')) == set(h)]
            else:
                match = [s for s in self.spans if h in s.get_attributes('pos')]
            if match:
                return match[0]
        return self.spans[0]

    @property
    def children(self) -> list:
        """Returns the children of the cluster, i.e. all spans except head.
        Returns:
            list: list of children spans.
        """
        head = self.head
        return [span for span in self.spans if span != head]