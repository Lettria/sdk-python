import requests
from .sentence import Sentence
from .data import Data

class Client:
	def __init__(self, key=None, raw=True):
		if not key:
			raise Exception('Missing key for initialization')
		if isinstance(key, str) is False:
			raise Exception('Wrong key format')
		if key.startswith('LettriaProKey'):
			key = key[14:]
		self.key = key
		self.raw = raw

	def getKey(self):
		if self.key:
			return self.key

	def setKey(self, key=None):
		if key:
			self.key = key
			return True
		return False

	def printResponseError(self, response):
		if 'Error' in response:
			print("Lettria SDK: \033[1;31;40mERROR:\033[0;37;40m {}".format(response['Error']))
		else:
			print(response)

	def server_request(self, text=''):
		response = None
		try:
			headers = { 'Authorization': 'LettriaProKey ' + str(self.key), 'content-type': 'application/json' }
			response = requests.post('https://api.lettria.com/main', headers=headers, json={'text' : text}).json()
		except Exception as e:
			print(e)
			pass
		if response and not isinstance(response, list):
			self.printResponseError(response)
			response = None
		return response

	def request(self, text='', raw=None):
		_raw = self.raw if raw == None else raw
		sentences_json = self.server_request(text)
		if _raw or not sentences_json:
			return sentences_json
		sentences = []
		for s in sentences_json:
			sentences.append(Sentence(s))
		return Data(sentences)
