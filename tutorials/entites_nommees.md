# Récupérer les entités nommées dans un texte

Le NER ("Named Entity Recognition" ou Reconnaissance d'entités nommées en francais) est un problème commun en NLP qui consiste à extraire d'un texte des entités et classer dans des catégories prédéfinies (date, organisation, vitesse, masse...).  

Lettria permet d'extraire et de manipuler pas moins de 40 entités différentes.  [Voir la liste exhaustive des entités gérées par l'API Lettria.](https://doc.lettria.com/#entities)  

Si vous souhaitez en savoir plus sur les entités nommées, et leurs usages,  [rendez-vous sur notre fiche explicative.](https://lettria.com/fr/dev/toolsheets/ner)  

Pour cet exemple nous allons utiliser les données suivantes, riches en entités:  
```python
data = ["Je vais a Rome vendredi prochain avec 3 copains. En roulant a 130 km/h on devrait y etre en 9 heures depuis Lyon, c'est Pierre qui conduit.",
"La fete nationale de la France est le 14 juillet, elle commémore la prise de la bastille le 14 juillet 1789."]
```
Vous pouvez bien sur aussi utiliser les résultats obtenus dans  **Effectuer une requête API** pour ce tutorial.  

## Requête API

```python
	import lettria

	api_key = ' VOTRE CLE API'
	nlp = lettria.NLP(api_key)
	
	data = ["Je vais a Rome vendredi prochain avec 3 copains. En roulant a 130 km/h on devrait y etre en 9 heures depuis Lyon, c'est Pierre qui conduit.",
	"La fete nationale de la France est le 14 juillet, elle commémore la prise de la bastille le 14 juillet 1789."]
		
	nlp.add_document(data)
	nlp.save_results('ner_results.json')
```

## Extraction d'entités

Notre objet **NLP** nous permet d'obtenir une vue d'ensemble des entités détectées dans nos données par la méthode ``list_entities``.  
```python
	entities = nlp.list_entities(level='global')
	for entity in entities:
	    print(entity)
```

```
{'person': ['Pierre'], 'location': ['Rome', 'Lyon', 'France'], 'date': ['vendredi prochain', '14 juillet', '14 juillet 1789'], 'number': ['3'], 'speed': ['130km/h'], 'duration': ['en 9 heures']}
```

On peut aussi décomposer cette liste par documents, sentences ou subsentences:
```python
	entities = nlp.list_entities(level='document')
	for entity in entities:
	    print(entity)
```
```
{'person': ['Pierre'], 'location': ['Rome', 'Lyon'], 'date': ['vendredi prochain'], 'number': ['3'], 'speed': ['130km/h'], 'duration': ['en 9 heures']}
{'location': ['France'], 'date': ['14 juillet', '14 juillet 1789']}
```
Il est aussi possible d'obtenir les entités en utilisant l'interface classique de **NLP**.
Cela permet aussi d'obtenir plus de détails sur nos entités:
```python
for t in nlp.tokens:
    print(t.token, t.ner)    
```
```
je 	 {'value': {'scalar': 1}}  
vais 	 {}  
a 	 {}  
Rome 	 {'type': ['location']}  
vendredi prochain 	 {'type': ['date',], 'value': {'ISO': '2020-09-04', 'formatted': 'Friday 04 September 2020 00:00:00', 'timestamp': 1599177600, 'chronology': 'future', 'chronology_day': 10, 'confidence': 0.99}}  
...  
en 9 heures 	 {'type': ['duration'], 'value': {'preposition': {'source': 'en', 'category': ['Temporal Localisation', 'Localisation', 'Duration']}, 'seconds': 32400, 'minutes': 540, 'hours': 9, 'days': 0.375, 'weeks': 0.05357142857142857, 'months': 0.0125, 'years': 0.001026694045174538, 'confidence': 0.99}}  
...  
14 juillet 1789 	 {'type': ['date'], 'value': {'ISO': '1789-07-14', 'formatted': 'Tuesday 14 July 1789 00:00:00', 'timestamp': -5694969600, 'chronology': 'past', 'chronology_day': 84413, 'confidence': 0.99}}  
. 	 {}  
```
Pour chaque token on obtient le ou les types possibles d'entités ainsi que les valeurs associées, par exemple les dates sont converties en format ISO et les durées sont converties en format numérique. 

### Ensemble du code
```python
	import lettria

	nlp = lettria.NLP()
	
	nlp.load_results("ner_results.json")
		
	entities = nlp.list_entities(level='global')
	for entity in entities:
	    print(entity)

	entities = nlp.list_entities(level='document')
	for entity in entities:
	    print(entity)

	for t in nlp.tokens:
	    print(t.token, t.ner)    
```