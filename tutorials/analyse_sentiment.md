# Analyse de sentiments

L'analyse sentimentale consiste à identifier pour un texte s'il à une connotation négative, positive ou neutre.  
Lettria analyse les sentiments au niveau de la subsentence, ce qui permet une analyse très fine des données et permet de gérer les phrases plus nuancées.  
  
Pour obtenir les résultats de cette analyse deux choix s'offrent à nous:  
- Utiliser les propriétés 'sentiment' avec l'objet **NLP** comme vu précédemment.  
- Utiliser le module lettria.Sentiment qui propose des fonctionnalités plus avancées.  
  
Nous allons découvrir cette deuxième option en analysant quelques commentaires :  
```python
data = ['Excellent accueil avec notre bébé. Endroit chaleureux et en plein centre ville. Nous avons très bien mangé.',
'Excellent accueil. Une équipe très serviable. Des plats délicieux. Parfait pour les enfants. Je recommande !',
'Un excellent restaurant !',
'Je suis decu car le plat etait mauvais et froid. Par contre le personnel etait tres sympathique']
```  
Chaque item de cette liste correspond à un commentaire, pour faciliter notre travail nous allons considérer que un commentaire = un document.  
Commençons par faire nos requêtes et sauvegarder le résultat dans un fichier json.  
```python
	import lettria
	
	nlp = lettria.NLP(api_key)
	for commentaire in data:
		nlp.add_document(commentaire)
	nlp.save_results('commentaires.json')
```
Le module sentiment prend en paramètre l'objet nlp qu'il utilise pour extraire les données.  
```python
	import lettria
	from lettria import Sentiment
	
	nlp = lettria.NLP()
	nlp.load_results('commentaires.json')
	sentiment = Sentiment(nlp)
```
  
## Analyse par phrases
  
Commençons par identifier les phrases positives et négatives avec **filter_polarity** qui va nous renvoyer une liste d'objets **Sentence**:  
```python
	print('\nPositive Sentences:')
	positive_sentences = sentiment.filter_polarity('positive')
	for p in positive_sentences:
	    print(p.str)

	print('\nNegative Sentences:')
	negative_sentences = sentiment.filter_polarity('negative')
	for n in negative_sentences:
	    print(n.str)
```
```
Positive Sentences:  
excellent accueil avec notre bebe .  
endroit chaleureux et en plein centre ville .  
nous avons mange tres bien .  
excellent accueil .  
une equipe tres serviable .  
des plats delicieux .  
parfait pour les enfants .  
je recommande !  
un excellent restaurant !  
par contre le personnel etait tres sympathique  
  
Negative Sentences:  
je suis decu car le plat etait mauvais et froid  
```
On peut aussi analyser les 'subsentences' en ajoutant un argument 'granularity', par la même occasion nous allons aussi afficher la valeur sentimentale associée:  
```python  
	print('\nNegative Sentences')  
	negative_sentences = sentiment.filter_polarity('negative', granularity='subsentence')  
	for n in negative_sentences:  
	    print(n.str, n.sentiment)  
```
```
Negative Sentences  
je suis decu {'positive': 0, 'negative': -0.27, 'total': -0.27}  
car le plat etait mauvais et froid {'positive': 0, 'negative': -0.46, 'total': -0.46}  
```
## Analyse par commentaire 
  
Ces informations sont utiles mais dans notre cas nous nous intéressons a la polarité des commentaires eux-mêmes.  
Pour cela nous pouvons utiliser **get_sentiment** qui permet d'obtenir les sentiments au niveau souhaité (global, document, sentence ou subsentence):  
```python
doc_sentiments = sentiment.get_sentiment(level='document')
for d in doc_sentiments:
    print(d)
```
```
{'positive': {'sum': 2.4185, 'occurences': 3, 'average': 0.8062}, 'negative': {'sum': 0, 'occurences': 0, 'average': 0}, 'total': {'sum': 2.42, 'occurences': 3, 'average': 0.8067}}  
{'positive': {'sum': 3.2306, 'occurences': 5, 'average': 0.6461}, 'negative': {'sum': 0, 'occurences': 0, 'average': 0}, 'total': {'sum': 3.23, 'occurences': 5, 'average': 0.646}}  
{'positive': {'sum': 0.56, 'occurences': 1, 'average': 0.56}, 'negative': {'sum': 0, 'occurences': 0, 'average': 0}, 'total': {'sum': 0.56, 'occurences': 1, 'average': 0.56}}  
{'positive': {'sum': 0.51, 'occurences': 1, 'average': 0.51}, 'negative': {'sum': -0.38, 'occurences': 1, 'average': -0.38}, 'total': {'sum': 0.13, 'occurences': 2, 'average': 0.065}}  
```
On obtient pour chaque commentaire le score de chaque polarité ainsi que le score total.  
```python
for score, com in zip(doc_sentiments, data):
    print(score['total']['average'], com)
```
```
0.8067 Excellent accueil avec notre bébé. Endroit chaleureux et en plein centre ville. Nous avons très bien mangé.
0.646 Excellent accueil. Une équipe très serviable. Des plats délicieux. Parfait pour les enfants. Je recommande !
0.56 Un excellent restaurant !
0.065 Je suis decu car le plat etait mauvais et froid. Par contre le personnel etait tres sympathique
```
Les trois premiers commentaires positifs sont correctement evalués. Le dernier commentaire présente un avis mitigé qui se reflète par un score proche de 0.  

## Analyser le sentiment des mots
On peut pousser l'analyse en ne s'arrêtant pas simplement aux phrases. En associant aux mots qui composent une phrase ou sous-phrase la valeur sentimentale de cette dernière, on peut construire un dictionnaire avec le sentiment moyen associé à l'utilisation d'un mot.  
Essayons d'extraire les sentiments des noms communs, en utilisant les lemma pour plus de fiabilité.  
```python
sentiment.word_sentiment(lemma=True, filter_pos = ['N'])
```
```
{'endroit': 0.9, 'accueil': 0.56, 'contre': 0.51, 'bebe': 0.56, 'personnel': 0.51, 'equipe': 0.85, 'restaurant': 0.56, 'plat': -0.025, 'centre ville': 0.9, 'enfant': 0.66}
```
La plupart des commentaires étant positifs les mots sont dans l'ensemble positifs, a l'exception de 'plat' qui apparaît à la fois dans un commentaire positif et négatif.  
Il peut être pratique de regrouper les mots faisant reference à la même idée, par exemple 'equipe', 'personnel' et 'accueil' font référence à la qualité du service client.  

## Analyser les 'meanings'  

Le concept de meaning correspond a la catégorisation d'un mot selon son sens afin de le regrouper avec d'autres mots similaires et simplifier l'analyse. Les dictionnaires Lettria peuvent etre personnalisés en associant à chaque mot ou lemma une catégorie (ou meaning) nouvelle ou existante.  
  
Pour cet exemple nous avons ajouté une catégorie 'service' aux mots 'accueil', 'equipe', 'personnel'.  
```python
sentiment.meaning_sentiment()
```  
```
{'Localisation': 0.685, 'city': 0.51, 'Destination': 0.76, 'action_disappoint': -0.38, 'action_accept': -0.38, 'Position': 0.685, 'Substitution': 0.66, 'action_heal': -0.38, ...,  'action_move': -0.38}
```
Afin d'avoir un résultat plus lisible et comme nous ne nous intéressons qu'a la catégorie 'service':  
```python
sentiment.meaning_sentiment(filter_meaning=['service'])
```
```
{'service': 0.62}
```
  
En utilisant astucieusement les dictionnaires et l'analyse sentimentale, on peut mesurer la satisfaction sur differents critères à partir d'une liste de commentaires !  

## Ensemble du code
```python
import lettria
from lettria import Sentiment

nlp.load_results('commentaires.json')
sentiment = Sentiment(nlp)

print('\nPositive Sentences')
positive_sentences = sentiment.filter_polarity('positive', granularity='subsentence')
for p in positive_sentences:
    print(p.str, p.sentiment)

print('\nNegative Sentences')
negative_sentences = sentiment.filter_polarity('negative', granularity='subsentence')
for n in negative_sentences:
    print(n.str, n.sentiment)

doc_sentiments = sentiment.get_sentiment(level='document')
for d in doc_sentiments:
    print(d)

for score, com in zip(doc_sentiments, data):
    print(score['total']['average'], com)

print(sentiment.word_sentiment(lemma=True, filter_pos = ['N']))
print(sentiment.meaning_sentiment(filter_meaning=['service']))
```