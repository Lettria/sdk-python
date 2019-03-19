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

class sentiment_list(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class sentiment_group(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class sentiment(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.list = sentiment_list(data['list']) if 'list' in data else None
		self.group = sentiment_group(data['group']) if 'group' in data else None

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
		return self.getByFilter('dep', role)

class postagger():
	def __init__(self, data=None):
		self.data = data

	def get(self):
		return self.data

	def getByTag(self, tag):
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
