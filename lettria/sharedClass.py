import json


class SharedClass:
	def __init__(self, data=None):
		pass
	def __str__(self):
		try:
			return json.dumps(self.data, indent=4, sort_keys=True)
		except:
			return str(self.data)

	def get(self):
		return self.data

	def set(self, data=None):
		try:
			self.data = data
			return True
		except:
			return False

	def get_nested(self, key, obj):
		if not isinstance(obj, dict):
			return None
		keys = key.split('.')
		k = keys.pop(0)
		if k not in obj: return None
		obj = obj[k]
		key = ''
		if len(keys) > 0:
			for item in keys: key += item + '.'
			return self.get_nested(key[:-1], obj)
		return obj

	def get_by_filter(self, key, value, list=None):
		r = []
		l = list if list else self.data
		if not isinstance(l, type([])):
			print("Lettria SDK: \033[1;33;40mWARNING:\033[0;37;40m {}".format(
				"get_by_filter() was called on something that does not contain a list format."
			))
			return None
		for item in l:
			try:
				if '.' in key:
					if self.get_nested(key, item) == value:
						r.append(item)
				else:
					if item[key] == value:
						r.append(item)
			except:
				pass
		return r

class SharedClass_A:
	""" Base class for all subclasses and entity classes.
		Provides tolist and todict methods which allows easy access to data.
		"""
	def __init__(self, data=None, document_level = True):
		self.document_level = document_level

	def format(self, data, force = ''):
		if force == 'sentence':
			return data
		elif force == 'document' or self.document_level:
			tmp = []
			for d in data:
				if d:
					tmp += d
				else:
					tmp += []
			return tmp
		else:
			return data

	def __str__(self):
		try:
			return json.dumps(self.format(self.data), indent=4, sort_keys=True)
		except Exception as e:
			print(e)
			return str(self.format(self.data))

	def get(self):
		return self.format(self.data)

	def set(self, data=None):
		try:
			self.data = data
			return True
		except:
			return False

	def tolist(self, fields = None, force = ''):
		if fields:
			if isinstance(fields, list):
				print('Only supports string. Use todict() for multiple fields request.')
				return ''
			else:
				res = []
				result = [v for v in self.todict([fields], force = 'sentence')]
				for seq in result:
					tmp = []
					for d in seq:
						if isinstance(d, dict):
							tmp += d.values()
						else:
							tmp.append(d)
					res.append(tmp)
				return self.format(res, force)
		else:
			return self.format([[sub['source'] for sub in d] if d else [] for d in self.data], force)

	def todict(self, fields=['source'], force = ''):
		if isinstance(fields, str):
			fields = [fields]
		res = []
		for sent in self.data:
			tmp_lst = []
			if sent:
				for d in sent:
					tmp = {}
					for field in fields:
						if field in d:
							tmp[field] = d[field]
						elif 'value' in d and d['value'] and field in d['value']:
							tmp[field] = d['value'][field]
						elif 'lemmatizer' in d and d['lemmatizer'] and field in d['lemmatizer']:
							tmp[field] = d['lemmatizer'][field]
						elif 'lemmatizer' in d and isinstance(d['lemmatizer'], list) and field in d['lemmatizer'][0]:
							tmp[field] = d['lemmatizer'][0][field]
						elif 'meaning' in d and d['meaning'] and field in d['meaning']:
							tmp_lst = []
							for d_ in d['meaning']:
								tmp_lst += d_[field]
							tmp[field] = tmp_lst
					tmp_lst.append(tmp)
			res.append(tmp_lst)
		return self.format(res, force)

	def fields(self, data = None, recurse = 0):
		if not recurse and self.name:
			print(self.name.capitalize() + " fields:")
		if not data:
			data = self.data
		keys = {}
		_data = data
		if isinstance(data, list):
			if isinstance(data[0], list):
				for _d in data:
					if _d:
						_data = _d if isinstance(_d, list) else data
						break
			else:
				_data = data
			for d in _data:
				if isinstance(d, list):
					return 'List of list: [[], [], []]'
				elif isinstance(d, str):
					return d
				for key in d.keys():
					if key in keys:
						continue
					if isinstance(d[key], (list, dict)) and d[key]:
						keys[key] = self.fields(d[key], 1)
					else:
						keys[key] = []
					# print(keys)
			if recurse == 0:
				return json.dumps(keys, indent = 4, sort_keys = True)
			else:
				return keys
		elif isinstance(data, dict):
			for key in data.keys():
				if key in keys:
					continue
				if isinstance(data[key], (list, dict)) and data[key]:
					keys[key] = self.fields(data[key], 1)
				else:
					keys[key] = []
			if recurse == 0:
				return json.dumps(keys, indent = 4, sort_keys = True)
			else:
				return keys
		else:
			return data

	def get_nested(self, key, obj):
		if not isinstance(obj, dict):
			return None
		keys = key.split('.')
		k = keys.pop(0)
		if k not in obj: return None
		obj = obj[k]
		key = ''
		if len(keys) > 0:
			for item in keys: key += item + '.'
			return self.get_nested(key[:-1], obj)
		return obj

	def get_by_filter(self, key, value, _list=None):
		l = _list if _list else self.data
		if not isinstance(l, list):
			print("Lettria SDK: \033[1;33;40mWARNING:\033[0;37;40m {}".format(
				"get_by_filter() was called on something that does not contain a list format."
			))
			return None
		r_lst = []
		for seq in l:
			r = []
			for item in seq:
				try:
					if '.' in key:
						if self.get_nested(key, item) == value:
							r.append(item)
					else:
						if item[key] == value:
							r.append(item)
				except:
					pass
			r_lst.append(r)
		return r_lst
