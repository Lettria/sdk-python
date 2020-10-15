# Nettoyer un jeu de données

En utilisant les résultats obtenus dans **Effectuer une requête API** nous allons voir comment manipuler et extraire les résultats de Lettria.  
Commencons par créer notre objet NLP (il n'y a pas besoin de fournir une clé API car nous n'allons pas faire de nouvelle requête) et utilisons **load_results** pour charger notre fichier json contenant les résultats de notre requête.  
```python
	import lettria
	nlp = lettria.NLP()
	nlp.load_results('wikipedia_results.json')
```
  
## Extraction de données
Maintenant que nous connaissons la syntaxe à utiliser nous allons extraire les tokens, les lemmas, les POS (Part of Speech) tags pour chaque phrase.  
```python
	data = []
	for sentence in nlp.sentences:
		tmp = []
		for tok, lem, tag in  zip(sentence.token, sentence.lemma, sentence.pos):
			tmp.append((tok, lem, tag))
		data.append(tmp)
```  
Pour chaque phrase nous obtenons la liste des tokens, lemmas et tag, puis nous construisons des tuples (token, lemma, tag) que nous stockons dans une liste pour chaque phrase.  
Visualisons le résultat:  
```python
	for data_sentence in data:
		print(data_sentence)
```  
> \[('Paris', 'Paris', 'NP'), ('est', 'etre', 'V'), ('la', 'le', 'D'), ('ville', 'ville', 'N'), ('la', 'le', 'D'), ('plus', 'plus', 'RB'), ('peuplee', 'peupler', 'VP'), ('et', 'et', 'CC'), ('la', 'le', 'D'), ('capitale', 'capitale', 'N'), ('de', 'de', 'P'), ('la', 'le', 'D'), ('France', 'France', 'NP'), ('.', '.', 'PUNCT')\] ...  
  
Parfait ! En quelques lignes nous avons pu extraire des données pertinentes qui peuvent être facilement enregistrées sous format json ou csv.  
Nous n'avons utilisé que les champs .token .pos et .lemma mais de nombreux autres propriétés sont disponibles, la liste exhaustive est disponible dans la documentation.  
  
## Extraction du vocabulaire
L'objet NLP permet aussi d'extraire directement le vocabulaire de vos données, en utilisant soit les tokens soit les lemmas et en ayant la possibilité de filtrer par tag.  
Les résultats sont sous la forme d'un couple (mot, tag) ce qui permet de différencier les mots qui ont plusieurs types possibles (etre: nom commun et verbe).  
  
Extraction de tous les noms propres du texte:  
```python
	nlp.vocabulary(filter_pos=['NP'])
```  
> \[('Paris', 'NP'), ('France', 'NP'), ('Seine', 'NP'), ('Marne', 'NP'), ('Oise', 'NP'), ('Ile-de-France', 'NP'), ('Lyon', 'NP'), ('Marseille', 'NP'), ('Ville', 'NP'), ('Etat', 'NP'), ('e plus', 'NP'), ('Lutece', 'NP'), ('Cite', 'NP'), ('Parisii', 'NP'), ('Tournai', 'NP'), ('Europe', 'NP')\]  
  
Extraction de tous les lemmas de verbe:  
```python
	nlp.vocabulary(filter_pos=['V', 'VP'], lemma=True)
```  
>\[('etre', 'V'), ('peupler', 'VP'), ('situer', 'V'), ('temperer', 'VP'), ('creer', 'VP'), ('diviser', 'VP'), ('constituer', 'V'), ('nommer', 'VP'), ('disposer', 'V'), ('exercer', 'VP'), ('connaitre', 'V'), ('consister', 'V'), ('diriger', 'VP'), ('compter', 'V'), ('developper', 'V'), ('rassembler', 'V'), ('permettre', 'V'), ('controler', 'VP'), ('faire', 'V'), ('situer', 'VP'), ('devenir', 'V'), ('fixer', 'V'), ('cesser', 'V'), ('jouer', 'V')\]
  
On peut aussi compter les occurences des mots filtrés avec la fonction word_count():  
```python
	nlp.word_count(filter_pos=['JJ'], lemma=True)
```  
> {('vaste', 'JJ'): 1, ('sedimentaire', 'JJ'): 1, ('fertile', 'JJ'): 2, ('parisien', 'JJ'): 3, ('grand', 'JJ'): 3, ('particulier', 'JJ'): 2, ('profond', 'JJ'): 1, ('second', 'JJ'): 1, ('important', 'JJ'): 3, ('large', 'JJ'): 1, ('nombreux', 'JJ'): 1, ('xxe', 'JJ'): 2, ('urbain', 'JJ'): 1, ('periurbain', 'JJ'): 1, ('quatrieme', 'JJ'): 1, ('europeen', 'JJ'): 2, ('32', 'JJ'): 1, ('navigable', 'JJ'): 1, ('romain', 'JJ'): 1, ('franc', 'JJ'): 1, ('agricole', 'JJ'): 1, ('humide', 'JJ'): 1, ('doux', 'JJ'): 1, ('principal', 'JJ'): 2, ('xe', 'JJ'): 1, ('royal', 'JJ'): 2, ('riche', 'JJ'): 1, ('xii', 'JJ'): 1, ('premier', 'JJ'): 2, ('economique', 'JJ'): 1, ('politiquer', 'JJ'): 2, ('xif', 'JJ'): 1, ('chretien', 'JJ'): 1, ('xvii', 'JJ'): 1, ('xviii', 'JJ'): 1, ('culturel', 'JJ'): 1, ('xixe', 'JJ'): 1, ('xvi', 'JJ'): 1, ('colonial', 'JJ'): 1, ('francais', 'JJ'): 1}
  
Enfin à la place des occurences on peut aussi obtenir les fréquences d'apparition des mots filtrés avec la fonction word_frequency():  
```python
	nlp.word_frequency(filter_pos=['JJ'], lemma=True)
```  
>{('vaste', 'JJ'): 0.0019305019, ('sedimentaire', 'JJ'): 0.0019305019, ('fertile', 'JJ'): 0.0038610039, ('parisien', 'JJ'): 0.0057915058, ('grand', 'JJ'): 0.0057915058, ('particulier', 'JJ'): 0.0038610039, ('profond', 'JJ'): 0.0019305019, ('second', 'JJ'): 0.0019305019, ('important', 'JJ'): 0.0057915058, ('large', 'JJ'): 0.0019305019, ('nombreux', 'JJ'): 0.0019305019, ('xxe', 'JJ'): 0.0038610039, ('urbain', 'JJ'): 0.0019305019, ('periurbain', 'JJ'): 0.0019305019, ('quatrieme', 'JJ'): 0.0019305019, ('europeen', 'JJ'): 0.0038610039, ('32', 'JJ'): 0.0019305019, ('navigable', 'JJ'): 0.0019305019, ('romain', 'JJ'): 0.0019305019, ('franc', 'JJ'): 0.0019305019, ('agricole', 'JJ'): 0.0019305019, ('humide', 'JJ'): 0.0019305019, ('doux', 'JJ'): 0.0019305019, ('principal', 'JJ'): 0.0038610039, ('xe', 'JJ'): 0.0019305019, ('royal', 'JJ'): 0.0038610039, ('riche', 'JJ'): 0.0019305019, ('xii', 'JJ'): 0.0019305019, ('premier', 'JJ'): 0.0038610039, ('economique', 'JJ'): 0.0019305019, ('politiquer', 'JJ'): 0.0038610039, ('xif', 'JJ'): 0.0019305019, ('chretien', 'JJ'): 0.0019305019, ('xvii', 'JJ'): 0.0019305019, ('xviii', 'JJ'): 0.0019305019, ('culturel', 'JJ'): 0.0019305019, ('xixe', 'JJ'): 0.0019305019, ('xvi', 'JJ'): 0.0019305019, ('colonial', 'JJ'): 0.0019305019, ('francais', 'JJ'): 0.0019305019}
  
## Ensemble du code
  
```python
	import lettria
	nlp = lettria.NLP()
	nlp.load_results('wikipedia_results.json')
	data = []
	for sentence in nlp.sentences:
		tmp = []
		for tok, lem, tag in  zip(sentence.token, sentence.lemma, sentence.pos):
			tmp.append((tok, lem, tag))
		data.append(tmp)

	for data_sentence in data:
		print(data_sentence)

	print(nlp.vocabulary(filter_pos=['NP']))
	print(nlp.vocabulary(filter_pos=['V', 'VP'], lemma=True))
	print(nlp.word_count(filter_pos=['JJ'], lemma=True))
	print(nlp.word_frequency(filter_pos=['JJ'], lemma=True))
```
