class Data():
	def __init__(self, data=None):
		self.data = data

	def get(self):
		return self.data

	def map(self, function=None):
		if callable(function) and isinstance(self.data, list) :
			for item in self.data:
				function(item)
			return True
		return False

	def getSentence(self, index=0):
		if not isinstance(self.data, type([])) or index >= len(self.data) or index < 0:
			return None
		return self.data[index]
