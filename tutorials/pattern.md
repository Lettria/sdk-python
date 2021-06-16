# Pattern matching

L'utilisation de patterns peut vous permettre d'identifier des informations précises dans un texte non structuré.  
Les patterns se basent sur les informations qui sont obtenues suite à l'analyse de vos documents par l'API compréhension de Lettria.  
Ainsi chaque information (tel que lemma, POS tag, type d'entité, catégorie...) peut être utilisée et combinée avec d'autre pour rechercher des structures précises de phrases.  
  
Il existe deux types de patterns:  
- **Token Patterns** permettant de construire des patterns simples en suivant l'ordre des tokens dans la phrase.  
- **Dependency Patterns** faisant usage de l'arbre de dépendance pour créer des patterns plus complexes basés sur la structure grammaticale de la phrase .  
  
Une fois vos patterns crées vous pouvez les utiliser sur votre texte pour retrouver les documents, phrases ou tokens qui y correspondent.  
On peut voir les patterns comme une forme évoluée des expressions régulières (regex), ils permettent des comportements plus avancés ainsi que d'accèder et d'analyser facilement le contexte autour de vos matchs.  
  
Nous allons découvrir ensemble comment utiliser ces deux types de patterns dans des cas simples.

## Token Pattern

Les Token Pattern peuvent être utilisés pour retrouver des structures suivants certaines règles grâce à une liste d'attributs qui servent de filtre. 

Attribut|Description
---|---
ORTH|Texte du token.
TEXT|Texte du token.
LOWER|Texte du token en minuscule.
LEMMA|Lemma du token.
POS|Part-Of-Speech tag du token.
DEP|Dependency tag du token.
ENT_TYPE|Type d'entité du token (voir NER API).
CATEGORY_SUPER|Categorie "SUPER" du token (voir Meaning API).
CATEGORY_SUB|Categorie "SUB" du token (voir Meaning API).
LENGTH|Longueur du token.
IS_ALPHA|Token est composé de alphabectics characters.
IS_ASCII|Token est composé de ASCII characters.
IS_DIGIT|Token est composé de digits.
IS_LOWER|Token est en minuscule.
IS_UPPER|Token est en majuscule.
IS_TITLE|Token est en titlecase.
IS_PUNCT|Token est un caractère de poncutation.
IS_SPACE|Token est un caractère space.
IS_SENT_START|Token est le premier de la phrase.
LIKE_NUM|Token est un nombre.
LIKE_URL|Token est une entité type URL.
LIKE_EMAIL|Token est une entité type email.
OP|Opérateur pour modifier le type de matching.

Le matching entre le pattern et le texte se fait dans l'ordre des tokens, si les structures que vous souhaitez retrouver ne respectent pas cet ordre alors il vaut probablement mieux utiliser un Dependency Pattern.  

**Example**

Commençons par analyser phrases simples, nous allons extraire d'un texte les noms propres précédes de la mention monsieur , madame ou docteur.  
Avant de démarrer le matching de pattern il faut d'abord effectuer une requête a l'API Lettria pour analyser le texte.  

```python
import lettria

text = [
    'Mr. George Dupont est le boulanger du village.',
    "J'ai rencontré Madame Dubois en allant chez le fleuriste.",
    "La directrice de l'école est Mme Brigitte Fleur.",
    "Le Dr. Blorot m'a demandé si j'avais des antécédents dans ma famille."
]

nlp = lettria.NLP(api_key)

for document in text:
    nlp.add_document(document)

print(nlp)
```
```python
[
    ['monsieur George Dupont est le boulanger du village.'],
    ['Je ai rencontre Madame Dubois en allant chez le fleuriste.'],
    ['La directrice de le ecole est madame Brigitte Fleur.'],
    ['Le docteur Blorot me a demande si je avais des antecedents dans ma famille.']
]
```

L'analyse par lettria procède à certaines modifications qui simplifient l'analyse de texte, ainsi tous les mentions 'Mr.' sont remplacées automatiquement par la forme longue 'monsieur'.   
Notre pattern va donc comporter deux composantes:  
-Match un token dont le texte est soit 'monsieur', 'madame' ou 'docteur'.  
-Match un token dont le POS tag est nom propre.  

```python
patterns = {
    "person": [
        {'LOWER':{"IN":['docteur', 'monsieur', 'madame']}},
        {'POS':"NP"}
    ]
}

for s, matches in nlp.match_pattern(patterns, level='doc'):
    print(s.str , matches)
```
```python
{'pattern': [[monsieur, George Dupont]]}['monsieur George Dupont est le boulanger du village.']
{'pattern': [[madame, Dubois]]}         ['Je ai rencontre Madame Dubois en allant chez le fleuriste.']
{'pattern': [[madame, Brigitte Fleur]]} ['La directrice de le ecole est madame Brigitte Fleur.']
{'pattern': [[docteur, Blorot]]}        ['Le docteur Blorot me a demande si je avais des antecedents dans ma famille.']
```
La fonction match_pattern nous renvoie ici le document qui a matché ainsi que les tokens précis qui correspondent au pattern, les deux sont des objets dont on peut extraire d'autres informations si nécessaires.  
On peut remarquer dans notre exemple que notre pattern indique un seul nom propre, pourtant nous obtenons un match avec 'monsieur George Dupont'. Cela s'explique par le fait que Lettria peut fusionner les noms propres qui se suivent pour avoir un token qui correspond à une entité (ici une personne).  
  
Pour des patterns plus complexes il est possible d'utiliser des opérateurs et des modificateurs. Les opérateurs permettent de modifier le comportement de matching d'un pattern en permettant de matcher plusieurs tokens pour une même étape, ou rendre l'étape optionnel.  
  
Operateur|Description
---|---
?|L'étape du pattern est optionnelle (match 0 ou 1 fois)
+|L'étape du pattern peut match au moins 1 token.
*|L'étape du pattern peut match 0 ou plusieurs tokens.
!|L'étape du pattern est inversé et doit match 0 fois.
.|Opérateur par défaut, l'étape doit match 1 token.

Les modificateurs permettent de spécifier les valeurs à match à une étape donnée du pattern. L'opérateur IN que nous avons utilisé permet de spécifier une liste de valeurs qui peuvent match.  

Attribute Modifier|Description
---|---
IN|La valeur de l'attribut est dans cette liste.
NOT_IN|La valeur de l'attribut n'est pas dans cette liste.
ISSUBSET|La valeur de l'attribut est un sous-ensemble de cette liste.
ISSUPERSET|La valeur de l'attribut a pour sous-ensemble cette liste. 
==, >, <, >=, <=|Pour comparaisons d'entiers, la valeur de l'attribut est égale, plus grande ou moins grande.

## Dependency Pattern
Les Dependency Patterns se basent sur le Dependency Parser qui construit un arbre grammatical de la phrase.  
Ce type de pattern suit une syntaxe différente car le matching ne se fait plus dans l'ordre des tokens mais par rapport aux relations grammaticales qui lient les tokens les uns aux autres.  
  
Un Dependency Pattern est défini par une liste de dictionnaire qui suit le format suivant:  
  
Nom|Description
---|---
LEFT_ID|Nom du node gauche dans la relation, il doit avoir été défini précédemment.
REL_OP|Operateur qui décrit la relation entre le node gauchet et le node droit.
RIGHT_ID|Nom du node droit dans la relation (le node qui est en train d'être défini)
RIGHT_ATTRS|Les attributs qui doivent match avec le node droit, ils sont définis de la même façon que pour les Token Patterns.
  
Chaque node doit présenter les 4 champs sauf le node 'root' qui ne contient que les champs 'RIGHT_ID' et 'RIGHT_ATTRS'.  
Chaque pattern doit comporter un et un seul root node.  
Pour aller avec cette nouvelle syntaxe d'autres opérateurs doivent être utilisés:
  
Operateur|Description
---|---
<|A depend directement de B.
\>|A est le parent de B.
<<|A depend de B directement ou indirectement.
\>>|A est le parent de B directement ou indirectement.
.|A token précède directement B: A.idx == B.idx - 1.
.*|A token est avant B: A.idx < B.idx.
;|A token suit directement B: A.idx == B.idx + 1.
;*|A token est après B: A.idx > B.idx.
$+|A est un frère de B (même parent) et précede directement B: A.idx == B.idx - 1.
$-|A est un frère de B (même parent) et suit directement B: A.idx == B.idx + 1.
$++|A est un frère de B (même parent) et est avant B: A.idx < B.idx.
$--|A est un frère de B (même parent) et est après B: A.idx > B.idx.

Essayons d'analyser precisement la phrase suivante en obtenant le sujet et l'objet de l'action.  
```python
"Microsoft a attaque Apple et Samsung en justice pour concurrence deloyale."
```

Notre pattern comportera quatre étapes:
-Le lemma du verbe que nous souhaitons attraper, le verbe de la phrase est toujours la 'racine' dans un arbre de dépendance. 
-Un enfant de cette racine qui aura comme tag de dépendance 'nsubj' (sujet du verbe).
-Un enfant de cette racine qui aura comme tag de dépendance 'obj' (objet du verbe).
-S'il y a plusieurs objets ceux-ci seront enfants du premier objet et auront le tag 'conj'.

```python
patterns = {
    "legal" : [
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
```

```python
for s, matches in nlp.match_pattern(patterns, level='doc', print_tree=True):
    print(s.str , matches)
```

En utilisant ce pattern on obtient le résultat suivant:

```python
a attaque [1](root) V root
|______Microsoft [0](nsubj) NP nsubj
|______Apple [2](obj) NP obj
|	|______Samsung [4](conj) NP conj
|	|	|______et [3](cc) CC cc
|______justice [6](obl) N obl
|	|______en [5](case) P case
|______concurrence [8](obl) N obl
|	|______pour [7](case) P case
|	|______deloyale [9](amod) JJ amod
|______. [10](punct) PUNCT punct

{'legal': [[a attaque, Microsoft, Apple, Samsung]]} ['Microsoft a attaque Apple et Samsung en justice pour concurrence deloyale.']
```
L'option print_tree nous permet d'imprimer l'arbre de dependance afin de voir la structure grammaticale de la phrase.  
Les résultats retournés sont dans l'ordre des étapes du pattern, Microsoft correspond donc bien au sujet et Apple et Samung aux objets du verbe.  
En utilisant ce pattern nous pouvons donc identifier dans des textes des cas d'attaques ainsi que les sujets et objets de ces attaques. Il est bien sur possible d'élargir le pattern en rajoutant des verbes ou en utilisant une catégorie à la place d'un lemma pour attraper tous les verbes qui auraient un sens similaire dans ce contexte.
  
Pour plus de détails n'hésitez pas à consulter la documentation liée au SDK.

## Ensemble du code
```python

import lettria
text = [
    'Mr. George Dupont est le boulanger du village.',
    "J'ai rencontré Madame Dubois en allant chez le fleuriste.",
    "La directrice de l'école est Mme Brigitte Fleur.",
    "Le Dr. Blorot m'a demandé si j'avais des antécédents dans ma famille."
]

nlp = lettria.NLP(api_key)

for document in text:
    nlp.add_document(document)

patterns = {
    "person": [
        {'LOWER':{"IN":['docteur', 'monsieur', 'madame']}},
        {'POS':"NP"}
    ]
}

for s, matches in nlp.match_pattern(patterns, level='doc'):
    print(s.str , matches)

nlp.reset_data()
text = "Microsoft a attaque Apple et Samsung en justice pour concurrence deloyale."
nlp.add_document(text)

patterns = {
    "legal" : [
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

for s, matches in nlp.match_pattern(patterns, level='doc', print_tree=True):
    print(s.str , matches)
```
