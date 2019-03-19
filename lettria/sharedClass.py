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

	def getNested(self, key, obj):
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

	def getByFilter(self, key, value, list=None):
		r = []
		l = list if list else self.data
		if not isinstance(l, type([])):
			print("Lettria SDK: \033[1;33;40mWARNING:\033[0;37;40m {}".format(
				"getByFilter() was called on something that does not contain a list format."
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
