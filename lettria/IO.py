from .NLP import NLP
import jsonlines as jsonl

class JSONLReader:
    def __init__(self, path, chunksize = 1):
        self.path = path
        self.chunksize = chunksize
        try:
            self.io = jsonl.open(path, 'r')
            self.io_iter = self.io.iter()
        except Exception as e:
            print("Failed to open file " + str(path) + ": " + str(e))
            self.io = None
        self.io_over = False

    def __iter__(self):
        self.nrows = 0
        return self

    def __next__(self):
        if self.io_over:
            raise StopIteration
        i = 0
        nlp = NLP()
        while i < self.chunksize:
            try:
                line = next(self.io_iter)
                nlp.add_document_data(line.get('data'), id=line.get('document_id', None))
            except StopIteration:
                self.io_over = True
                self.io.close()
                if i == 0:
                    raise StopIteration
                else:
                    return nlp
            i+=1
        return nlp

def load_result(self, *args):
    """ Alias for load_results"""
    load_results(*args)

def load_results(path = 'results_0', reset = False, chunksize = None):
    """ Loads result from a valid json file."""
    if not (path.endswith('.json') or path.endswith('.jsonl')):
        path = path + '.jsonl'
    nlp = NLP()
    if not (isinstance(chunksize, int) and chunksize >= 1):
        try:
            if reset:
                self.reset_data()
            if path.endswith('jsonl'):
                with jsonl.open(path, 'r') as f:
                    for line in f:
                        nlp.add_document_data(line.get('data'), id=line.get('document_id', None))
            elif path.endswith('json'):
                with open(path, 'r') as f:
                    result = json.load(f)
                    if isinstance(result, dict):
                        assert len(result.get('document_ids', [])) == len(result.get('documents', [])), \
                                "'document_ids' and 'documents' should be of similar length"
                        for id_, r in zip(result['document_ids'], result['documents']):
                            nlp.add_document_data(r, id=id_)
                    else:
                        for r in result:
                            nlp.add_document_data(r)
            print(f'Loaded {path} successfully')
        except Exception as e:
            print('Failure to load ' + str(path) + ': ')
            print(e, '\n')
    else:
        if not path.endswith('jsonl'):
            print("chunk loading only avaiable with jsonl files.")
            return None
        return JSONLReader(path, chunksize)
    return nlp