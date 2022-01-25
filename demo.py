import lettria

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

commentaires = [
	"I have 48 bananas, 32 pears and one apple."
]

commentaires = [
	"3416 consecutive patients were reviewed and 1476 finally enrolled (65.9 ± 20.9 years, 57.3% male). 76 (5.1%) patients had NAEs. Of 444 patients, 76% were male. They had a mean age of 69 ± 10 years."
]


api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRjIiwicHJvamVjdElkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRkIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExNjExZGM5MDMxMGQ4ZWJhMzIiLCJpYXQiOjE2MTgzMjAyOTAsImV4cCI6MTY2NjcwNDI5MH0.emln3t9ACFTFQH3uChi-fOAvJgBDHEqekzk4PGfYaZA"

nlp = lettria.NLP(api_key, no_print=False)

import json

# commentaires = [
#	 "..."
# ]

# nlp.load_results('results_hotel_angleterre_preprocessed.json')
# nlp.load_results('results_hotel_halle_preprocessed.json')

# for c in commentaires:
#	 nlp.add_document(c, verbose=False)
# nlp.add_document('Les chiens sont très triste de ne pas pour venir avec nous. Mais je suis content de partir en vacances')



commentaires = [
	'Mr. George Dupont est le boulanger du village.',
	"J'ai rencontré Madame Dubois en allant chez le fleuriste.",
	"La directrice de l'école est Mme Brigitte Fleur.",
	"Le Dr. Blorot m'a demandé si elle avait des antécédents dans ma famille car elle est malade."
]

# nlp.add_document(' '.join(commentaires))
# nlp.add_documents(commentaires)

nlp.load_result('res_tmp.jsonl')
# nlp.save_result('res_tmp.jsonl')

# docs = [doc1, doc2, doc3, doc4]
# print(docs)

# print("\nskip\n")
# nlp.add_documents(docs, skip_document=True, verbose=True)#, document_ids=['a','b','c','d'])
# nlp.add_documents(docs, skip_document=True, verbose=True, document_ids=['a','b','c','d'])
# # nlp.add_documents(docs, skip_document=True, verbose=True, document_ids=['e','f','g','h'])
# # nlp.add_documents(docs, skip_document=True, verbose=True)#, document_ids=['a','b','c','d'])

# print("\nNo skip\n")
# nlp.add_documents(docs, skip_document=False)#, document_ids=['a','b','c','d'])
# nlp.add_documents(docs, skip_document=False, document_ids=['a','b','c','d'])
# # nlp.add_documents(docs, skip_document=False, document_ids=['e','f','g','h'])
# # nlp.add_documents(docs, skip_document=False)#, document_ids=['a','b','c','d'])

# docs = [
# 	['salut ca va!!', 'il est la']
# ]

# for d in docs:
# 	nlp.add_document(d, skip_document=True, id='test')
# 	print()
# 	print()
# 	nlp.add_document(d, skip_document=False, id='test2')
# 	print()
# 	print()
# 	nlp.add_document(d, skip_document=False)
# 	print('====================')

# nlp.save_results("doc")
# nlp.load_results("doc", reset=True)

# print([d.id for d in nlp])

# for s in nlp:
# 	# for t in s:
# 	# 	print(t)
# 	print(f"s.str:		  {s.str_doc}")
# 	# print(f"s.spans:	  {s.span}")
# 	# print(f"s.clusters:	  {s.cluster}")
# 	# print(f"s.str_original: {s.original_text}")
# 	# print(f"s.tokens: {' '.join(s.token_flat)}")
# 	# print(f"s.sentiment: {s.sentiment}")
# 	# print(f"s.sentiment_ml: {s.sentiment_ml}")
# 	# print(f"s.emotion: {s.emotion}")
# 	# print(f"s.emotion_ml: {s.emotion_ml}")
	
# 	for t in s.tokens:
# 		print(t, t.spans)
# 		print(t, t.clusters)

# 	for cl in s.clusters:
# 		print('cluster:', cl)
# 		print("head:   ", cl.head)
# 		# for sp in cl:
# 		# 	print('=====>', sp)
# 	print()
# 	# print("\nSpans")
# 	# for s in s.spans:
# 	# 	print('==>', s, s.cluster_idx, s.sentence_idx)

nlp.documents[0].replace_coreference(attribute='source', replace=['CLS'])

exit()

patterns = {
	"pattern": [
		{'LOWER':{"IN":['docteur', 'monsieur', 'madame']}},
		{'POS':"NP"}
	]
}

patterns = {
	"patients" : [
			{
			"RIGHT_ID": "rootnode",
			"RIGHT_ATTRS": {"LEMMA":"attaquer"}
			},
			{
			"LEFT_ID": "rootnode",
			"REL_OP": ">",
			"RIGHT_ID": "sujet",
			"RIGHT_ATTRS": {"DEP": "nsubj"}
			},
			{
			"LEFT_ID": "rootnode",
			"REL_OP": ">",
			"RIGHT_ID": "objet",
			"RIGHT_ATTRS": {"DEP": "obj"}
			},
			{
			"LEFT_ID": "objet",
			"REL_OP": ">",
			"RIGHT_ID": "objet_conj",
			"RIGHT_ATTRS": {"DEP": "conj"}
			}
		]
}

patterns = {
	"pattern_adjectif":
	 [  
		{
		  "RIGHT_ID" : "qualificatif",
		  "RIGHT_ATTRS": {"POS": {"IN": ["V"]}}
		},
		{
		  "LEFT_ID": "qualificatif",
		  "REL_OP": ">>",
		  "RIGHT_ID": "support",
		  "RIGHT_ATTRS": {"POS":"NP", "OP":"+"}
		}
	 ],
  }

# print()
for s, matches in nlp.match_pattern(patterns, level='sentence', print_tree=False, skip_errors=False):
	print(s, matches)

# for t in nlp.sentences:
#	 # print()
#	 # print(t)
#	 for s, matches in t.match_pattern(patterns, level='sentence', print_tree=False, skip_errors=False):
#		 print(matches, s.str)
#		 pass

# for s, matches in nlp.match_pattern(patterns, level='sent'):
#	 print(s, matches)

# for s, matches in nlp.match_pattern(patterns, level='sub'):
#	 print(s, matches)

# with open('pattern_dependency.json', 'r') as f:
#	 patterns = json.load(f)

# for s, matches in nlp.match_pattern(patterns, level='doc'):
#	 print(s, matches)

# for s, matches in nlp.match_pattern(patterns, level='sent'):
#	 print(s, matches)

# for s, matches in nlp.match_pattern(patterns, level='sub'):
#	 print(s, matches)

# for t in nlp.tokens:
#	 print(t.str, t.pos, t.dep, t.ner)

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
#	 print([v.get('meaning', '') for v in t.data['synthesis']])
#	 print(t.meaning)

# for sentence in nlp.sentences:
#	 for t in sentence:
#		 print(t.pos, t.str)
# exit()

# for doc in nlp.documents:
#	 indexes = []
# for s, matches in nlp.match_pattern(patterns, level='sent'):
#	 print(s.idx, s.str, matches)
	# print(s, matches)
	# for k, val in matches.items():
	#	 for m in val:
	#		 for t in m:
	#			 # print(t   )
	#			 print(t.str, t.pos, t.idx, t.dep)
