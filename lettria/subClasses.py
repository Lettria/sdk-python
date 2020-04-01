from .sharedClass import SharedClass, SharedClass_A
from .extractClass import ExtractClass
from .entitiesClass import *
from collections import Counter
from functools import reduce
import json

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

class ner_Analyzer(SharedClass_A, ExtractClass):
	""" NER class
	Provides access to entities subclasses and methods for data exploration.
	All sublasses implement print_formatted(), tolist() and todict() for data manipulation.
	"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'NER'
		self.define_entities()
		self.entities = {}
		for key in self.__dict__.keys():
			if key not in ['name', 'data', 'entities', 'document_level']:
				self.entities[key] = self.__dict__[key]
		self.scan_entities()

	def scan_entities(self):
		""" Create classes for non standard entities using Base_entity class."""
		for seq in self.data:
			for d in seq:
				if d['type'] and d['type'].lower() not in self.__dict__.keys():
					self.__dict__[d['type']] = Base_entity(d['type'], self.get_by_filter('type', d['type']), self.document_level)
					self.entities[d['type']] = self.__dict__[d['type']]

	def define_entities(self):
		""" Creates and assigns data to entities subclasses"""
		self.person =			Person(self.get_by_filter('type', 'PERSON'), self.document_level)
		self.location =			Location(self.get_by_filter('type', 'LOCATION'), self.document_level)
		self.date =			 	Date(self.get_by_filter('type', 'date'), self.document_level)
		self.distance =		 	Distance(self.get_by_filter('type', 'distance'), self.document_level)
		self.duration =		 	Duration(self.get_by_filter('type', 'duration'), self.document_level)
		self.frequency =		Frequency(self.get_by_filter('type', 'frequency'), self.document_level)
		self.interval =			Interval(self.get_by_filter('type', 'interval'), self.document_level)
		self.ip =			 	Ip(self.get_by_filter('type', 'ip'), self.document_level)
		self.ipv6 =			 	Ipv6(self.get_by_filter('type', 'ipv6'), self.document_level)
		self.mail =			 	Mail(self.get_by_filter('type', 'mail'), self.document_level)
		self.mass =			 	Mass(self.get_by_filter('type', 'mass'), self.document_level)
		self.mass_by_volume =   Mass_by_volume(self.get_by_filter('type', 'mass by volume'), self.document_level)
		self.mol =			  	Mol(self.get_by_filter('type', 'mol'), self.document_level)
		self.money =			Money(self.get_by_filter('type', 'money'), self.document_level)
		self.ordinal =		  	Ordinal(self.get_by_filter('type', 'ordinal'), self.document_level)
		self.percent =		  	Percent(self.get_by_filter('type', 'percent'), self.document_level)
		self.phone =			Phone(self.get_by_filter('type', 'phone'), self.document_level)
		self.pressure =		 	Pressure(self.get_by_filter('type', 'pressure'), self.document_level)
		self.set =			  	Set(self.get_by_filter('type', 'set'), self.document_level)
		self.speed =			Speed(self.get_by_filter('type', 'speed'), self.document_level)
		self.strength =		 	Strength(self.get_by_filter('type', 'strength'), self.document_level)
		self.surface =		  	Surface(self.get_by_filter('type', 'surface'), self.document_level)
		self.surface_tension =  Surface_tension(self.get_by_filter('type', 'surface tension'), self.document_level)
		self.temperature =	  	Temperature(self.get_by_filter('type', 'temperature'), self.document_level)
		self.time =			 	Time(self.get_by_filter('type', 'time'), self.document_level)
		self.url =			  	Url(self.get_by_filter('type', 'url'), self.document_level)
		self.voltage =		  	Voltage(self.get_by_filter('type', 'voltage'), self.document_level)
		self.volume =		   	Volume(self.get_by_filter('type', 'volume'), self.document_level)

	def list_entities(self, detail = False):
		""" Print all detected entities.
			Detail: Boolean. Shows most important information for each entity"""
		for key, val in self.entities.items():
			if val.data and not self.__check_empty(val.data):
				if not detail:
					print("{:10s}: {}".format(key.upper(), val.__repr__()))
				else:
					val.print_formatted()
					print('')

	def get_entities(self, return_empty = False):
		if return_empty:
			return {key.upper():val.__repr__() for key,val in self.entities.items()}
		else:
			return {key.upper():val.__repr__() for key,val in self.entities.items() if not self.__check_empty(val.data)}

	def print_formatted(self):
		self.list_entities(True)

	def __check_empty(self, data):
		if not data:
			return True
		for l in data:
			if l:
				return False
		return True

	def __getattribute__(self, key):
		"Emulate type_getattro() in Objects/typeobject.c"
		try:
			v = object.__getattribute__(self, key)
		except:
			_data = [d for d in self.data if d['type'] == key]
			if _data:
				self.__dict__[key] = Base_entity(key, _data)
				self.entities[key] = self.__dict__[key]
				v = object.__getattribute__(self, key)
			else:
				print('No entity of type: "' + key + '" has been found.')
				return ''
		if hasattr(v, '__get__'):
			return v.__get__(None, self)
		return v

class nlu_Analyzer(SharedClass_A, ExtractClass):
	""" Subclass for NLU key.
		Provides methods to manipulate categories.
	 """
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'NLU'

	def categories_unique(self, type='sub', id_sent = '', id_sub = ''):
		""" Returns a list of unique categories (sub or super)
		Sentence and subsentence index may be provided to limit the scope of the result"""
		cats = []
		if id_sub:
			start_id = id_sub['start_id'] if id_sub['start_id'] >= 0 else 0
			end_id = id_sub['end_id'] + 1
		if id_sent != '' and id_sent >= 0 and id_sent <= len(self.data):
			start_sent_id = id_sent
			end_sent_id = id_sent + 1
		else:
			start_sent_id = 0
			end_sent_id = len(self.data)
		if type not in ['sub', 'super']:
			print("Choose 'sub' or 'super' categories.")
			return []
		for sent in self.data[start_sent_id:end_sent_id]:
			tmp = []
			if not id_sub:
				start_id = 0
				end_id = len(sent)
			# print('\n===>',start_sent_id, end_sent_id, 's',start_id, 'e',end_id, 'len',len(sent))
			for d in sent[start_id:end_id]:
				for mean in d['meaning']:
					# print(mean)
					if mean and type in mean and mean[type]:
						tmp.append(mean[type])
			tmp = list(set(tmp))
			cats.append(tmp)
		if self.document_level:
			return list(set(reduce(lambda a,b : a + b, cats)))
		else:
			return cats

	def categories_count(self, type='sub'):
		""" Returns a dictionnary with categories and occurences as keys and values"""
		cats = []
		if type not in ['sub', 'super']:
			print("Choose 'sub' or 'super' categories.")
			return []
		for sent in self.data:
			tmp = {}
			for d in sent:
				for mean in d['meaning']:
					if mean and type in mean and mean[type]:
						tmp[mean[type]] = tmp.get(mean[type], 0) + 1
			cats.append(tmp)
		if self.document_level:
			return dict(reduce(lambda a,b: Counter(a) + Counter(b), cats))
		else:
			return cats

class nlp_Analyzer(SharedClass_A, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'NLP'

class sentiment_elements_Analyzer(SharedClass_A, ExtractClass):
	"""Subclass of sentiment for manipulation of elements"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

class sentiment_subsentences_Analyzer(SharedClass_A, ExtractClass):
	"""Subclass of sentiment for manipulation of subsentences"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

class sentiment_values_Analyzer(SharedClass_A, ExtractClass):
	"""Subclass of sentiment for manipulation of values"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

	def total(self):
		""" Merges the different sentiment values by document or by sentence"""
		if self.document_level:
			dico = {'total':0, 'negative':0, 'positive':0}
			for seq in self.data:
				if not seq:
					continue
				for d in seq:
					for k,v in d.items():
						dico[k] += v
			for k,v in dico.items():
				dico[k] = round(v, 4)
		else:
			dico = []
			for seq in self.data:
				if not seq:
					dico.append([])
					continue
				tmp = {'total':0, 'negative':0, 'positive':0}
				for d in seq:
					for k,v in d.items():
						tmp[k] += v
				for k,v in tmp.items():
					tmp[k] = round(v, 4)
				dico.append(tmp)
		return dico

	def mean(self):
		""" Calculates the average of the different sentiment values by document or by sentence"""
		if self.document_level:
			length = 0
			dico = {'total':0, 'negative':0, 'positive':0}
			for seq in self.data:
				if not seq:
					continue
				for d in seq:
					for k,v in d.items():
						dico[k] += v
					length += 1
			for k,v in dico.items():
				dico[k] = round(v / length + 1e-6, 3)
		else:
			dico = []
			for seq in self.data:
				if not seq:
					dico.append([])
					continue
				length = 0
				tmp = {'total':0, 'negative':0, 'positive':0}
				for d in seq:
					for k,v in d.items():
						tmp[k] += v
					length += 1
				for k,v in tmp.items():
					tmp[k] = round(v / length + 1e-6, 3)
				dico.append(tmp)
		return dico

	def average(self):
		self.mean()

	def tolist(self, force = ''):
		return self.format(self.data, force)

	def todict(self, force = ''):
		return self.tolist(force)

class sentiment_Analyzer(SharedClass_A, ExtractClass):
	""" Subclass for sentiment analysis
		Provides access to 3 subclasses, values, elements and subsentences and
		different methods to get sentences and their associated sentiment values."""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'sentiment'
		self.elements = sentiment_elements_Analyzer([d['elements'] if 'elements' in d else None for d in self.data], document_level)
		self.values = sentiment_values_Analyzer([[d['values']] if 'values' in d else None for d in self.data], document_level)
		self.subsentences = sentiment_subsentences_Analyzer([d['subsentences'] if 'subsentences' in d else None for d in self.data], document_level)

	def __str__(self):
		print(self.elements)
		print(self.subsentences)
		print(self.values)
		return ''

	def classify_sentences(self):
		""" Returns a dictionnary with classified sentences according to their
		given classes."""
		values = self.list_sentences_sentiments(force = 'document')
		res = {'positive':[], 'negative':[], 'neutral':[]}
		for seq in values:
			if seq and seq[1] == 0:
				res['neutral'].append(seq[0])
			elif seq and seq[1] > 0:
				res['positive'].append(seq[0])
			elif seq and seq[1] < 0:
				res['negative'].append(seq[0])
		return res

	def classify_subsentences(self):
		""" Returns a dictionnary with classified subsentences according to their
		given classes."""
		values = self.list_subsentences_sentiments(force = 'document')
		res = {'positive':[], 'negative':[], 'neutral':[]}
		for seq in values:
			if seq and seq[1] == 0:
				res['neutral'].append(seq[0])
			elif seq and seq[1] > 0:
				res['positive'].append(seq[0])
			elif seq and seq[1] < 0:
				res['negative'].append(seq[0])
		return res

	def print_subsentences_sentiments(self):
		print("{:120.120s} {:10}".format('Subsentence','Total value'))
		print('-' * 132)
		res = self.subsentences.todict(['sentence', 'values'])
		for r in res:
			if r:
				print("{:120.120} {:10}".format(r['sentence'], r['values']['total']))

	def list_subsentences_sentiments(self, force = ''):
		""" Returns list of subsentences with associated values"""
		res = self.subsentences.todict(['sentence', 'values'], force = 'sentence')
		return self.format([[[x['sentence'], x['values']['total']] for x in sub] for sub in res], force)

	def list_sentences_sentiments(self, force = ''):
		""" Returns list of sentences with associated values"""
		res = self.subsentences.todict(['sentence'], force='sentence')
		vals = self.values.todict(force = 'sentence')
		res = [[' '.join([x['sentence'] for x in sub]), val[0]['total']] if val else [' '.join([x['sentence'] for x in sub]), 0] for sub, val in zip(res, vals)]
		return res

	def tolist(self):
		return None

	def todict(self):
		return None

class emotion_Analyzer(SharedClass_A, ExtractClass):
	""" Emotion class, similar to sentiment class"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'emotions'
		self.elements = emotion_elements_Analyzer([d['elements'] if 'elements' in d else None for d in self.data], document_level)
		self.values = emotion_values_Analyzer([[d['values']] if 'values' in d else None for d in self.data], document_level)
		self.subsentences = emotion_subsentences_Analyzer([d['subsentences'] if 'subsentences' in d else None for d in self.data], document_level)
		self.colors = {
			'anger'		:'\033[31m',
			'happiness'	:'\033[32m',
			'surprise'	:'\033[33m',
			'sadness'	:'\033[34m',
			'disgust'	:'\033[35m',
			'fear'		:'\033[36m'
		}
		if self.data and self.data[0] and 'values' in self.data[0]:
			self.fields = list(self.data[0]['values'].keys())

	def __str__(self):
		print(self.elements)
		print(self.subsentences)
		print(self.values)
		return ''

	def list_subsentences_emotions(self, force = ''):
		""" Returns list of subsentences with associated values"""
		res = self.subsentences.todict(['sentence', 'values'], force = 'sentence')
		return self.format([[[x['sentence'], x['values']] for x in sub] for sub in res], force)

	def list_sentences_emotions(self, force = ''):
		""" Returns list of sentences with associated values"""
		res = self.subsentences.todict(['sentence'], force='sentence')
		vals = self.values.todict(force = 'sentence')
		res = [[' '.join([x['sentence'] for x in sub]), val[0]] if val else [' '.join([x['sentence'] for x in sub]), 0] for sub, val in zip(res, vals)]
		return res

	def classify_sentences(self):
		""" Returns a dictionnary with classified sentences according to their
		given classes."""
		values = self.list_sentences_emotions(force = 'document')
		print(values)
		res = {k:[] for k in self.fields}
		for seq in values:
			if seq and isinstance(seq[1], dict):
				for key in res.keys():
					if key in seq[1] and seq[1][key] > 0:
						res[key].append(seq[0])
		return res

	def classify_subsentences(self):
		""" Returns a dictionnary with classified subsentences according to their
		given classes."""
		values = self.list_subsentences_emotions(force = 'document')
		res = {k:[] for k in self.fields}
		for seq in values:
			if seq and isinstance(seq[1], dict):
				for key in res.keys():
					if key in seq[1] and seq[1][key] > 0:
						res[key].append(seq[0])
		return res

	def print_subsentences_emotions(self):
		print("{:100.100s}".format('Subsentence'), end = '\t')
		for k in ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']:
			print("{:9}".format(k), end = '\t')
		print('\n', '-' * 190)
		res = self.subsentences.todict(['sentence', 'values'])
		for r in res[:]:
			print("{:100.100}".format(r['sentence'], r['values']), end = '\t')
			for k,v in r['values'].items():
				if v == 0:
					print('{:9.4s}'.format(''), end = '\t')
				else:
					if k in self.colors:
						print(self.colors[k], end = '')
					print('{:9.4f}'.format(v), end = '\t')
					print('\033[0m', end = '')
			print('')

class emotion_elements_Analyzer(SharedClass_A, ExtractClass):
	"""Subclass of emotion for manipulation of elements"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

class emotion_subsentences_Analyzer(SharedClass_A, ExtractClass):
	"""Subclass of emotion for manipulation of subsentences"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

class emotion_values_Analyzer(SharedClass_A, ExtractClass):
	"""Subclass of emotion for manipulation of values"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		if self.data and self.data[0]:
			self.fields = list(self.data[0][0].keys())

	def total(self):
		""" Merges the different emotion values by document or by sentence"""
		if self.document_level:
			dico = {k:0 for k in self.fields}
			for seq in self.data:
				if not seq:
					continue
				for d in seq:
					for k,v in d.items():
						dico[k] += v
			for k,v in dico.items():
				dico[k] = round(v, 4)
		else:
			dico = []
			for seq in self.data:
				if not seq:
					dico.append([])
					continue
				tmp = {k:0 for k in self.fields}
				for d in seq:
					for k,v in d.items():
						tmp[k] += v
				for k,v in tmp.items():
					tmp[k] = round(v, 4)
				dico.append(tmp)
		return dico

	def mean(self):
		""" Calculates the average of the different emotion values by document or by sentence"""
		if self.document_level:
			length = 0
			dico = {k:0 for k in self.fields}
			for seq in self.data:
				if not seq:
					continue
				for d in seq:
					for k,v in d.items():
						dico[k] += v
					length += 1
			for k,v in dico.items():
				dico[k] = round(v / length + 1e-6, 3)
		else:
			dico = []
			for seq in self.data:
				if not seq:
					dico.append([])
					continue
				length = 0
				tmp = {k:0 for k in self.fields}
				for d in seq:
					for k,v in d.items():
						tmp[k] += v
					length += 1
				for k,v in tmp.items():
					tmp[k] = round(v / length + 1e-6, 3)
				dico.append(tmp)
		return dico

	def average(self):
		return self.mean()

	def tolist(self, force = ''):
		return self.format(self.data, force)

	def todict(self, force = ''):
		return self.tolist(force)

class emoticons_Analyzer(SharedClass_A, ExtractClass):
	""" Subclass for emoticons"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'emoticons'

	def todict(self, fields=None):
		if isinstance(fields, str):
			fields = [fields]
		if not fields:
			return self.format(self.data)
		else:
			return self.format([{k:v for k,v in seq.items() if k in fields} for seq in self.data])

	def tolist(self):
		return self.format([k for k,v in self.todict().items() if v > 0])

	def format(self, data):
		if self.document_level:
			emots = {k:0 for k in data[0].keys() if data[0]}
			for d in data:
				for k,v in d.items():
					if v > 0:
						emots[k] += v
			return emots
		else:
			return data

class parser_dependency_Analyzer(SharedClass_A, ExtractClass):
	""" Subclass for parser_dependency"""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'parser_dependency'

	def getByRole(self, role):
		return self.get_by_filter('dep', role)

	def get_dep_of_source(self, word, return_empty = True, filter_tag = [], \
			return_category = False, return_lemma = False):
		"""
		Takes a token as input and retrieves the tokens that have the token as a reference.
		return_empty : Boolean. Returns empty list if no match in a sentence.
		filter_tag : List of string. List of tags to filter results with.
		return_lemma : Boolean. Returns lemmatized tokens instead of original input.
		return_category : Boolean. Returns category of tokens instead of original input.
		"""
		word = [word] if isinstance(word, str) else word
		idx = [[v['index'] for v in seq if v['source'] in word] for seq in self.data]
		type = 'lemma' if return_lemma else 'source'
		if filter_tag and isinstance(filter_tag, list):
			if return_category:
				words = [{v[type]:self.__flatten_meaning(v['meaning'], 'sub') for v in seq \
					if v['ref'] in id and v['tag'] in filter_tag} for seq, id in zip(self.data, idx)]
			else:
				words = [[v[type] for v in seq \
					if v['ref'] in id and v['tag'] in filter_tag] for seq, id in zip(self.data, idx)]
		else:
			if return_category:
				words = [{v[type]:self.__flatten_meaning(v['meaning'], 'sub') for v in seq \
					if v['ref'] in id} for seq, id in zip(self.data, idx)]
			else:
				words = [[v[type] for v in seq if v['ref'] in id] for seq, id in zip(self.data, idx)]
		if return_empty:
			return self.format(words)
		else:
			return self.format([x for x in words if x])

	def get_dep_of_category(self, category, return_empty = True, filter_tag = [],\
	 		return_lemma = False):
		"""
		Takes a category as input and retrieves the tokens that have the category as a reference.
		return_empty : Boolean. Returns empty list if no match in a sentence.
		filter_tag : List of string. List of tags to filter results with.
		return_lemma : Boolean. Returns lemmatized tokens instead of original input.
		"""
		category = [category] if isinstance(category, str) else category
		idx = [[v['index'] for v in seq if self.__match_meaning(v['meaning'], category)] for seq in self.data]
		type = 'lemma' if return_lemma else 'source'
		if filter_tag and isinstance(filter_tag, list):
			words = [[v[type] for v in seq if v['ref'] in id and v['tag'] in filter_tag] for seq, id in zip(self.data, idx)]
		else:
			words = [[v[type] for v in seq if v['ref'] in id] for seq, id in zip(self.data, idx)]
		if return_empty:
			return self.format(words)
		else:
			return self.format([x for x in words if x])

	def __flatten_meaning(self, data, type = 'sub'):
		lst = []
		if type not in ['sub', 'super']:
			return []
		for elem in data:
			if elem and elem[type]:
				lst.append(elem[type])
		return lst

	def __match_meaning(self, data, category, type = 'sub'):
		if type not in ['sub', 'super']:
			return False
		for elem in data:
			if elem and elem[type] in category:
				return True
		return False

class postagger_Analyzer(SharedClass_A):
	""" Subclass for postagger key.
		Allows filtering (include/exclude) and easy extraction of information."""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'postagger'

	def get_by_tag(self, tag):
		"""  Filtering: include
		Returns tuple (source, tag)"""
		data = self.tolist(True, True)
		r = []
		if data:
			for seq in data:
				tmp = []
				for item in seq:
					if isinstance(tag, list):
						if item[1] in tag:
							tmp.append(item)
					else:
						if item[1] == tag:
							tmp.append(item)
				tmp.append(r)
		return self.format(r)

	def get_by_tag_exclude(self, tag):
		"""  Filtering: exclude
			Returns tuple (source, tag)"""
		data = self.tolist(True, True)
		r = []
		if data:
			for seq in data:
				tmp = []
				for item in seq:
					if isinstance(tag, list):
						if item[1] not in tag:
							tmp.append(item)
					else:
						if item[1] != tag:
							tmp.append(item)
				r.append(tmp)
		return self.format(r)

	def tolist(self, tuple = False, force = ''):
		if not tuple:
			return self.format([[d[1] for d in seq] for seq in self.data], force)
		else:
			return self.format([[(d[0], d[1]) for d in seq] for seq in self.data], force)

	def fields(self):
		string = self.name.capitalize() + " fields. List of tuples (SOURCE, TAG):\n"
		string += json.dumps([('je', 'CLS'), ('ai', 'V'), ('mange', 'VP'), ('un', 'CD'), ('sandwich', 'N'), ('.', 'PUNCT')], indent=4)
		return string

class sentence_acts_Analyzer(SharedClass_A, ExtractClass):
	""" Subclass fo sentence_acts key.
		Sentence_act classifies the sentence between question, assertion etc."""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'sentence_acts'
		# print(self.data)

	def format(self, data, force = ''):
		if force == 'document' or self.document_level:
			tmp = []
			for d in data:
				if d:
					tmp.append(d[0])
				else:
					tmp.append([])
			return tmp
		else:
			return data


class coreference_Analyzer(SharedClass_A, ExtractClass):
	""" Subclass fo coreference object."""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'coreference'

class synthesis_Analyzer(SharedClass_A, ExtractClass):
	""" Subclass for synthesis key.
		Synthesis regroups key information for each token."""
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'synthesis'

from collections import Counter, OrderedDict

class utils():
	def __init__(self):
		pass

	def count_sort(self, data, reverse = True):
		data = OrderedDict(sorted(Counter(data).items(), key = lambda v: v[1], reverse = reverse))
		return data
