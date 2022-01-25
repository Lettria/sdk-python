import lettria
import json

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRjIiwicHJvamVjdElkIjoiNWRlOGRiMzBlYzY4YjA1MWNmZmZiZGRkIiwic3Vic2NyaXB0aW9uSWQiOiI1ZDZkMjExNjExZGM5MDMxMGQ4ZWJhMzIiLCJpYXQiOjE2MTgzMjAyOTAsImV4cCI6MTY2NjcwNDI5MH0.emln3t9ACFTFQH3uChi-fOAvJgBDHEqekzk4PGfYaZA"
nlp = lettria.NLP(api_key, no_print=False)

commentaires = [
	'Mr. George Dupont est le boulanger du village.',
	"J'ai rencontré Madame Dubois en allant chez le fleuriste.",
	"La directrice de l'école est Mme Brigitte Fleur.",
	"Le Dr. Blorot m'a demandé si elle avait des antécédents dans ma famille car elle est malade."
]

# nlp.add_document(' '.join(commentaires))
# nlp.add_documents(commentaires)

nlp.load_result('./res_tmp.jsonl')

# nlp.documents[0].replace_coreference(attribute='source', replace=['CLS'])


import streamlit as st
from annotated_text import annotated_text

st.title('Demo coreference resolution')

# col1, col2 = st.columns(2)
col1 = st.columns(1)

# with col1:
st.write('Original text:')
spans = nlp.documents[0].spans
clusters = nlp.documents[0].clusters
text = [[' ' + k.str + ' ' for k in s] for s in nlp.documents[0].sentences]
    
for i, cluster in enumerate(clusters):
    for s in cluster.spans:
        text[s.sentence_idx][s.tokens_idx[0]:s.tokens_idx[-1] + 1] = [(' ' + t.str + ' ', str(i)) for t in s.tokens]
for sentence in text:
    annotated_text(
        *sentence
    )

# with col2:
#     st.write('With replacements:')
#     text = [' ' + t + ' ' for s in nlp.documents[0].replace_coreference(attribute='source') for t in s]
#     annotated_text(
#         *text
#     )