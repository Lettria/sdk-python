from .sharedClass import SharedClass
from .extractClass import ExtractClass
from .subClasses import *

class Sentence(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.ner = ner(data['NER']) if data and 'NER' in data else None
		self.nlu = nlu(data['NLU']) if data and 'NLU' in data else None
		self.nlp = nlp(data['NLP']) if data and 'NLP' in data else None
		self.sentiment = sentiment(data['Sentiment']) if data and 'Sentiment' in data and 'list' in data['Sentiment'] else None
		self.emoticons = emoticons(data['emoticons']) if data and 'emoticons' in data else None
		self.parser_dependency = parser_dependency(data['parser_dependency']) if data and 'parser_dependency' in data else None
		self.postagger = postagger(data['postagger']) if data and 'postagger' in data else None
		self.sentence_acts = sentence_acts(data['sentence_acts']) if data and 'sentence_acts' in data else None
		self.coreference = coreference(data['coreference']) if data and 'coreference' in data else None
		self.data_global = data['global'] if data and 'global' in data else None

	def getByFilter(self, key, value, list=None):
		r = []
		l = list if list else self.data_global
		if not isinstance(l, type([])):
			return None
		for item in l:
			try:
				if '.' in key:
					if self.getNested(key, item) == value:
						r.append(item)
				else:
					if item[key] == value:
						r.append(item)
			except:
				pass
		return r
