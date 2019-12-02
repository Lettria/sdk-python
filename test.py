import lettria
from lettria.analyzeClass import Analyzer

api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWQ5YjczOTE2MWRjZjk0Njc3ZDM5MWQwIiwicHJvamVjdElkIjoiNWQ5YjczOTE2MWRjZjk0Njc3ZDM5MWQxIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExMjExZGM5MDMxMGQ4ZWI5OTgiLCJpYXQiOjE1NzEyMTg4NDUsImV4cCI6MTYxOTYwMjg0NX0.kjRt3Y9_TBnEy8SiGzIOTPrJLLJiyXBtP6osVc8Nikk'

client = lettria.Client(key=api_key, raw=False)
phrase1 = "Je :) mange du poulet a 4 heures du matin. 23/07/1192. 12.143.43.123 Hier, 3 km/h 12 km 145.247.145.1 Henri est vraiment devenu fou. 124.53.111.3 :-) :D XD"
# phrase2 = "Jack Nicholson /d͡ʒæk ˈnɪkəlsən/1 est un acteur, réalisateur et scénariste américain, né le 22 avril 1937 à Neptune (New Jersey). Il a joué un grand nombre de rôles principaux ou secondaires, principalement des personnages sombres, d'anti-héros, de personnages odieux, d'éternel marginal, de vagabond sardonique, de rebelle contre la société2, voire de fou, dans de nombreux films culte du cinéma américain comme Easy Rider, Chinatown, Vol au-dessus d'un nid de coucou, Batman, Mars Attacks!, Pour le pire et pour le meilleur, Les Infiltrés, Shining, et du cinéma européen comme Profession : reporter. Avec douze nominations et trois récompenses, il fait partie des acteurs les plus nommés et récompensés aux Oscars du cinéma."
# ret = client.request(phrase)
# print(ret.data[0].get_judgement_items())
# exit()

# phrase1 = "J'ai mange un sandwich."

analyzer = Analyzer(client)
# ret = client.request(phrase)
analyzer.request(phrase1)
# analyzer.request(phrase2)
analyzer.analyze_document()

# print(analyzer.emoticons)
# print(analyzer.emoticons.todict())
# print(analyzer.emoticons.tolist())

# print(analyzer.ner)
# print(analyzer.ner.date.tolist())
# print(analyzer.ner.ip)
# print(analyzer.ner.ip.tolist())
# print(analyzer.ner.ip.todict())

# analyzer.ner.list_entities(detail = True)
# analyzer.ner.date.print_formatted()
# print(analyzer.ner.date.todict(['source', 'ISO', 'timestamp']))
# test = analyzer.ner.get_entities()

print(analyzer.ner.list_entities())

# print(analyzer.postagger.tolist())
# print(analyzer.postagger.tolist(tuple = True))

# print(analyzer.parser_dependency)
# print(analyzer.parser_dependency.fields())
# print(analyzer.parser_dependency.todict(['dep', 'lemma', 'tag', 'sub']))


# print(analyzer.postagger.tolist(True))
# print(analyzer.postagger.fields())

# print(analyzer.parser_dependency.tolist())
# print(analyzer.parser_dependency.tolist(True))
# print(analyzer.parser_dependency.todict(['source', 'dep', 'tag']))

#rajouter par sentence
#proposer filtre par tag
#renvoyer une liste par api + objet global

#proposer analyse document et phrase par phrase
#ressortir les questions
