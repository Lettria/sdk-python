from .subClasses import *
import json
import os
import lettria
from collections import Counter
import numpy as np

class Analyzer:
    """ Class for data analysis of API return.
        Takes a Client class as input which is used to make api requests.
        Provides both high and low level methods to access data via specific class
        for each key in the api result or methods designed for specific use cases.
        """
    def __init__(self, api_key = '', raw=True, client = None, data = None):
        if client:
            self.client = client
        else:
            self.client = lettria.Client(api_key, raw=True)
        self.data = data
        self.result = []
        self.utils = utils()
        self.document_level = True

    def __str__(self):
        return json.dumps(self.result, indent = 4)

    def request(self, data = None):
        if not self.client:
            self.missing_client()
            return
        if not data:
            if self.data:
                data = self.data
            else:
                return
        try:
            if isinstance(data, list):
                for seq in data:
                    self.result += self.client.request(seq, raw=True)
            else:
                self.result += self.client.request(data, raw=True)
        except Exception as e:
            print(e)
            pass

    def reset_data(self):
        self.result = []

    def missing_client(self):
        print('Please assign a client in order to make a request.')

    def by_sentence(self):
        """ Change return format of all functions so that the result is returned
            sentence by sentence"""
        try:
            self.document_level = False
            self.ner.document_level = False
            self.postagger.document_level = False
            self.emoticons.document_level = False
            self.parser_dependency.document_level = False
            self.nlp.document_level = False
            self.nlu.document_level = False
            self.emotion.document_level = False
            self.emotion.values.document_level = False
            self.emotion.subsentences.document_level = False
            self.emotion.elements.document_level = False
            self.sentiment.document_level = False
            self.sentiment.values.document_level = False
            self.sentiment.subsentences.document_level = False
            self.sentiment.elements.document_level = False
            self.sentence_acts.document_level = False
            self.coreference.document_level = False
            self.synthesis.document_level = False
        except:
            print('Error classes not initialized, process() should be called.')

    def by_document(self):
        """ Change return format of all functions so that the individual sentences
        results are merged together
        """
        try:
            self.document_level = True
            self.ner.document_level = True
            self.postagger.document_level = True
            self.emoticons.document_level = True
            self.parser_dependency.document_level = True
            self.nlp.document_level = True
            self.nlu.document_level = True
            self.emotion.document_level = True
            self.emotion.values.document_level = True
            self.emotion.subsentences.document_level = True
            self.emotion.elements.document_level = True
            self.sentiment.document_level = True
            self.sentiment.values.document_level = True
            self.sentiment.subsentences.document_level = True
            self.sentiment.elements.document_level = True
            self.sentence_acts.document_level = True
            self.coreference.document_level = True
            self.synthesis.document_level = True
        except:
            print('Error classes not initialized, process() should be called.')

    def process(self, document_level = True):
        """
        Creates subclasses for the different keys of the api.
        Must be used after makin a request or loading a file.
        All classes implement common methods such as .tolist() and .todict() which
        returns data in the specified format.
        """
        if not self.result:
            print('No data to analyze')
        else:
            self.ner = ner_Analyzer([[sub for sub in d['NER']] for d in self.result if 'NER' in d], document_level)
            self.postagger = postagger_Analyzer([[sub for sub in d['postagger']] for d in self.result if 'postagger' in d], document_level)
            self.emoticons = emoticons_Analyzer(self.concat_emoticons(document_level), document_level)
            self.parser_dependency = parser_dependency_Analyzer([[sub for sub in d['parser_dependency']] for d in self.result if 'parser_dependency' in d], document_level)
            self.nlp = nlp_Analyzer([[sub for sub in d['NLP']] for d in self.result if 'NLP' in d], document_level)
            self.nlu = nlu_Analyzer([[sub for sub in d['NLU']] for d in self.result if 'NLU' in d], document_level)
            self.emotion = emotion_Analyzer([{sub:v for sub,v in d['emotion'].items()} for d in self.result if 'emotion' in d], document_level)
            self.sentiment = sentiment_Analyzer([{sub:v for sub,v in d['sentiment'].items()} for d in self.result if 'sentiment' in d], document_level)
            self.sentence_acts = sentence_acts_Analyzer([[{sub:v for sub,v in d['sentence_acts'].items()}] if 'sentence_acts' in d and d['sentence_acts'] else [{}] for d in self.result ], document_level)
            self.coreference = coreference_Analyzer([[sub for sub in d['coreference']] for d in self.result if 'coreference' in d], document_level)
            self.synthesis = synthesis_Analyzer([[sub for sub in d['synthesis']] for d in self.result if 'synthesis' in d], document_level)

    def lemmatize(self):
        """ Returns a list of lemmatized tokens, some tokens are merged due to regex"""
        return self.synthesis.tolist('lemma')

    def tokenize(self, merge = False):
        ''' Returns a list of tokens.
            Option merge: Merge tokens according to NER patterns.
            merge False :   ['2','km','/','/h']
            merge True :    ['2km/h']                   '''
        if merge:
            return self.synthesis.tolist('source')
        else:
            return self.nlp.tolist('source')

    def vocabulary(self, lemma = False, lowercase = False, alphabetic = False, max_len = 40):
        """ Returns a list of unique tokens """
        if lemma:
            data = self.synthesis.tolist('lemma', force = 'document')
        else:
            data = self.synthesis.tolist('source', force = 'document')
        if alphabetic:
            data = [d for d in data if d.isalpha() or d in '-_']
        if lowercase:
            data = [d.lower() for d in data]
        data = [d for d in data if len(d) < max_len]
        return sorted(list(set(data)))

    def bag_of_words(self, lemma = False, return_matrix = False, vocabulary = ''):
        """ Returns a dict or matrix of words occurences based on a vocabulary """
        if vocabulary:
            vocab = vocabulary
        else:
            vocab = self.vocabulary(lemma)
        vocab = sorted(vocab)
        if self.document_level:
            if lemma:
                data = self.synthesis.tolist('lemma', force = 'document')
            else:
                data = self.synthesis.tolist('source', force = 'document')
            if not return_matrix:
                return {voc:data.count(voc) for voc in vocab}
            else:
                array = np.zeros((1, len(vocab)))
                for idx, word in enumerate(vocab):
                    array[0][idx] = data.count(word)
                return array
        else:
            if lemma:
                data = self.synthesis.tolist('lemma', force = 'sentence')
            else:
                data = self.synthesis.tolist('source', force = 'sentence')
            if not return_matrix:
                return [{voc:sub.count(voc) for voc in vocab} for sub in data]
            else:
                array = np.zeros((len(data), len(vocab)))
                for i, seq in enumerate(data):
                    for idx, word in enumerate(vocab):
                        array[i][idx] = seq.count(word)
                return array


    def concat_emoticons(self, document_level):
        """ Merge different dictionnaries of emoticon occurences"""
        self.emoticons = [[d['emoticons']['emoticon']] for d in self.result if 'emoticons' in d]
        lst_emots = []
        for seq in self.emoticons:
            emots = {k:0 for k in seq[0].keys() if seq[0]}
            for d in seq:
                for k,v in d.items():
                    if v > 0:
                        emots[k] += v
            lst_emots.append(emots)
        return lst_emots

    def category_sentiment_by_subsentence(self, mode = 'average', filter = [], sample = 5):
        """ Return the sentiment associated with a category.
            It takes the sum or average of sentiment value of each subsentence in which the category appears."""
        cats = self.nlu.categories_unique('sub')
        if filter:
            cats = [cat for cat in cats if cat in filter]
        sentiments = {cat:{'positive':0, 'negative':0, 'total':0, 'occurences':0, 'p_sentences': [], 'n_sentences':[]} for cat in cats}
        sub_ids = self.sentiment.subsentences.todict(['start_id', 'end_id', 'sentence'], 'sentence')
        sub_values = self.sentiment.subsentences.todict(['values'], 'sentence')
        length = 0
        for id_sent, (sent, sent2) in enumerate(zip(sub_ids, sub_values)):
            for id_sub, value in zip(sent, sent2):
                tmp = self.nlu.categories_unique('sub', id_sent, id_sub)
                for cat in tmp:
                    if not filter or filter and cat in filter:
                        sentiments[cat]['negative'] += value['values']['negative']
                        sentiments[cat]['positive'] += value['values']['positive']
                        sentiments[cat]['total'] += value['values']['total']
                        sentiments[cat]['occurences'] += 1
                        if value['values']['total'] > 0.5 and len(sentiments[cat]['p_sentences']) < sample:
                            sentiments[cat]['p_sentences'].append(id_sub['sentence'])
                        elif value['values']['total'] < -0.5 and len(sentiments[cat]['n_sentences']) < sample:
                            sentiments[cat]['n_sentences'].append(id_sub['sentence'])
                length += 1
        if mode == 'sum':
            sentiments = {k:{k1: round(v1,3) for k1, v1 in v.items()} for k,v in sentiments.items()}
        else:
            fields = ['negative', 'positive', 'total']
            sentiments = {k:{k1: round(v1 / v['occurences'] + 1e-6, 3) if k1 in fields else v1 for k1, v1 in v.items()} for k,v in sentiments.items()}
        return sentiments

    def category_sentiment_by_sentence(self, mode = 'average', filter = [], sample = 5):
        """ Return the sentiment associated with a category.
            It takes the sum or average of sentiment value of each sentence in which the category appears."""
        cats = self.nlu.categories_unique('sub')
        if filter:
            cats = [cat for cat in cats if cat in filter]
        sentiments = {cat:{'positive':0, 'negative':0, 'total':0, 'occurences':0, 'p_sentences': [], 'n_sentences':[]} for cat in cats}
        values = self.sentiment.values.tolist('sentence')
        sentences = self.parser_dependency.tolist(None, 'document')
        for id_sent, (sent, value) in enumerate(zip(sentences, values)):
            if not value or not sent:
                continue
            sent = ' '.join(sent)
            value = value[0]
            cats = self.nlu.categories_unique('sub', id_sent)
            for cat in cats:
                if not filter or filter and cat in filter:
                    sentiments[cat]['negative'] += value['negative']
                    sentiments[cat]['positive'] += value['positive']
                    sentiments[cat]['total'] += value['total']
                    sentiments[cat]['occurences'] += 1
                    if value['total'] > 0.5 and len(sentiments[cat]['p_sentences']) < sample:
                        sentiments[cat]['p_sentences'].append(sent)
                    elif value['total'] < -0.5 and len(sentiments[cat]['n_sentences']) < sample:
                        sentiments[cat]['n_sentences'].append(sent)
        if mode == 'sum':
            sentiments = {k:{k1: round(v1,3) for k1, v1 in v.items()} for k,v in sentiments.items()}
        else:
            fields = ['negative', 'positive', 'total']
            sentiments = {k:{k1: round(v1 / v['occurences'] + 1e-6, 3) if k1 in fields else v1 for k1, v1 in v.items()} for k,v in sentiments.items()}
        return sentiments

    def sentences_type(self, filter = []):
        """ Returns a list of all the sentences of the specified type.
            filter argument may be a string or a list"""
        types = self.sentence_acts.tolist('predict')
        sentences = self.parser_dependency.tolist(None, True)
        if filter and not isinstance(filter, list):
            filter = [filter]
        if not filter:
            filter = ['question_yn', 'question_open', 'assert', 'command', 'exclam']
        questions = []
        for type, sent in zip(types, sentences):
            if type in filter:
                questions.append(' '.join(sent))
        return questions

    def save_results(self, file = ''):
        """ Writes json result to a file with the specified name."""
        path_ok = 0
        c = 0
        if not file:
            file = 'results'
            while not path_ok:
                path = file + '_' + str(c)
                if not os.path.isfile(path + '.json'):
                    path_ok = 1
                else:
                    c += 1
        else:
            path = file
            if path.endswith('.json'):
                path = path.replace('.json', '')
        with open(path + '.json', 'w') as f:
            json.dump(self.result, f)

    def load_results(self, file = 'results_0'):
        """ Loads result from a valid json file."""
        if file.endswith('.json'):
            file = file.replace('.json', '')
        with open(file + '.json', 'r') as f:
            self.result = json.load(f)

# A REMOVE
    def normalize(self):
            self.result = [d['Retour_api'] for d in self.result]
            tmp = []
            for d in self.result:
                if d:
                    tmp += d
            self.result = tmp
