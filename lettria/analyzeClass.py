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

    def analyze_document(self):
        if not self.result:
            print('No data to analyze')
            return
        # [d['emoticons']['emoticon'] for d in self.result if 'emoticons' in d])
        self.ner = ner([sub for d in self.result if 'NER' in d for sub in d['NER']])
        self.postagger = postagger([sub for d in self.result if 'postagger' in d for sub in d['postagger']])
        self.emoticons = emoticons(self.concat_emoticons())
        self.parser_dependency = parser_dependency([sub for d in self.result if 'parser_dependency' in d for sub in d['parser_dependency']])
        # self.nlu = nlu(data['NLU']) if data and 'NLU' in data else None
        # self.nlp = nlp(data['NLP']) if data and 'NLP' in data else None
        # self.emotion = sentiment(data['emotion']) if data and 'emotion' in data else None
        # self.sentiment = sentiment(data['sentiment']) if data and 'sentiment' in data else None
        # self.emoticons = emoticons(data['emoticons']) if data and 'emoticons' in data else None
        # self.sentence_acts = sentence_acts(data['sentence_acts']) if data and 'sentence_acts' in data else None
        # self.coreference = coreference(data['coreference']) if data and 'coreference' in data else None
        # self.data_synthesis = data['synthesis'] if data and 'synthesis' in data else None

    def concat_emoticons(self):
        self.emoticons = [d['emoticons']['emoticon'] for d in self.result if 'emoticons' in d]
        emots = {k:0 for k in self.emoticons[0].keys() if self.emoticons[0]}
        for d in self.emoticons:
            for k,v in d.items():
                if v > 0:
                    emots[k] += v
        return emots

    def flatten(arg):
        pass
