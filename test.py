import lettria
from lettria.analyzeClass import Analyzer

api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRjIiwicHJvamVjdElkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRkIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExNjExZGM5MDMxMGQ4ZWJhMzIiLCJpYXQiOjE1NzU1NDE1NTQsImV4cCI6MTYyMzkyNTU1NH0.dZCq-mv9oHGTCx6lW1GyxmYLehgD1OYg2RMObJueXH0'

client = lettria.Client(key=api_key, raw=False)
phrase1 ="J'aime beaucoup le fromage. Tu detestes la charcuterie. Ca fait vraiment chier mais bon je suis content. Ok"

phrase2 = "Jack Nicholson /d͡ʒæk ˈnɪkəlsən/1 est un acteur, réalisateur et scénariste américain, né le 22 avril 1937 à Neptune (New Jersey). Il a joué un grand nombre de rôles principaux ou secondaires, principalement des personnages sombres, d'anti-héros, de personnages odieux, d'éternel marginal, de vagabond sardonique, de rebelle contre la société2, voire de fou, dans de nombreux films culte du cinéma américain comme Easy Rider, Chinatown, Vol au-dessus d'un nid de coucou, Batman, Mars Attacks!, Pour le pire et pour le meilleur, Les Infiltrés, Shining, et du cinéma européen comme Profession : reporter. Avec douze nominations et trois récompenses, il fait partie des acteurs les plus nommés et récompensés aux Oscars du cinéma."

analyzer = Analyzer(client)
# analyzer.request(phrase1)
# analyzer.request(phrase2)

# analyzer.save_results()
# analyzer.load_results()
analyzer.load_results('verbatim_api.json')
analyzer.normalize() # A NE PAS FAIRE NORMALEMENT, VERBATIM API A UN FORMAT PARTICULIER
# analyzer.load_results('results_0.json')
# analyzer.save_results('results_0.json')


analyzer.process()

# print(analyzer.emoticons)
# print(analyzer.emoticons.todict('happy'))
# print(analyzer.emoticons.tolist())

#NER

# print(analyzer.ner.person)
# print(analyzer.ner.date.tolist())
# print(analyzer.ner.ip)
# print(analyzer.ner.ip.tolist())
# print(analyzer.ner.ip.fields())
# print(analyzer.ner.ip.todict(['country', 'source']))
# analyzer.ner.print_formatted()
# analyzer.ner.interval.print_formatted()
# analyzer.ner.speed
# analyzer.ner.url.print_formatted()
# analyzer.ner.list_entities(detail = True)
# analyzer.ner.list_entities(detail = True)
# analyzer.ner.date.print_formatted()
# print(analyzer.ner.date.todict(['source', 'ISO', 'timestamp']))
# entities = analyzer.ner.get_entities()
# print(entities)

#NLP

# print(analyzer.nlp)
# print(analyzer.nlp.fields())
# print(analyzer.nlp.fields(['test','a']))
# print(analyzer.nlp.tolist('lemma'))
# test = analyzer.nlp.todict(['lemma', 'infinit'])

# for t in test:
#     print(t)

# print(analyzer.nlp.fields())
# print(analyzer.nlp.todict(['source','lemma']))
# print(analyzer.nlp.tolist('lemma'))

#POSTAGGER

# print(analyzer.postagger.tolist())
# print(analyzer.postagger.tolist(tuple = True))
# print(analyzer.postagger.fields())
# print(analyzer.postagger.get_by_tag_exclude(['PUNCT', 'SYM', 'NP']))

#PARSER_DEP
# analyzer.by_sentence()
# print(analyzer.parser_dependency)
# test = analyzer.parser_dependency.get_dep_of_source("agence", return_empty=False, filter_tag = ['JJ'])
# print(test)
# test = analyzer.utils.count_sort(test)
# print(test)

# test = analyzer.parser_dependency.get_dep_of_category(['Personnel'], return_empty=False, filter_tag = ['JJ'], return_lemma = True)
# print(test)
# test = analyzer.utils.count_sort(test)
# print(test)
# print(analyzer.parser_dependency.fields())
# print(analyzer.parser_dependency.tolist())
# print(analyzer.parser_dependency.tolist(True))
# print(analyzer.parser_dependency.todict(['dep', 'lemma', 'tag', 'sub']))


#SENTIMENT
# print(analyzer.sentiment)
# print(analyzer.sentiment.tolist())
# print(analyzer.sentiment.values)
# print(analyzer.sentiment.values.total())
# print(analyzer.sentiment.values.mean())
# print(analyzer.sentiment.values.todict())
# print(analyzer.sentiment.elements)
# print(analyzer.sentiment.elements.tolist())
# print(analyzer.sentiment.elements.todict('target'))
# print(analyzer.sentiment.elements.tolist('target'))
# print(analyzer.sentiment.subsentences)
# print(analyzer.sentiment.subsentences.todict(['sentence', 'values']))
# analyzer.sentiment.print_subsentences_sentiments()
# print(analyzer.sentiment.list_subsentences_sentiments())
# print(analyzer.sentiment.list_sentences_sentiments())
# print(analyzer.sentiment.classify_sentences())
# print(analyzer.sentiment.classify_subsentences()['neutral'])

#EMOTION

# print(analyzer.emotion)
# print(analyzer.emotion.fields())
# print(analyzer.emotion.values)
# print(analyzer.emotion.values.total())
# print(analyzer.emotion.values.average())
# print(analyzer.emotion.values.todict())
# print(analyzer.emotion.elements)
# print(analyzer.emotion.elements.tolist())
# print(analyzer.emotion.elements.tolist())
# print(analyzer.emotion.subsentences)
# analyzer.emotion.print_subsentences_emotions()
# print(analyzer.emotion.list_subsentences_emotions())
# print(analyzer.emotion.list_sentences_emotions())
# print(analyzer.emotion.classify_sentences())
# print(analyzer.emotion.classify_subsentences()['surprise'])
#NLU

# print(analyzer.nlu)
# print(analyzer.nlu.categories_unique('sub'))
# print(analyzer.nlu.categories_count('sub'))
# print(analyzer.nlu)
# print(analyzer.nlu.categories_unique('sub'))
# print(analyzer.nlu.categories_count('sub'))


# SENTIMENT ANALYSIS

# test = analyzer.category_sentiment_by_subsentence('average',\
#         filter = ['General', 'personnel', 'retrait', 'paiement', 'frais'], sample = 5)

# test = analyzer.category_sentiment_by_sentence('average',\
        # filter = ['General', 'personnel', 'retrait', 'paiement', 'frais'], sample = 5)

# for k,v  in test.items():
#     print(k,v)
#     print('')
# print('')

#SENTENCE_ACT

# print(analyzer.sentence_acts)
# print(analyzer.sentence_acts.tolist('predict'))
# print(analyzer.sentence_acts.todict(['predict','probabilities']))
# print(analyzer.sentences_type('question_yn'))

# COREFERENCE
#
# print(analyzer.coreference)
# print(analyzer.coreference.fields())
# print(analyzer.coreference.todict(['source','reference']))

# SYNTHESIS

# print(analyzer.synthesis)
# print(analyzer.synthesis.fields())
# print(analyzer.synthesis.tolist('tag'))
# print(analyzer.synthesis.todict(['source', 'lemma'])[0])

# print(analyzer.lemmatize())
# print(analyzer.tokenize())
# print(analyzer.tokenize(True))

#rajouter par sentence
#proposer filtre par tag
#renvoyer une liste par api + objet global


#mettre un mot et chopper tous les mots qui l'ont en ref
#et filter par tag
