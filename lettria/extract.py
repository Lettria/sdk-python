class Extract:
	def __init__(self, key=None):
		None
	def rd(self, json, where):
		if json and where and where in json:
			return json['NLP']
		else:
			return None
	def NLP(self, json):
		return self.rd(json, 'NLP')
	def NER(self, json):
		return self.rd(json, 'NER')
	def NLU(self, json):
		return self.rd(json, 'NLU')
	def Sentiment(self, json):
		return self.rd(json, 'Sentiment')
	def emoticons(self, json):
		return self.rd(json, 'emoticons')
	def language_used(self, json):
		return self.rd(json, 'language_used')
	def postagger(self, json):
		return self.rd(json, 'postagger')
	def tokenizer(self, json):
		if json and 'postagger' in json:
			p = [ item[0] for item in json['postagger']]
		else:
			return None
		return p
	def Entities_numeral(self, json):
		if json and 'Entities_numeral' in json:
			return json['Entities_numeral']
		else:
			return None
	def parser_dependency(self, json):
		if json and 'parser_dependency' in json:
			return json['parser_dependency']
		else:
			return None
	def get_from_tag(self, json, tag):
		print("JSON")
		print(json['NLP'])
		res = []
		if json and 'NLP' in json:
			for item in json['NLP']:
				if 'tag' in item and item['tag'] == tag:
					res.append(item)
		return res
	def get_verbs(self, json):
		return self.get_from_tag(json, 'VP') + self.get_from_tag(json, 'V') + self.get_from_tag(json, 'VINF')
	def get_nouns(self, json):
		return self.get_from_tag(json, 'N')
	def get_proper_nouns(self, json):
		return self.get_from_tag(json, 'NP')
	def get_adjective(self, json):
		return self.get_from_tag(json, 'JJ')
	def get_numerals(self, json):
		return self.get_from_tag(json, 'CD')
	def get_adverbs(self, json):
		return self.get_from_tag(json, 'RB')
	def get_cls(self, json):
		return self.get_from_tag(json, 'RB')
	def get_clo(self, json):
		return self.get_from_tag(json, 'RB')
	def get_prepositions(self, json):
		return self.get_from_tag(json, 'P')
