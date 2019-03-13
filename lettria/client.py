import requests

class Client:
    def __init__(self, key=None):
        if not key:
            raise Exception('Missing key for initialization')
        if isinstance(key, str) is False:
            raise Exception('Wrong key format')
        if key.startswith('LettriaProKey'):
            key = key[14:]
        self.key = key

    def printKey(self):
        if self.key:
            print(self.key)

    def request(self, text=''):
        response = None
        try:
            headers = { 'Authorization': 'LettriaProKey ' + str(self.key), 'content-type': 'application/json' }
            response = requests.post('https://api.lettria.com/main', headers=headers, json={'text' : text}).json()
        except:
            None
        return response
