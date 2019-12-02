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

	def tolist(self):
		return [d['source'] for d in self.data]

	def todict(self, fields=['source']):
		if isinstance(fields, str):
			fields = [fields]
		res = []
		for d in self.data:
			tmp = {}
			for field in fields:
				if field in d:
					tmp[field] = d[field]
				elif 'value' in d and d['value'] and field in d['value']:
					tmp[field] = d['value'][field]
				elif 'meaning' in d and d['meaning'] and field in d['meaning']:
					print('AAAH')
					tmp_lst = []
					for d_ in d['meaning']:
						tmp_lst += d_[field]
					tmp[field] = tmp_lst
			res.append(tmp)
		# return [{field:d[field] if field in d else d['value'][field] if 'value' in d and field in d['value']\
				# else d['meaning'][field] if 'meaning' in d and field in d['meaning'] else '' for field in fields} for d in self.data]
		return res

	def fields(self, data = None, recurse = 0):
		if not recurse:
			print(self.name.capitalize() + " fields.\n")
		if not data:
			data = self.data
		keys = {}
		if isinstance(data, list):
			for d in data:
				if isinstance(d, list):
					return 'List of list: [[], [], []]'
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
		else:
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
					if self.getNested(key, item) == value:
						r.append(item)
				else:
					if item[key] == value:
						r.append(item)
			except:
				pass
		return r
