import lettria
from lettria.analyzeClass import Analyzer

api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRjIiwicHJvamVjdElkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRkIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExNjExZGM5MDMxMGQ4ZWJhMzIiLCJpYXQiOjE1NzU1NDE1NTQsImV4cCI6MTYyMzkyNTU1NH0.dZCq-mv9oHGTCx6lW1GyxmYLehgD1OYg2RMObJueXH0'

client = lettria.Client(key=api_key, raw=False)
# phrase1 = "Je :) mange du poulet a 4 heures du matin. 21m/s 23/07/1192. www.google.com   www.google.fr 12.143.43.123 Hier, 3 km/h 12 km 145.247.145.1 Henri est vraiment devenu fou. 124.53.111.3 :-) :D XD"

phrase1 ="J'aime beaucoup le fromage. Tu detestes la charcuterie. Ca fait vraiment chier mais bon je suis content. Ok"

phrase2 = "Jack Nicholson /d͡ʒæk ˈnɪkəlsən/1 est un acteur, réalisateur et scénariste américain, né le 22 avril 1937 à Neptune (New Jersey). Il a joué un grand nombre de rôles principaux ou secondaires, principalement des personnages sombres, d'anti-héros, de personnages odieux, d'éternel marginal, de vagabond sardonique, de rebelle contre la société2, voire de fou, dans de nombreux films culte du cinéma américain comme Easy Rider, Chinatown, Vol au-dessus d'un nid de coucou, Batman, Mars Attacks!, Pour le pire et pour le meilleur, Les Infiltrés, Shining, et du cinéma européen comme Profession : reporter. Avec douze nominations et trois récompenses, il fait partie des acteurs les plus nommés et récompensés aux Oscars du cinéma."
# ret = client.request(phrase)
# print(ret.data[0].get_judgement_items())
# exit()

# phrase1 = "J'ai mange un sandwich."

analyzer = Analyzer(client)
# ret = client.request(phrase)
# analyzer.request(phrase1)
# analyzer.request(phrase2)

# analyzer.save_results()
# analyzer.load_results()
analyzer.load_results('verbatim_api.json')

analyzer.analyze_document()
# analyzer.analyze_sentence()

# print(analyzer.emoticons)
# print(analyzer.emoticons.todict('happy'))
# print(analyzer.emoticons.tolist())

#NER

# print(analyzer.ner)
# print(analyzer.ner.date.tolist())
# print(analyzer.ner.ip)
# print(analyzer.ner.ip.tolist())
# print(analyzer.ner.ip.fields())
# print(analyzer.ner.ip.todict(['country', 'source']))
# analyzer.ner.print_formatted()
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

#PARSER_DEP

# print(analyzer.parser_dependency)
# print(analyzer.parser_dependency.fields())
# print(analyzer.parser_dependency.tolist())
# print(analyzer.parser_dependency.tolist(True))
# print(analyzer.parser_dependency.todict(['dep', 'lemma', 'tag', 'sub']))

# print(analyzer.parser_dependency.tolist())
# print(analyzer.parser_dependency.tolist(True))
# print(analyzer.parser_dependency.todict(['source', 'dep', 'tag']))

#SENTIMENT

# print(analyzer.sentiment)
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
# analyzer.sentiment.subsentences_sentiments()

#NLU

# print(analyzer.nlu)
# print(analyzer.nlu.categories_unique('sub'))
# print(analyzer.nlu.categories_count('sub'))
# print(analyzer.nlu)
# print(analyzer.nlu.categories_unique('sub'))
# print(analyzer.nlu.categories_count('sub'))

test = analyzer.category_sentiment_by_subsentence('average',\
        filter = ['General', 'personnel', 'retrait', 'paiement', 'frais'], sample = 5)

for k,v  in test.items():
    print(k,v)
    print('')
print('')


#SENTENCE_ACT

# print(analyzer.sentence_acts)
# print(analyzer.sentence_acts.tolist('predict'))
# print(analyzer.sentence_acts.todict(['predict','probabilities']))

# print(analyzer.list_questions())


# A FINIR

# print(analyzer.synthesis)
# print(analyzer.synthesis.tolist())

#rajouter par sentence
#proposer filtre par tag
#renvoyer une liste par api + objet global

#proposer analyse document et phrase par phrase
#ressortir les questions
