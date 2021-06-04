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
    ['Le garcon de ma voisine et de mon voisin est sympa, la fille du boulanger aussi']
]

# ner_text = ["Je vais a Rome vendredi prochain avec 3 copains. En roulant a 130 km/h on devrait y etre en 9 heures depuis Lyon, c'est Pierre qui conduit.",
# 	"La fete nationale de la France est le 14 juillet, elle commémore la prise de la bastille le 14 juillet 1789."]

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRjIiwicHJvamVjdElkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRkIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExNjExZGM5MDMxMGQ4ZWJhMzIiLCJpYXQiOjE2MTgzMjAyOTAsImV4cCI6MTY2NjcwNDI5MH0.emln3t9ACFTFQH3uChi-fOAvJgBDHEqekzk4PGfYaZA"

nlp = lettria.NLP(api_key, no_print=False)

import json

# for c in commentaires:
#     nlp.add_document(c)

# nlp.save_results("results2.jsonl")
# nlp.load_results('results2.jsonl', reset=True)
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
# print(nlp.pos)

for t in nlp.tokens:
    print(t.str, t.pos, t.dep)

## new functions emotion

# print(nlp.word_sentiment(filter_pos=['N'],average=True))
# print(nlp.word_sentiment(filter_pos=['N'],average=False))
# print(nlp.word_emotion(filter_pos=['N'],average=True))
# print(nlp.word_emotion(filter_pos=['N'],average=False))

# print(nlp.meaning_sentiment(filter_meaning=['action_heal'],average=True))
# print(nlp.meaning_sentiment(filter_meaning=['action_heal'],average=False))
# print(nlp.meaning_emotion(filter_meaning=['action_heal'],average=True))
# print(nlp.meaning_emotion(filter_meaning=['action_heal'],average=False))

# print(nlp.sentences[0].data['synthesis'][3])
# for t in nlp.sentences:
#     print([v.get('meaning', '') for v in t.data['synthesis']])
#     print(t.meaning)

# for sentence in nlp.sentences:
#     for t in sentence:
#         print(t.pos, t.str)
for doc, matches in nlp.match_pattern(patterns, level='sentence'):
    print(doc.str, matches)
    for k, val in matches.items():
        print(k)
        for m in val:
            for t in m:
                print(t.str, t.pos, t.idx, t.dep)
            print("")

# for sentence in nlp.sentences:
#     for sentence, matches in sentence.match_pattern(patterns):
#         print(sentence.str, matches)
#         for k, val in matches.items():
#             print(k)
#             for m in val:
#                 for t in m:
#                     print(t.str, t.pos, t.dep)

