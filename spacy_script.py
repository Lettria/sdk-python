import spacy
from spacy.matcher import DependencyMatcher

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

nlp = spacy.load("en_core_web_sm")
matcher = DependencyMatcher(nlp.vocab)

pattern = [
            {
            "RIGHT_ID": "rootnode",
            "RIGHT_ATTRS": {"LEMMA": {"IN":["patient", "patients"]}}
            },
            {
            "LEFT_ID": "rootnode",
            "REL_OP": ">>",
            "RIGHT_ID": "num",
            "RIGHT_ATTRS": {"DEP":"nummod"}
            }
        ]

pattern2 = [
            {
            "RIGHT_ID": "rootnode",
            "RIGHT_ATTRS": {"LEMMA": {"IN":["patient", "patients"]}}
            },
            {
            "LEFT_ID": "rootnode",
            "REL_OP": "<<",
            "RIGHT_ID": "num",
            "RIGHT_ATTRS": {"DEP":"nummod"}
            }
        ]

matcher.add("patient", [pattern])
# matcher.add("patient2", [pattern2])

for d in commentaires:
    doc = nlp(d[0])
    # for t in doc:
    #     print(t.lemma_, t.dep_)
    matches = matcher(doc)
    # print(matches)
    for m in matches:
        print(doc[m[1][0]], doc[m[1][1]])