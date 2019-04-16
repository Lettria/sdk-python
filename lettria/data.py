class Data():
	def __init__(self, data=None):
		self.data = data
		self.sentences = data
		self.lastIndex = -1

	def get(self):
		return self.data

	def map(self, function=None):
		if callable(function) and isinstance(self.data, list) :
			for item in self.data:
				function(item)
			return True
		return False

	def get_sentence(self, index=None):
		if index is not None:
			self.lastIndex = index
		else:
			index = self.lastIndex + 1
			self.lastIndex = index
		if not isinstance(self.data, type([])) or index >= len(self.data) or index < 0:
			return None
		return self.data[index]

	def get_number_of_sentences(self):
		if not self.data:
			return 0
		return len(self.data)
