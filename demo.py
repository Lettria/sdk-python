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

commentaires = [
    [
        "Of 444 patients, 76% were male. They had a mean age of 69 ± 10 years and LVEF of 28.2 ± 6.7%. HF was of ischemic etiology in 42% of cases and they were in NYHA class II (47.5%), III (50.0%) or IV (2.5%). On average, patients were active for 9% of the day (2 h 10 min). The physical activity decreased by approx. 10% with the onset of the lockdown (figure 1) and recovered within the following eight weeks. Comparison of the 28-days periods before, during and after the lockdown showed a statistically significant intra-individual decrease in physical activity (mean decrease 9 min per day) during the lockdown compared to pre- and post-lockdown values and a trend toward reduced mean heart rates. In parallel, a significant increase in device detected atrial arrhythmia burden (mean increase 17 min per day) was observed. All other parameters did not change significantly."
    ],
    [
        "We enrolled 34 consecutive patients with confirmed diagnosis of SARS-CoV-2 (mean age 62.45 ± 5.25years, 16male). Remote wireless rhythm monitoring was performed using portative ECG sensor.Average follow-up period was 21 days during in-hospital stage and 2 months after discharge."
    ],
    [
        "3416 consecutive patients were reviewed and 1476 finally enrolled (65.9 ± 20.9 years, 57.3% male). 76 (5.1%) patients had NAEs. Most of them were new atrial fibrillation episodes (48 patients, 3.2%), mostly seen in patients with no previous arrhythmia (38 patients, 79.2%). Atrial flutter (AFL) accounted for 20% of all NAEs. Ventricular arrhythmias were seen in 9 (0.6%) patients. Multivariable analysis showed that prior AFL, heart failure, dyslipidaemia, lopinavir/ritonavir, and combined hydroxychloroquine and azithromycin were independently associated with NAEs. 66 (86.8%) patients with NAEs died. The Kaplan-Meier analysis showed a lower survival of patients with NAEs (P < 0.001). Eight out of 9 (88.9%) and 41 out of 48 (85.4%) patients with ventricular arrhythmias and atrial fibrillation respectively died. Older age, male gender and NAEs were independently associated with death. NAEs and other outcomes, such as heart failure, thromboembolism, and bleeding independently predicted death."
    ]
]

commentaires = [
    "Nous avons enrollé 34 patients avec un diagnostic confirmé de SARS-COV-2 (âge moyen 62,45 ± 5.25ans, 16hommes)."
]

# ner_text = ["Je vais a Rome vendredi prochain avec 3 copains. En roulant a 130 km/h on devrait y etre en 9 heures depuis Lyon, c'est Pierre qui conduit.",
# 	"La fete nationale de la France est le 14 juillet, elle commémore la prise de la bastille le 14 juillet 1789."]

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRjIiwicHJvamVjdElkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRkIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExNjExZGM5MDMxMGQ4ZWJhMzIiLCJpYXQiOjE2MTgzMjAyOTAsImV4cCI6MTY2NjcwNDI5MH0.emln3t9ACFTFQH3uChi-fOAvJgBDHEqekzk4PGfYaZA"

nlp = lettria.NLP(api_key, no_print=False)

import json

# for c in commentaires:
    # nlp.add_document(c)

# nlp.save_results("results2.jsonl")
# nlp.load_results('results2.jsonl', reset=True)
# nlp.save_results("results_juisci.jsonl")
nlp.load_results('results_juisci.jsonl', reset=True)
# nlp.load_results('results.jsonl', reset=True)

# nlp = lettria.load_results('results.jsonl')
# for nlp in lettria.load_results('results.jsonl', chunksize=5):
#     for doc in nlp:
#         print(doc.str)

# nlp.add_document("j'ai 43 fils et filles.")

with open('pattern.json', 'r') as f:
    patterns = json.load(f)

# with open('pattern_dependency.json', 'r') as f:
#     patterns = json.load(f)

# for t in nlp.tokens:
#     print(t.str, t.pos, t.dep)

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
# exit()
# print(nlp.meaning)

for doc in nlp.documents:
    indexes = []
    for s, matches in doc.match_pattern(patterns, level='sentence'):
        # print(s.idx, s.str, matches)
        print(matches)
        indexes.append(s.idx)
        for m in matches:
            print(m)
            # for t in m:
                # print(t)
                # print(t.str, t.pos, t.idx, t.dep)
    # for s in doc.sentences:
    #     tmp = [t.str for t in s if t.str.lower() in ['them', 'they', 'patients', 'patient']]
    #     # print(s.idx, indexes)
    #     if tmp:
    #         if s.idx not in indexes and s.idx - 1 in indexes:
    #             indexes.append(s.idx)
    # res = (min(indexes), max(indexes))
    # print(doc.sentences[res[0]: res[1] + 1])
    # for k, val in matches.items():
    #     print("==>", k.upper())
    #     for m in val:
    #         for t in m:
    #             print(t.str, t.pos, t.idx, t.dep)
    #         print("")