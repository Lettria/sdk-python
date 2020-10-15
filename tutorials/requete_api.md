# Effectuer une requête API

Nous allons voir comment effectuer une requête à l'API Lettria et sauvegarder le retour dans un fichier afin de pouvoir le réutiliser à loisir.  

## Requête API

Tout d'abord on importe lettria et on initialise l'objet **NLP** qui va nous permettre de faire nos requêtes en lui passant une clé API valide.  
```python
	import lettria

	api_key = ' VOTRE CLE API'
	nlp = lettria.NLP(api_key)
```
Pour cet exemple et les prochains tutoriels nous allons utiliser le texte suivant que vous pouvez copier coller dans un fichier:  
  
```Paris est la ville la plus peuplée et la capitale de la France.  
Elle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l'Oise. Paris est également le chef-lieu de la région Île-de-France et le centre de la métropole du Grand Paris, créée en 2016. Elle est divisée en arrondissements, comme les villes de Lyon et de Marseille, au nombre de vingt. Administrativement, la ville constitue depuis le 1er janvier 2019 une collectivité à statut particulier nommée « Ville de Paris » (auparavant, elle était à la fois une commune et un département). L'État y dispose de prérogatives particulières exercées par le préfet de police de Paris. La ville a connu de profondes transformations sous le Second Empire dans les décennies 1850 et 1860 à travers d'importants travaux consistant notamment au percement de larges avenues, places et jardins et la construction de nombreux édifices, dirigés par le baron Haussmann.  
La ville de Paris comptait 2,19 millions d'habitants au 1er janvier 2016. L'agglomération parisienne s’est largement développée au cours du xxe siècle, rassemblant 10,73 millions d'habitants au 1er janvier 2016, et son aire urbaine (l'agglomération et la couronne périurbaine) comptait 12,57 millions d'habitants. L'agglomération parisienne est ainsi la plus peuplée de France, elle est la quatrième du continent européen et la 32e plus peuplée du monde au 1er janvier 2019.  
La position de Lutèce, sur l'île aujourd'hui nommée l'île de la Cité, permettant le franchissement du grand fleuve navigable qu'est la Seine par une voie reliant le Nord et le Sud des Gaules, en fait dès l'Antiquité une cité importante, capitale des Parisii, puis lieu de séjour d'un empereur romain. Sa position au centre du territoire contrôlé par les rois francs la fait choisir comme capitale de la France à la place de Tournai. Située au cœur d'un territoire agricole fertile avec un climat humide et doux, Paris devient une des principales villes de France au cours du xe siècle, avec des palais royaux, de riches abbayes et une cathédrale. Au cours du xiie siècle, avec l'université de Paris, la cité devient un des premiers foyers en Europe pour l’enseignement et les arts. Le pouvoir royal se fixant dans cette ville, son importance économique et politique ne cesse de croître. Ainsi, au début du xive siècle, Paris est l'une des villes les plus importantes du monde chrétien. Au xviie siècle, elle est la capitale de la principale puissance politique européenne ; au xviiie siècle, l'un des plus grands centres culturels de l’Europe ; et au xixe siècle, la capitale des arts et des plaisirs. Du xvie siècle au xxe siècle, Paris a été la capitale de l'Empire colonial français. Paris joue donc un rôle de tout premier plan dans l'histoire de l'Europe et du monde depuis des siècles.
```

Ouvrons notre fichier et lisons son contenu:  
```python
	with open("wiki.txt", "r") as f:
		wikipedia_data = f.readlines()
```
Nous sommes maintenant prêts à faire notre requête grâce a la fonction **add_document**.  
Cette fonction prend en argument une string ou une liste de string, elle va effectuer les requêtes nécessaires vers l'API de Lettria et ranger les resultats dans une instance de **Document**.  
Nous conseillons de décomposer vos données en 'documents' (un commentaire, un article de journal, un compte rendu ...) et d'appeler cette fonction sur chacun, vous pouvez passer un argument id pour les nommer et les retrouver plus facilement par la suite.  
Cette décomposition sera utilisée pour ranger les résultats et facilitera vos analyses, dans notre cas nous n'avons qu'un seul document à analyser:  
 ```python
	nlp.add_document(wikipedia_data)
	nlp.save_results('wikipedia_results.json')
```
Une fois la requête terminée, un nouveau fichier **wikipedia_results.json** doit s'etre crée, vos résultats sont prêts !  
Voyons maintenant comment manipuler l'objet NLP pour extraire vos résultats avec le prochain tutoriel [Utilisation de NLP](#Utilisation-de-NLP).  
  
### Ensemble du code
  
```python
	import lettria

	api_key = ' VOTRE CLE API'
	nlp = lettria.NLP(api_key)

	with open("wiki.txt", "r") as f:
		wikipedia_data = f.readlines()

	nlp.add_document(wikipedia_data)
	nlp.save_results('wikipedia_results.json')
```