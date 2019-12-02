from .sharedClass import SharedClass
from .extractClass import ExtractClass
from .entitiesClass import *
import json

class ner(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data =	data
		self.name = 'NER'
		self.define_entities()
		# self.entities = {
		# 	'person':self.person,
		# 	'location':self.location,
		# 	'date' : self.date,
		# 	'distance' : self.distance,
		# 	'duration' : self.duration,
		# 	'electric_power' : self.electric_power,
		# 	'hex_color' : self.hex_color,
		# 	'frequency' : self.frequency,
		# 	'interval' : self.interval,
		# 	'ip' : self.ip,
		# 	'ipv6' : self.ipv6,
		# 	'light_intensity' : self.light_intensity,
		# 	'mail' : self.mail,
		# 	'mass' : self.mass,
		# 	'mass_by_volume' : self.mass_by_volume,
		# 	'mol' : self.mol,
		# 	'money' : self.money,
		# 	'ordinal' : self.ordinal,
		# 	'percent' : self.percent,
		# 	'phone' : self.phone,
		# 	'pressure' : self.pressure,
		# 	'set' : self.set,
		# 	'speed' : self.speed,
		# 	'strength' : self.strength,
		# 	'surface' : self.surface,
		# 	'surface_tension' : self.surface_tension,
		# 	'temperature' : self.temperature,
		# 	'time' : self.time,
		# 	'url' : self.url,
		# 	'voltage' : self.voltage,
		# 	'volume' : self.volume
		# 	}
		self.entities = {}
		for key in self.__dict__.keys():
			if key not in ['name', 'data', 'entities']:
				self.entities[key] = self.__dict__[key]
		# print(self.__dict__.keys())
		# print(self.date)
		# print(self.entities['speed'])

	def define_entities(self):
		self.person =			Person(self.get_by_filter('type', 'PERSON'))
		self.location =			Location(self.get_by_filter('type', 'LOCATION'))
		self.date =             Date(self.get_by_filter('type', 'date'))
		self.distance =         Distance(self.get_by_filter('type', 'distance'))
		self.duration =         Duration(self.get_by_filter('type', 'duration'))
		self.electric_power =   Electric_power(self.get_by_filter('type', 'electric power'))
		self.hex_color =        Hex_color(self.get_by_filter('type', 'hex color'))
		self.frequency =        Frequency(self.get_by_filter('type', 'frequency'))
		self.interval =         Interval(self.get_by_filter('type', 'interval'))
		self.ip =               Ip(self.get_by_filter('type', 'ip'))
		self.ipv6 =             Ipv6(self.get_by_filter('type', 'ipv6'))
		self.light_intensity =  Light_intensity(self.get_by_filter('type', 'light intensity'))
		self.mail =             Mail(self.get_by_filter('type', 'mail'))
		self.mass =             Mass(self.get_by_filter('type', 'mass'))
		self.mass_by_volume =   Mass_by_volume(self.get_by_filter('type', 'mass by volume'))
		self.mol =              Mol(self.get_by_filter('type', 'mol'))
		self.money =            Money(self.get_by_filter('type', 'money'))
		self.ordinal =          Ordinal(self.get_by_filter('type', 'ordinal'))
		self.percent =          Percent(self.get_by_filter('type', 'percent'))
		self.phone =            Phone(self.get_by_filter('type', 'phone'))
		self.pressure =         Pressure(self.get_by_filter('type', 'pressure'))
		self.set =              Set(self.get_by_filter('type', 'set'))
		self.speed =            Speed(self.get_by_filter('type', 'speed'))
		self.strength =         Strength(self.get_by_filter('type', 'strength'))
		self.surface =          Surface(self.get_by_filter('type', 'surface'))
		self.surface_tension =  Surface_tension(self.get_by_filter('type', 'surface tension'))
		self.temperature =      Temperature(self.get_by_filter('type', 'temperature'))
		self.time =             Time(self.get_by_filter('type', 'time'))
		self.url =              Url(self.get_by_filter('type', 'url'))
		self.voltage =          Voltage(self.get_by_filter('type', 'voltage'))
		self.volume =           Volume(self.get_by_filter('type', 'volume'))

	def list_entities(self, detail = False):
		for key, val in self.entities.items():
			if val.data:
				if not detail:
					print("{:10s}: {}".format(key.upper(), val.__repr__()))
				else:
					val.print_formatted()
					print('')

	def get_entities(self, return_empty = False):
		if return_empty:
			return {key.upper():val.__repr__() for key,val in self.entities.items()}
		else:
			return {key.upper():val.__repr__() for key,val in self.entities.items() if val.data}

class nlu(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.name = 'NLU'

class nlp(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.name = 'NLP'

class sentiment_elements(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class sentiment_values(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data

class sentiment(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.name = 'sentiment'
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
		self.name = 'emotions'
		self.elements = emotion_elements(data['elements']) if 'elements' in data else None
		self.values = emotion_values(data['values']) if 'values' in data else None

class emoticons(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
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
			return self.data
		else:
			return {k:v for k,v in self.data.items() if k in fields}

	def tolist(self):
		return [k for k,v in self.todict().items() if v > 0]

class parser_dependency(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.name = 'parser_dependency'

	def getByRole(self, role):
		return self.get_by_filter('dep', role)

	def tolist(self, tuple = False):
		if not tuple:
			return [d['dep'] for d in self.data]
		else:
			return [(d['source'], d['dep']) for d in self.data]

class postagger(SharedClass):
	def __init__(self, data=None):
		self.data = data
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
			return [d[1] for d in self.data]
		else:
			return [(d[0], d[1]) for d in self.data]

	def fields(self):
		string = self.name.capitalize() + " fields. List of tuples (SOURCE, TAG):\n"
		string += json.dumps([('je', 'CLS'), ('ai', 'V'), ('mange', 'VP'), ('un', 'CD'), ('sandwich', 'N'), ('.', 'PUNCT')], indent=4)
		return string

class sentence_acts(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.name = 'sentence_acts'

class coreference(SharedClass, ExtractClass):
	def __init__(self, data=None):
		self.data = data
		self.name = 'coreference'
