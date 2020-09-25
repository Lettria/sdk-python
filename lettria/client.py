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
		self.headers = { 'Authorization': 'LettriaProKey ' + str(self.key), 'content-type': 'application/json' }

	def get_key(self):
		if self.key:
			return self.key

	def set_key(self, key=None):
		if key:
			self.key = key
			self.headers = { 'Authorization': 'LettriaProKey ' + str(self.key), 'content-type': 'application/json' }
			return True
		return False

	def print_response_error(self, response):
		if 'Error' in response:
			print("Lettria SDK: \033[1;31;40mERROR:\033[0;37;40m {}".format(response['Error']))
		else:
			print(response)

	def server_request(self, text=''):
		response = None
		try:
			response = requests.post('http://51.254.207.74:4300/api/main', headers=self.headers, json={'text' : text}).json()
		except Exception as e:
			print(e)
			pass
		if response and not isinstance(response, list):
			self.print_response_error(response)
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
