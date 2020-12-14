from .NLP import NLP
from .utils import flatten_lst

GLOBAL = ['g', 'global', 'glob']
DOC = ['d', 'doc', 'document', 'documents']
SENT = ['s', 'sentence', 'sent', 'sentences']
SUB = ['sub', 'subsentence', 'subsentences']
TOK = ['t', 'token', 'tok', 'tokens']
POSITIVE = ['positive', 'pos', '+']
NEGATIVE = ['negative', 'neg', '-']
NEUTRAL = ['neutral', 'neut']

## DEPRECATED, Functional interface should be used instead.
class Sentiment:
    def __init__(self, nlp):
        if not isinstance(nlp, NLP):
            print('Please provide an instance of the NLP class')
            raise TypeError
        self.nlp = nlp

    def get_emotion(self, level='document'):
        """ Returns emotion results at the specified hierarchical level """
        emotions = []
        if level in GLOBAL:
            _iter = [self.nlp]
        elif level in DOC:
            _iter = self.nlp.documents
        elif level in SENT:
            _iter = self.nlp.sentences
        elif level in SUB:
            _iter = self.nlp.subsentences
        else:
            print("'" + str(level) + "' is an incorrect value for level argument.")
            return []
        
        for d in _iter:
            tmp = {}
            for e in d.emotion_flat:
                if e[0] not in tmp:
                    tmp[e[0]] = {'sum':0, 'occurences':0, 'average':0}
                tmp[e[0]]['sum'] += round(e[1], 4)
                tmp[e[0]]['occurences'] += 1
            for e in tmp:
                if tmp[e]['occurences'] != 0:
                    tmp[e]['average'] = round(tmp[e]['sum'] / tmp[e]['occurences'], 4)
            emotions.append(tmp)
        return emotions

    def get_sentiment(self, level='document'):
        """ Returns sentiment results at the specified hierarchical level """
        sentiments = []
        if level in GLOBAL:
            _iter = [self.nlp]
        elif level in DOC:
            _iter = self.nlp.documents
        elif level in SENT:
            _iter = self.nlp.sentences
        elif level in SUB:
            _iter = self.nlp.subsentences
        else:
            print("'" + str(level) + "' is an incorrect value for level argument.")
            return []
        
        for d in _iter:
            tmp = {}
            for e in d.sentiment_flat:
                for pol in e:
                    if pol not in tmp:
                        tmp[pol] = {'sum':0, 'occurences':0, 'average':0}
                    tmp[pol]['sum'] += e[pol]
                    if e[pol] != 0 or pol == 'total':
                        tmp[pol]['occurences'] += 1
            for e in tmp:
                if tmp[e]['occurences'] != 0:
                    tmp[e]['average'] = round(tmp[e]['sum'] / tmp[e]['occurences'], 4)
            for p in tmp:
                tmp[p]['sum'] = round(tmp[p]['sum'], 4)
            sentiments.append(tmp)
        return sentiments

    def add_dict(self, d1, d2):
        for k,v in d2.items():
            d1[k] = d1.get(k, 0) + v
        return d1

    def sum_dicts(self, lst):
        merge = {}
        for d in lst:
            merge = self.add_dict(merge, d)
        return merge

    def average_dicts(self, lst):
        merge = {}
        for d in lst:
            merge = self.add_dict(merge, d)
        c = len(lst)
        return {k:round(v/c, 5) for k,v in merge.items()}

    def word_sentiment(self, granularity = 'sentence', lemma = False, filter_pos = None):
        """ Returns sentiment associated with word"""
        if granularity not in SENT + SUB:
            print("granularity argument should be 'sentence' or 'subsentence'")
            return None
        tokens = self.nlp.vocabulary(filter_pos=filter_pos, lemma=lemma)
        res = {t:{'val':0, 'occ':0} for t in tokens}
        iter_ = self.nlp.subsentences if granularity in SUB else self.nlp.sentences
        for sentence in iter_:
            val = sentence.sentiment.get('total', 0)
            tmp_iter = sentence.lemma if lemma else sentence.token
            for t, p in zip(tmp_iter, sentence.pos):
                if not filter_pos or p in filter_pos:
                    res[(t,p)]['val'] += val
                    res[(t,p)]['occ'] += 1
        res = {t: round(res[t]['val'] / (res[t]['occ'] + 1e-8), 4) for t in res.keys()}
        return res

    def meaning_sentiment(self, granularity='sentence', filter_meaning=None):
        """ Returns sentiment associated with meaning"""
        if granularity not in SENT + SUB:
            print("granularity argument should be 'sentence' or 'subsentence'")
            return None
        if isinstance(filter_meaning, str):
            filter_meaning = [filter_meaning]
        meanings = list(set([m[1] for m in self.nlp.meaning_flat if m[1]]))
        if filter_meaning and isinstance(filter_meaning, list):
            meanings = filter_meaning
        res = {t:{'val':0, 'occ':0} for t in meanings}
        iter_ = self.nlp.subsentences if granularity == 'subsentence' else self.nlp.sentences
        for sentence in iter_:
            val = sentence.sentiment.get('total',0)
            tmp_iter = list(set([m[1] for m in sentence.meaning_flat if m[1]]))
            for m in tmp_iter:
                if not filter_meaning or m in filter_meaning:
                    res[m]['val'] += val
                    res[m]['occ'] += 1
        res = {t: round(res[t]['val'] / (res[t]['occ'] + 1e-8), 4) for t in res.keys()}
        return res

    def filter_polarity(self, polarity, granularity='sentence'):
        if polarity not in POSITIVE + NEGATIVE + NEUTRAL:
            print("polarity argument should be 'neutral', 'positive' or 'negative'.")
            return None
        if granularity not in SENT + SUB:
            print("granularity argument should be 'sentence' or 'subsentence'")
            return None
        def check_polarity(value, polarity):
            if polarity in NEUTRAL:
                return value == 0
            elif polarity in POSITIVE:
                return value > 0
            elif polarity in NEGATIVE:
                return value < 0
            else:
                return False
        iter_ = self.nlp.subsentences if granularity == 'subsentence' else self.nlp.sentences
        return [s for s in iter_ if check_polarity(s.sentiment.get('total', 0), polarity)]

    def filter_emotion(self, emotions, granularity='sentence'):
        if isinstance(emotions, str):
            emotions = [emotions]
        if granularity not in SENT + SUB:
            print("granularity argument should be 'sentence' or 'subsentence'")
            return None
        def check_emotion(emotion_lst, filter):
            emotions = [e[0] for e in emotion_lst]
            for e in emotions:
                if e in filter:
                    return True
            return False
        iter_ = self.nlp.subsentences if granularity in SUB else self.nlp.sentences
        return [s for s in iter_ if check_emotion(s.emotion, emotions)]
