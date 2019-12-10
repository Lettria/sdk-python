import json

class SharedClass:
	def __init__(self, data=None, document_level = True):
		self.document_level = document_level

	def format(self, data, force_sentence = ''):
		if not force_sentence and self.document_level:
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

	def tolist(self, fields = None, force_sentence = False):
		if fields:
			if isinstance(fields, list):
				print('Only supports string. Use todict() for multiple fields request.')
				return ''
			else:
				res = []
				result = [v for v in self.todict([fields], force_sentence = True)]
				for seq in result:
					tmp = []
					for d in seq:
						if isinstance(d, dict):
							tmp += d.values()
						else:
							tmp.append(d)
					res.append(tmp)
				return self.format(res)
		else:
			return self.format([[sub['source'] for sub in d] if d else [] for d in self.data], force_sentence)

	def todict(self, fields=['source'], force_sentence = False):
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
		return self.format(res, force_sentence)

	def print_formatted(self):
		length = 25
		d = {}
		seq = []
		print("{:15s}\t{:20s}\t".format('Type','Source'), end = '')
		# print(self.data)
		for _seq in self.data:
			for _seq in self.data:
				if _seq:
					seq = _seq
					break
		for d_ in seq:
			if d_:
				d = d_
				break
		if not d:
			return
		for key in d.keys():
			if key not in ['type', 'source']:
				if isinstance(d[key], dict):
					for k in d[key].keys():
						print("{:12s}".format(k.capitalize()), end = '\t')
						length += 16
				else:
					print("{:10s}".format(key.capitalize()), end = '\t')
					length += 16
		print('')
		print('-' * length)
		for seq in self.data:
			for d in seq:
				print("{:15.15s}\t{:20.20s}\t".format(d['type'].upper(), d['source']), end = '')
				for key in d.keys():
					if key not in ['type', 'source']:
						if isinstance(d[key], dict):
							for k in d[key].keys():
								if not isinstance(d[key][k], (str, float, int)):
									print("{:12.12s}".format(type(d[key][k]).__name__), end = '\t')
								else:
									print("{:12.12s}".format(str(d[key][k])), end = '\t')
						else:
							_field = d[key] if d[key] else 'None'
							print("{:10}".format(_field), end = '\t')
				if d:
					print('')

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
			return self.getNested(key[:-1], obj)
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
						if self.getNested(key, item) == value:
							r.append(item)
					else:
						if item[key] == value:
							r.append(item)
				except:
					pass
			r_lst.append(r)
		return r_lst
