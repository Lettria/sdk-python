from .sharedClass import SharedClass
from .extractClass import ExtractClass
from .entitiesClass import *
from collections import Counter
from functools import reduce
import json

class ner(SharedClass, ExtractClass):
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
		for seq in self.data:
			for d in seq:
				if d['type'].lower() not in self.__dict__.keys():
					self.__dict__[d['type']] = Base_entity(d['type'], self.get_by_filter('type', d['type']), self.document_level)
					self.entities[d['type']] = self.__dict__[d['type']]

	def define_entities(self):
		self.person =			Person(self.get_by_filter('type', 'PERSON'), self.document_level)
		self.location =			Location(self.get_by_filter('type', 'LOCATION'), self.document_level)
		self.date =			 	Date(self.get_by_filter('type', 'date'), self.document_level)
		self.distance =		 	Distance(self.get_by_filter('type', 'distance'), self.document_level)
		self.duration =		 	Duration(self.get_by_filter('type', 'duration'), self.document_level)
		# self.electric_power =   Electric_power(self.get_by_filter('type', 'electric power'), self.document_level)
		# self.hex_color =		Hex_color(self.get_by_filter('type', 'hex color'), self.document_level)
		self.frequency =		Frequency(self.get_by_filter('type', 'frequency'), self.document_level)
		self.interval =			Interval(self.get_by_filter('type', 'interval'), self.document_level)
		self.ip =			 	Ip(self.get_by_filter('type', 'ip'), self.document_level)
		self.ipv6 =			 	Ipv6(self.get_by_filter('type', 'ipv6'), self.document_level)
		# self.light_intensity =  Light_intensity(self.get_by_filter('type', 'light intensity'), self.document_level)
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
		for key, val in self.entities.items():
			if val.data and not self.check_empty(val.data):
				if not detail:
					print("{:10s}: {}".format(key.upper(), val.__repr__()))
				else:
					val.print_formatted()
					print('')

	def get_entities(self, return_empty = False):
		if return_empty:
			return {key.upper():val.__repr__() for key,val in self.entities.items()}
		else:
			return {key.upper():val.__repr__() for key,val in self.entities.items() if not self.check_empty(val.data)}

	def print_formatted(self):
		self.list_entities(True)

	def check_empty(self, data):
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

class nlu(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'NLU'

	def categories_unique(self, type='sub', id_sent = '', id_sub = ''):
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

class nlp(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'NLP'

class sentiment_elements(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

class sentiment_subsentences(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

class sentiment_values(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

	def total(self):
		if self.document_level:
			dico = {'total':0, 'negative':0, 'positive':0}
			for seq in self.data:
				for d in seq:
					for k,v in d.items():
						dico[k] += v
		else:
			dico = []
			for seq in self.data:
				tmp = {'total':0, 'negative':0, 'positive':0}
				for d in seq:
					for k,v in d.items():
						tmp[k] += v
				dico.append(tmp)
		return dico

	def mean(self):
		if self.document_level:
			length = 0
			dico = {'total':0, 'negative':0, 'positive':0}
			for seq in self.data:
				for d in seq:
					for k,v in d.items():
						dico[k] += v
					length += 1
			for k,v in dico.items():
				dico[k] = round(v / length + 1e-6, 3)
		else:
			dico = []
			for seq in self.data:
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

	def tolist(self, force_sentence = False):
		return self.format(self.data, force_sentence)

	def todict(self, force_sentence = False):
		return self.tolist(force_sentence)

class sentiment(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		# for d in data:
		# 	print(d)
		super().__init__(data, document_level)
		self.name = 'sentiment'
		self.elements = sentiment_elements([d['elements'] if 'elements' in d else None for d in self.data], document_level)
		self.values = sentiment_values([[d['values']] if 'values' in d else None for d in self.data], document_level)
		self.subsentences = sentiment_subsentences([d['subsentences'] if 'subsentences' in d else None for d in self.data], document_level)

	def __str__(self):
		print(self.elements)
		print(self.subsentences)
		print(self.values)
		return ''

	def subsentences_sentiments(self):
		print("{:120.120s} {:10}".format('Subsentence','Total value'))
		print('-' * 132)
		res = self.subsentences.todict(['sentence', 'values'])
		for r in res:
			# print(r)
			print("{:120.120} {:10}".format(r['sentence'], r['values']['total']))

class emotion_elements(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

class emotion_values(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)

class emotion(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'emotions'
		self.elements = emotion_elements(data['elements']) if 'elements' in data else None
		self.values = emotion_values(data['values']) if 'values' in data else None

class emoticons(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'emoticons'

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

class parser_dependency(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'parser_dependency'

	def getByRole(self, role):
		return self.get_by_filter('dep', role)

	# def tolist(self, tuple = False, force_sentence = False):
	# 	if not tuple:
	# 		return self.format([[sub['dep'] for sub in d] for d in self.data], force_sentence)
	# 	else:
	# 		return self.format([[(sub['source'], sub['dep']) for sub in d] for d in self.data], force_sentence)

class postagger(SharedClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'postagger'

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
	def tolist(self, tuple = False):
		if not tuple:
			return self.format([[d[1] for d in seq] for seq in self.data])
		else:
			return self.format([[(d[0], d[1]) for d in seq] for seq in self.data])

	def fields(self):
		string = self.name.capitalize() + " fields. List of tuples (SOURCE, TAG):\n"
		string += json.dumps([('je', 'CLS'), ('ai', 'V'), ('mange', 'VP'), ('un', 'CD'), ('sandwich', 'N'), ('.', 'PUNCT')], indent=4)
		return string

class sentence_acts(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'sentence_acts'
		# print(self.data)

	def format(self, data, force_sentence = ''):
		if not force_sentence and self.document_level:
			tmp = []
			for d in data:
				if d:
					tmp.append(d[0])
				else:
					tmp.append([])
			print('format',len(tmp))
			return tmp
		else:
			return data


class coreference(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'coreference'

class synthesis(SharedClass, ExtractClass):
	def __init__(self, data=None, document_level = True):
		self.data = data
		super().__init__(data, document_level)
		self.name = 'synthesis'
