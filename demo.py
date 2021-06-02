import lettria
from lettria import Sentiment

commentaires = [
    [
        "tres bien comme de habitude mais trop de attractions fermees pour un prix de plus en plus cher .",
        "il a fait tres beau et beaucoup de soleil"
    ],
    [
        "les enfant sont trop content en plus on a pu voir toutes les princesses, ma petite derniere a adore.",
        "l'hotel etait trop cher par contre mais bon cetait magique quand meme"
    ],
    [
        'Je vais bien mais mon ami est tres malade, je suis triste. 12 janvier 1992'
    ]
]

commentaires = [
    ['ma fille est tres belle, son ami et amant est charmant']
]

# ner_text = ["Je vais a Rome vendredi prochain avec 3 copains. En roulant a 130 km/h on devrait y etre en 9 heures depuis Lyon, c'est Pierre qui conduit.",
# 	"La fete nationale de la France est le 14 juillet, elle commémore la prise de la bastille le 14 juillet 1789."]

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRjIiwicHJvamVjdElkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRkIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExNjExZGM5MDMxMGQ4ZWJhMzIiLCJpYXQiOjE2MTgzMjAyOTAsImV4cCI6MTY2NjcwNDI5MH0.emln3t9ACFTFQH3uChi-fOAvJgBDHEqekzk4PGfYaZA"

nlp = lettria.NLP(api_key, no_print=False)

import json

# for c in commentaires:
    # nlp.add_document(c)

# nlp.save_results("results.jsonl")
nlp.load_results('results.jsonl', reset=True)

# nlp = lettria.load_results('results.jsonl')
# for nlp in lettria.load_results('results.jsonl', chunksize=5):
#     for doc in nlp:
#         print(doc.str)

# with open('pattern.json', 'r') as f:
#     patterns = json.load(f)


with open('pattern_dependency.json', 'r') as f:
    patterns = json.load(f)

# print(nlp.str)

# print(nlp.str)
# for doc in nlp:
#     for sent in doc:
#         for tok in sent:
#             print(tok.ner)

# matches = nlp.match_pattern(patterns, level='documents')
# print("GLOB DOC", matches)
# for match in matches:
    # for k,v in match.items():
        # print(k, v.str)
for sentence in nlp.sentences:
    for t in sentence:
        print(t.pos, t.str)
for doc, matches in nlp.match_pattern(patterns, level='sentence'):
    print(doc.str, matches)
    # for k, val in matches.items():
    #     print(k)
    #     for m in val:
    #         for t in m:
    #             print(t.str, t.pos, t.dep)

# for sentence in nlp.sentences:
#     for sentence, matches in sentence.match_pattern(patterns):
#         print(sentence.str, matches)
#         for k, val in matches.items():
#             print(k)
#             for m in val:
#                 for t in m:
#                     print(t.str, t.pos, t.dep)

