from .subClasses import *
import functools
import collections

class Analyzer:
    def __init__(self, client = None, data = None):
        self.client = client
        self.data = data
        self.result = []
        self.sentence_number = 0

    def request(self, document = None):
        if not self.client:
            self.missing_client()
            return
        if not document:
            if self.data:
                document = self.data
            else:
                return
        try:
            if isinstance(document, list):
                for seq in document:
                    self.result += self.client.request(seq, raw=True)
            else:
                self.result += self.client.request(document, raw=True)
        except Exception as e:
            print(e)
            pass

    def missing_client(self):
        print('Please assign a client in order to make a request.')

    def analyze_sentence(self):
        if not self.result:
            print('No data to analyze')
        else:
            self.analyze(False)

    def analyze_document(self):
        if not self.result:
            print('No data to analyze')
        else:
            self.analyze(True)

    def analyze(self, document_level):
        # self.ner = ner([[sub for sub in d['NER']] for d in self.result if 'NER' in d], document_level)
        self.postagger = postagger([[sub for sub in d['postagger']] for d in self.result if 'postagger' in d], document_level)
        self.emoticons = emoticons(self.concat_emoticons(document_level), document_level)
        self.parser_dependency = parser_dependency([[sub for sub in d['parser_dependency']] for d in self.result if 'parser_dependency' in d], document_level)
        self.nlp = nlp([[sub for sub in d['NLP']] for d in self.result if 'NLP' in d], document_level)
        # self.nlu = nlu(data['NLU']) if data and 'NLU' in data else None
        # self.emotion = sentiment(data['emotion']) if data and 'emotion' in data else None
        self.sentiment = sentiment([{sub:v for sub,v in d['sentiment'].items()} for d in self.result if 'sentiment' in d], document_level)
        # self.sentence_acts = sentence_acts(data['sentence_acts']) if data and 'sentence_acts' in data else None
        # self.coreference = coreference(data['coreference']) if data and 'coreference' in data else None
        # self.synthesis = synthesis([[sub for sub in d['synthesis']] for d in self.result if 'synthesis' in d], document_level)
        # self.synthesis = synthesis([sub for d in self.result if 'synthesis' in d for sub in d['synthesis']])
        # self.lemma = [d['lemma'] for d in self.synthesis]

    def concat_emoticons(self, document_level):
        self.emoticons = [[d['emoticons']['emoticon']] for d in self.result if 'emoticons' in d]
        lst_emots = []
        for seq in self.emoticons:
            emots = {k:0 for k in seq[0].keys() if seq[0]}
            for d in seq:
                for k,v in d.items():
                    if v > 0:
                        emots[k] += v
            lst_emots.append(emots)
        return lst_emots

    def flatten(arg):
        pass
