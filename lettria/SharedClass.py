GLOBAL = ['g', 'global', 'glob']
DOC = ['d', 'doc', 'document', 'documents']
SENT = ['s', 'sentence', 'sent', 'sentences']
SUB = ['sub', 'subsentence', 'subsentences']
TOK = ['t', 'token', 'tok', 'tokens']
POSITIVE = ['positive', 'positif', 'pos', '+']
NEGATIVE = ['negative', 'negatif', 'neg', '-']
NEUTRAL = ['neutral', 'neutre', 'neut']

class SharedClass:
    def __init__(self):
        self.client = None
        if client or api_key:
            self.add_client(client, api_key)
        self.documents = []
        self.max = len(self.documents)
        self.data = self.documents
        self.fields = [p for p in dir(Sentence) if isinstance(getattr(Sentence,p),property)]
        if 'token_flat' not in self.fields:
            self._generate_properties()
    
    def vocabulary(self, filter_pos = None, lemma=False, level='global'):
        """ Generates vocabulary list of words"""
        vocabulary = []
        tokens = self.token_flat if not lemma else self.lemma_flat
        pos = self.pos_flat
        for t, p in zip(tokens, pos):
            if (t,p) not in vocabulary:
                if not filter_pos or p in filter_pos:
                    vocabulary.append((t, p))
        return vocabulary
    
    def list_entities(self, level='global'):
        """ Returns dictionary (or list of dict) of ner entities at the specified level"""
        entities = []
        tmp = {}
        for t, e in zip(self.token_flat, self.ner_flat):
            if e.get('type', None):
                for type in e['type']:
                    if type in tmp:
                        tmp[type].append(t)
                    else:
                        tmp[type] = [t]
        entities.append(tmp)
        return entities

    def word_count(self, filter_pos = None, lemma=False, level='global'):
        """ Generates word count, document or global level """
        word_count = []
        tokens = self.token_flat if not lemma else self.lemma_flat
        pos = self.pos_flat
        word_count = {}
        for t, p in zip(tokens, pos):
            if not filter_pos or p in filter_pos:
                word_count[(t, p)] = word_count.get((t,p), 0) + 1
        return word_count

    def word_frequency(self, filter_pos = None, lemma=False, level='global'):
        """ Generates frequency list of words """
        vocab = self.word_count(filter_pos=filter_pos, lemma=lemma)
        total = sum(self.word_count().values())
        return {k:round(v/(total + 1e-10), 10) for k,v in vocab.items()}

    def statistics(self):
        class_name = self.__class__.__name__
        return {'documents': len(self.documents) if class_name in ['NLP'] else int(class_name == 'Document'),
        'sentences': len(self.sentences) if class_name in ['NLP', 'Document'] else int(class_name == 'Sentence'),
        'subsentences': len(self.subsentences) if class_name in ['NLP', 'Document', 'Sentence'] else int(class_name == 'Subsentence'),
        'tokens': len(self.tokens)}
    
    def get_emotion(self, granularity = 'sentence'):
        """ Returns emotion results at the specified hierarchical level """
        class_name = self.__class__.__name__
        if granularity not in SENT + SUB:
            print("granularity argument should be 'sentence' or 'subsentence'")
            return None
        if class_name == 'Subsentence':
            granularity = 'subsentence'
        emotions = {}
        _iter = self.subsentences if granularity in SUB else self.sentences
        denumerator = self.statistics().get('subsentences', 1) if granularity in SUB else self.statistics().get('sentences', 1)
        for sequence in _iter:
            for e in sequence.emotion_flat:
                if e[0] not in emotions:
                    emotions[e[0]] = {'sum':0, 'occurences':0, 'average':0}
                emotions[e[0]]['sum'] += round(e[1], 4)
                emotions[e[0]]['occurences'] += 1
            for e in emotions:
                if emotions[e]['occurences'] != 0:
                    emotions[e]['average'] = round(emotions[e]['sum'] / (denumerator  + 1e-6), 4)
        for k in emotions.keys():
            emotions[k]['sum'] = round(emotions[k]['sum'], 4)
            emotions[k]['average'] = round(emotions[k]['average'], 4)
        return emotions

    def get_sentiment(self, granularity='sentence'):
        """ Returns sentiment results at the specified hierarchical level """
        class_name = self.__class__.__name__
        if granularity not in SENT + SUB:
            print("granularity argument should be 'sentence' or 'subsentence'")
            return None
        if class_name == 'Subsentence':
            granularity = 'subsentence'
        _iter = self.subsentences if granularity in SUB else self.sentences
        denumerator = self.statistics().get('subsentences', 1) if granularity in SUB else self.statistics().get('sentences', 1)
        sentiments = {}
        for sequence in _iter:
            for e in sequence.sentiment_flat:
                for pol in e:
                    if pol not in sentiments:
                        sentiments[pol] = {'sum':0, 'occurences':0, 'average':0}
                    sentiments[pol]['sum'] += e[pol]
                    if e[pol] != 0 or pol == 'total':
                        sentiments[pol]['occurences'] += 1
            for e in sentiments:
                if sentiments[e]['occurences'] != 0:
                    sentiments[e]['average'] = sentiments[e]['sum'] / (denumerator + 1e-6)
            for p in sentiments:
                sentiments[p]['sum'] = sentiments[p]['sum']
        for k in sentiments.keys():
            sentiments[k]['sum'] = round(sentiments[k]['sum'], 4)
            sentiments[k]['average'] = round(sentiments[k]['average'], 4)
        return sentiments
    
    def filter_polarity(self, polarity, granularity='sentence'):
        if isinstance(polarity, str):
            polarity = [polarity]
        for p in polarity:
            if p not in POSITIVE + NEGATIVE + NEUTRAL:
                print("polarity argument should be 'neutral', 'positive' or 'negative'.")
                return []
        if granularity not in SENT + SUB:
            print("granularity argument should be 'sentence' or 'subsentence'")
            return []
        class_name = self.__class__.__name__
        if class_name == 'Subsentence':
            granularity = 'subsentence'
        def check_polarity(value, polarity):
            if len(set(NEUTRAL).intersection(set(polarity))) >= 1:
                if value == 0:
                    return True
            if len(set(POSITIVE).intersection(set(polarity))) >= 1:
                if value > 0:
                    return True
            if len(set(NEGATIVE).intersection(set(polarity))) >= 1:
                if value < 0:
                    return True
            else:
                return False
        _iter = self.subsentences if granularity == 'subsentence' else self.sentences
        # print([s for s in _iter if check_polarity(s.sentiment.get('total', 0), polarity)])
        return [s for s in _iter if check_polarity(s.sentiment.get('total', 0), polarity)]

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
        _iter = self.nlp.subsentences if granularity in SUB else self.nlp.sentences
        return [s for s in _iter if check_emotion(s.emotion, emotions)]

    def word_sentiment(self, granularity = 'sentence', lemma = False, filter_pos = None):
        """ Returns sentiment associated with word"""
        if granularity not in SENT + SUB:
            print("granularity argument should be 'sentence' or 'subsentence'")
            return None
        tokens = self.nlp.vocabulary(filter_pos=filter_pos, lemma=lemma)
        res = {t:{'val':0, 'occ':0} for t in tokens}
        _iter = self.nlp.subsentences if granularity in SUB else self.nlp.sentences
        for sentence in _iter:
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
        _iter = self.nlp.subsentences if granularity == 'subsentence' else self.nlp.sentences
        for sentence in _iter:
            val = sentence.sentiment.get('total',0)
            tmp_iter = list(set([m[1] for m in sentence.meaning_flat if m[1]]))
            for m in tmp_iter:
                if not filter_meaning or m in filter_meaning:
                    res[m]['val'] += val
                    res[m]['occ'] += 1
        res = {t: round(res[t]['val'] / (res[t]['occ'] + 1e-8), 4) for t in res.keys()}
        return res