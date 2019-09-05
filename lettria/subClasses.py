from .sharedClass import SharedClass
from .extractClass import ExtractClass

class ner(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class nlu(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class nlp(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class sentiment_elements(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class sentiment_values(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class sentiment(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.elements = sentiment_elements(data['elements']) if 'elements' in data else None
		self.values = sentiment_values(data['values']) if 'values' in data else None

class emotion_elements(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class emotion_values(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class emotion(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.elements = emotion_elements(data['elements']) if 'elements' in data else None
		self.values = emotion_values(data['values']) if 'values' in data else None

class emoticons(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

	def get_confidence(self):
		r = []
		if self.data and 'confidence' in self.data:
			return self.data['confidence']
		return None

	def get_present(self):
		r = []
		if self.data and 'emoticon' in self.data:
			for k in self.data['emoticon']:
				if self.data['emoticon'][k]:
					r.append(k)
		return r

class parser_dependency(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

	def getByRole(self, role):
		return self.get_by_filter('dep', role)

class postagger():
	def __init__(self, data=None):
		self.data = data

	def get(self):
		return self.data

	def get_by_tag(self, tag):
		r = []
		if self.data:
			for item in self.data:
				if isinstance(tag, list):
					if item[1] in tag:
						r.append(item)
				else:
					if item[1] == tag:
						r.append(item)
		return r

class sentence_acts(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class coreference(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
