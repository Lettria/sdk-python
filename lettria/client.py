import requests
import random
import json

class RequestError(Exception): pass

class Client:
    def __init__(self, key=None):
        if not key:
            raise Exception('Missing key for initialization')
        if isinstance(key, str) is False:
            raise Exception('Wrong key format')
        if key.startswith('LettriaProKey'):
            key = key[14:]
        self.key = key
        self.headers = { 'Authorization': 'LettriaProKey ' + str(self.key), 'content-type': 'application/json' }
        self.max_try = 2

    def print_response_error(self, response):
        if 'Error' in response:
            print("Lettria SDK: \033[1;31;40mERROR:\033[0;37;40m {}".format(response['Error']))
        else:
            print(response)

    def request(self, text):
        result = None
        response = None
        i = 0
        while i < self.max_try:
            try:
                response = requests.post('https://api.lettria.com/', headers=self.headers, json={'text' : text}).json()
                if not response or (response and not isinstance(response, dict)):
                    raise Exception
                result = response
                break
            except Exception as e:
                print(e)
                i += 1
        if result is None:
            print(f'Request failed after {self.max_try} tries.')
        if result and not isinstance(result, dict):
            result = None
        return result
    
    def request_batch(self, batch_documents):
        result = []
        i = 0
        while i < self.max_try:
            try:
                response = requests.post('https://api.lettria.com/', headers=self.headers, json={'documents' : batch_documents}).json()
                if not response or (response and not isinstance(response, list)):
                    raise Exception
                result = response
                break
            except Exception as e:
                i += 1
        if result is None or len(result) == 0:
            print(f'Batch request failed after {self.max_try} tries.')
        if result and not isinstance(result, list):
            result = []
        return result
    
    def _check_result(self, result):
        """ Check if detail key is empty """
        bad_idx = []
        for i, r in enumerate(result):
            if not isinstance(r, dict) or not 'detail' in r:
                bad_idx.append(i)
        return bad_idx
    
    def request_document(self, document, skip_document = False, verbose=False):
        """ Input: string or list of string"""
        results = []
        try:
            results = self.request(document)
            if results is None:
                raise RequestError
        except RequestError:
            if skip_document:
                return None
        return results

    def request_batch_documents(self, batch_documents, document_ids, skip_document = False):
        ''' Input: string or list of string'''
        results = self.request_batch(batch_documents)
        if skip_document:
            for idx in range(len(results) - 1, -1, -1):
                if not results[idx]:
                    print("WARNING: Skipping document, request error.")
                    results.pop(idx)
                    if document_ids:
                        document_ids.pop(idx)
        return results, document_ids