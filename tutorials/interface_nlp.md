# Utilisation de NLP

Avant de commencer à analyser nos résultats il est important de comprendre comment sont structurés les résultats obtenus afin de pouvoir chercher efficacement les informations que l'on veut:
- Au plus haut niveau nous avons l'objet **NLP** qui contient l'ensemble des données dans une liste de documents sous forme d'objets **Document**
- Chaque document contient une liste de phrases ou objets **Sentence**
- Chaque sentence peut contenir une ou plusieurs sous-phrases (objet **Subsentence**) et contient une liste de tokens (objet **Token**)
- Chaque subsentence peut aussi être decomposée en une liste de tokens (objet **Token**)

Cela peut sembler un peu abstrait au premier abord,  nous allons voir comment cela se traduit concretement en extrayant la liste des tokens a chaque niveau hierarchique par le biais de la propriété '.token'.
```python
	nlp.token
```
On obtient la liste des tokens sous un format \[liste de documents \[ liste de sentences \[ liste de tokens\]\]\]
>\[\[\['Paris', 'est', 'la', 'ville', 'la', 'plus', 'peuplee', 'et', 'la', 'capitale', 'de', 'la', 'France', '.'\], \['elle', 'se', 'situe', 'au', 'coeur', 'de', 'un', 'vaste', 'bassin', 'sedimentaire', 'aux', 'sols',    ...    le', 'plus', 'suivi', 'au', 'monde', '.'\]\]\]


```python
	for doc in nlp:
		print(doc.token)
```
On obtient à chaque ligne la liste des tokens sous un format \[ liste de sentences \[ liste de tokens\]\]. Peu de différences ici car nous n'avons qu'un seul document.
>\[\['Paris', 'est', 'la', 'ville', 'la', 'plus', 'peuplee', 'et', 'la', 'capitale', 'de', 'la', 'France', '.'\], \['elle', 'se', 'situe', 'au', 'coeur', 'de', 'un', 'vaste', 'bassin', 'sedimentaire', 'aux', 'sols',    ...    le', 'plus', 'suivi', 'au', 'monde', '.'\]\]

```python
	for doc in nlp:
		for sentence in doc:
			print(sentence.token)

	for doc in nlp:
		for sentence in doc:
			for sub in sentence.subsentences:
				print(sub.token)
```
On obtient à chaque ligne la liste des tokens sous un format \[liste de tokens\].
> \['Paris', 'est', 'la', 'ville', 'la', 'plus', 'peuplee', 'et', 'la', 'capitale', 'de', 'la', 'France', '.'\]
> ...
> \['Paris', 'accueille', 'egalement', 'de', 'nombreuses', 'competitions', ... 'plus', 'suivi', 'au', 'monde', '.'\]

```python
for doc in nlp:
	for sentence in doc:
		for token in sentence:
			print(token.token)
```
On obtient à chaque ligne un token:
> Paris <br/>
> ... <br/>
> monde <br/>
> . <br/>

Des accès directs sont aussi possibles afin de rendre l'interface plus pratique à utiliser:

	for token in nlp.tokens:
	for sentence in nlp.sentences:
	for subsentence in nlp.subsentences:
	for token in nlp.documents[0].tokens:
	...

Par exemple pour extraire les tokens (.token) et POS tags (.pos) du premier document de vos données on peut utiliser la syntaxe suivante:
```python
for t in nlp.documents[0].tokens:
	print(t.token, t.pos)
```
> Paris NP <br/>
est V<br/>
la D<br/>
ville N<br/>
la D<br/>
plus RB<br/>
peuplee VP<br/>
...

La liste des propriétés accessibles est disponible dans la documentation.<br/>
Toutes les propriétés au niveau 'global' et 'document' proposent aussi une variante `_flat` (i.e. token_flat) qui permet de retour une liste aplatie.
