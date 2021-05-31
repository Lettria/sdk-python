import lettria
from lettria import Sentiment

commentaires = [
    [
        "tres bien comme de habitude mais trop de attractions fermees pour un prix de plus en plus cher .",
        "il a fait tres beau et beaucoup de soleil"
    ],
    [
        "les enfant sont trop content en plus on a pu voir toutes les princesses ma petite derniere a adore.",
        "lhotel etait trop cher par contre mais bon cetait magique quand meme"
    ],
    [
        'Je vais bien mais mon ami est tres malade, je suis triste. 12 janvier 1992'
    ]
]

ner_text = ["Je vais a Rome vendredi prochain avec 3 copains. En roulant a 130 km/h on devrait y etre en 9 heures depuis Lyon, c'est Pierre qui conduit.",
	"La fete nationale de la France est le 14 juillet, elle commémore la prise de la bastille le 14 juillet 1789."]

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRjIiwicHJvamVjdElkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRkIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExNjExZGM5MDMxMGQ4ZWJhMzIiLCJpYXQiOjE1NzU1NDE1NTQsImV4cCI6MTYyMzkyNTU1NH0.dZCq-mv9oHGTCx6lW1GyxmYLehgD1OYg2RMObJueXH0"

nlp = lettria.NLP(api_key, no_print=False)

nlp.load_results('test.json', reset=True)

# nlp.add_document("nono@gmail.fr")

import json
with open('pattern.json', 'r') as f:
    pattern = json.load(f)
matches = nlp.match_pattern(pattern)

print(nlp.str)

# for doc in nlp:
#     for sent in doc:
#         for tok in sent:
#             print(tok.ner)

print(matches)