# Python SDK

```python
import lettria

nlp = lettria.NLP(api_key)
nlp.add_document([sentence_1, sentence_2])

for doc in nlp:
	for sentence in doc:
		print(sentence.token, sentence.pos)
```

To use our API, you will need a personal key, refered as API_KEY. Get your free API_KEY on your [Dashboard](https://app.lettria.com/dashboard/subscription).  
Install using Python Software Developpement Kit :  

`pip install lettria`

Check the official sources for more information and documentation on how to extract key informations using our SDK : [https://github.com/Lettria/sdk-python](https://github.com/Lettria/sdk-python)

##  _NLP class_

**NLP** inherits from [TextChunk](#textchunk).

**NLP** is a class designed to give access to relevant data at the different levels (document, sentence, subsentence) in an intuitive way. It allows to perform quick data exploration, manipulation and analysis.  
It is also used to perform requests and can save and load the result as JSON objects.

When a response from the API is received it is stored in a hierarchy of classes:  
**NLP** (all data) => **Document** => **Sentence** => **Subsentence** => **Token**  
At each level direct access to inferior levels is possible i.e. ``nlp.sentences`` gives access to a list of all the **Sentence** in the current data, while ``nlp.documents[0].sentences`` gives only the **Sentence** of the first **Document**.

NLP is iterable and will yield **Document** instances.

### Attributes / Properties

Name|Type|Description
---|---|---
documents|list of [Document](#document-class) instances|List of all the **Document** instances.
sentences|list of [Sentence](#sentence-class) instances|Direct access to all of the **Sentences** instances.
subsentences|list of [Subsentence](#subsentence-class) instances|Direct access to all of the **Subsentence** instances.
tokens|list of [Token](#token-class) instances|Direct access to all **Token** in the subsentence
fields|list of string|List of all common properties accessible at all levels (token, pos etc.)
client|instance of [Client](#client-class)|Client used for performing request to Lettria's API
[Common properties](#common-properties)|depends on property|Properties allowing access to specific data (pos, token etc.)

### Methods

<b>Data management</b>

METHOD|DESCRIPTION
---|---
[add_document()](#add_document)|Submits document to API
[save_results()](#save_results)|Saves data from json file
[load_results()](#load_results)|Loads data from json file
[add_client()](#load_results)|Adds new client / api_key

### add_document

`add_document(document, skip_document = False, id=None)`

Performs a request to lettria API using the API_KEY provided.
Results are appended as an additional **Document instance** to the <b>documents</b> attribute.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
document|string or list of string|Data to be sent to the API|False
skip_document|bool|Whether to skip the document if there is a problem during processing|True
id|str|Id to identify the document, by default an incrementing integer is assigned.|True

### save_results

`save_results(file = '')`

Writes current results to a JSON file. If no file is specified the default path is results_X.json with X being next 'free' integer.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
file|string|Path of file to write in.|True

### load_results

`load_results(path = 'results_0', reset = False)`

Loads results from a JSON file.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
file|string|Path of file to load.|True
reset|bool|Whether to erase current data.|True

### add_client

`add_client(client = None, api_key = None)`

Replaces current client with provided one, or creates a new client using the provided api_key.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
client|instance of Client class|Client instance to replace the current one.|True
api_key|string|Key to use for the new client.|True





## _TextChunk_

**TextChunk** is the base class of **NLP**, **Document**, **Sentence** and **Subsentence**.  
It offers different methods that can be accessed through children classes.

<b>Data analysis:</b>

METHOD|DESCRIPTION
---|---
[vocabulary()](#vocabulary)|Returns vocabulary from current data.
[word_count()](#word_count)|Returns word count from current data.
[word_frequency()](#word_frequency)|Returns word frequency of current data.
[list_entities()](#list_entities)|Returns dictionaries of detected entities by type.
[get_emotion()](#get_emotion)|Returns emotion results at the specified hierarchical level
[get_sentiment()](#get_sentiment)|Returns sentiment results at the specified hierarchical level
[word_sentiment()](#word_sentiment)| Returns average sentiment for each word of the whole vocabulary
[meaning_sentiment()](#meaning_sentiment)|Returns average sentiment for each **meaning**
[filter_polarity()](#filter_polarity)|Filters **Sentence** or **Subsentence** of the specified polarity
[filter_emotion()](#filter_emotion)|Filters **Sentence** or **Subsentence** of the specified emotions
[filter_type()](#filter_type)|Filters **Sentence** of the specified types

### vocabulary

`vocabulary(filter_pos = None, lemma=False)`

Returns vocabulary from current data with their associated POStag i.e. if a word appears both as a verb and a noun it will be in two tuples (word, 'V'), (word, 'N').
Allows filtering by POS tags.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
filter_pos|list of string|Tags to use for filtering.|True
lemma|string|Whether to use lemma or plain words.|True
<br/>

**Return**:

Type|Description
---|---
list of tuple|List of unique tuples (token, POStag).

### word_count

`word_count(filter_pos = None, lemma=False):`

Returns count of words from current data with their associated POStag i.e. if a word appears both as a verb and a noun it will be in two tuples (word, 'V'), (word, 'N').
Allows filtering by POS tags.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
filter_pos|list of string|Tags to use for filtering.|True
lemma|string|Whether to use lemma or plain words.|True
<br/>

**Return**:

Type|Description
---|---
dictionary|dictionary of word counts { (token, POStag): occurences }.

### word_frequency

`word_frequency(filter_pos = None, lemma=False)`

Returns words or lemma frequency, allows filtering by POS tag

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
filter_pos|list of string|Tags to use for filtering.|True
lemma|bool|Whether to use lemma or plain words.|True
<br/>

**Return**:

Type|Description
---|---
dictionary|Dictionary of word frequency

### list_entities

`list_entities()`

Returns dictionaries of detected entities by type.

**Return**:

Type|Description
---|---
list of dictionary|List of dictionaries of different entities at the specified level.


### get_emotion
``get_emotion(granularity = 'sentence')``

Returns emotion results, **granularity** defines whether to use emotion by sentence or by subsentence.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
granularity|string|Level at which emotions are analyzed. <br>One of 'sentence' or 'subsentence'.|True

**Return**:

Type|Description
---|---
list of dict|List of dictionaries with emotions as keys and dict {'occurences','sum','average'} as values.


### get_sentiment
``get_sentiment(granularity = 'sentence')``

Returns sentiment results, **granularity** defines whether to use sentiment by sentence or by subsentence.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
granularity|string|Level at which sentiments are analyzed. <br>One of 'sentence' or 'subsentence'.|True

**Return**:

Type|Description
---|---
list of dict|List of dictionaries with polarity as keys and dict {'occurences','sum','average'} as values.


### word_sentiment
``word_sentiment(granularity = 'sentence', lemma = False, filter_pos = None)``

Returns an average sentiment score for each word or lemma.
For each sentence or subsentence (**granularity** parameter), the sentiment score is added to each of the words present. The scores are divided by the number of sentences or subsentences to get an average.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
granularity|string|Whether to use sentiment by 'sentence' or 'subsentence' for scoring.|True
lemma|bool|Whether to use lemma or plain words.|True
filter_pos|list of string| POStags to use for filtering.|True

**Return**:

Type|Description
---|---
dictionary|Dictionary with words as keys and sentiment as value


### meaning_sentiment
``meaning_sentiment(granularity='sentence', filter_meaning=None)``

Returns average sentiment score for each **meaning**
For each sentence or subsentence(**granularity** parameter), the sentiment score is added to each of the meaning present. The scores are divided by the number of sentences or subsentences to get an average.
This can be used with custom **meaning** to get the sentiment associated with customer service or pricing when analyzing reviews.  

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
granularity|string|Whether to use sentiment by 'sentence' or 'subsentence' for scoring.|True
filter_meaning|list of string|Filters results by list of meanings|True


**Return**:

Type|Description
---|---
dictionary|Dictionary with meanings as keys and sentiment as value

### filter_polarity
``filter_polarity(polarity, granularity='sentence')``

Filters **Sentence** or **Subsentence** of the specified polarity.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
polarity|string or list of string|Polarity, 'neutral', 'positive', 'negative'.|False
granularity|string|Whether to use sentiment by 'sentence' or 'subsentence' for scoring.|True

**Return**:

Type|Description
---|---
list of instances of **Sentence** or **Subsentence**|List of instances of objects with the specified polarity.


### filter_emotion
``filter_emotion(emotions, granularity='sentence')``

Filters **Sentence** of the specified emotions.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
emotions|string or list of string|Emotions to filter, one of 'joy', 'love', 'surprise', 'anger', 'sadness', 'fear' or 'neutral'.|False
granularity|string|Whether to use sentiment by 'sentence' or 'subsentence' for scoring.|True

**Return**:

Type|Description
---|---
list of instances of **Sentence** or **Subsentence**|List of instances of objects with the specified emotion.

### filter_type
``filter_type(sentence_type)``

Filters **Sentence** of the specified emotions.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
sentence_type|string or list of string|Types to filter, one of 'assert', 'command', 'question_open', 'question_closed'.|False

**Return**:

Type|Description
---|---
list of instances of **Sentence**|List of instances of **Sentence** with the specified type.

## _Document Class_

**Document** inherits from [TextChunk](#textchunk).

**Document** stores the information for a document (for example an online review for a product or a news article).
The class is iterable and will yield instances of **Sentence**.

### Attributes / Properties

Name|Type|Description
---|---|---
sentences|list of [Sentence](#sentence-class) instances|List of **Sentences** of the document.
subsentences|list of [Subsentence](#subsentence-class) instances|Direct access to list of **Subsentence** for the document.
id|str|Id of document, by default sequential integer if not provided.
[common properties](#common-properties)|depends on property|Properties allowing access to specific data (pos, token etc.).

## _Sentence Class_

**Sentence** inherits from [TextChunk](#textchunk).  

**Sentence** stores data for a sentence. Sentences are delimited automatically from the input raw text. For longer and more complicated sentences it can be advantageous to further cut the sentences into subsentences.

**Sentence** is iterable and will yield instances of **Token** class

### Attributes / Properties

Name|Type|Description
---|---|---
subsentences|list of [Subsentence](#subsentence-class) instances|List of **Subsentence** in the sentence
tokens|list of [Token](#token-class) instances|List of **Token** in the sentence
[common properties](#common-properties)|depends on property|Properties allowing access to specific data (pos, token etc.)

## _Subsentence Class_
**Subsentence** stores data relative to a part of a sentence. For longer and more complicated sentences it can be advantageous to cut it in multiple pieces to have a more detailed analysis.

For example:
``I liked the park but it was raining and the weather was cold`` would be cut into:

``I liked the park ``
``but it was raining``
``and the weather was cold``

In this case it allows to perform more precise sentiment analysis than assigning a score to the whole sentence.

**Subsentence** is iterable and will yield instances of **Token** class.

### Attributes / Properties

Name|Type|Description
---|---|---
tokens|list of [Token](#token-class) instances|List of **Token** in the subsentence
[common properties](#common-properties)|depends on property|Properties allowing access to specific data (pos, token etc.)

## _Token Class_
**Token** stores data relative to a specific token. Tokens are delimited according to our Tokenizer.

### Attributes / Properties

Name|Type|Description
---|---|---
[common properties](#common-properties)|depends on property|Properties allowing access to specific data (pos, token etc.)

## _Common properties_

These properties are accessible at all analysis levels : **NLP**, **Document**, **Sentence**, **Subsentence**, **Token**.

All properties have a **_flat** variant (token_flat) which flatten recursively the return.

Name|type|Description
---|---|---
str|String|Returns sentence as string
token|String|Returns token
lemma|String|Returns lemma
lemma_detail|String|Returns unmerged lemma
pos|String|Returns POS (Part-Of-Speech) tags
pos_detail|String|Returns unmerged POS (Part-Of-Speech) tags
dep|String|Returns dependency relations
morphology|String|Returns morphological features
language|String|Returns detected language
meaning|List of Tuples|Returns meanings as tuples (SUPER, SUB)
emotion|Tuple|Returns emotion as tuple (Type, score)
sentiment|Dictionary|Returns sentiment with positive, negative and total values
sentiment_ml|Dictionary|Returns sentiment of ml_model without further fine tuning
sentiment_target|Tuple|Returns 'target' of words with strong sentimental meaning
sentence_type|String|Returns type of sentence
coreference|String|Returns reference of token if it exists
synthesis|Dictionary|Returns synthesis object

## _Sentiment Class_

!!! **Sentiment** is deprecated as 5.0.2 and may be removed in future releases, all methods are now available at all levels through the functional interface, cf [TextChunk](#textchunk).  !!!

  
**Sentiment** provides methods to perform some specific sentiment and emotion analysis.
It takes as input an instance of **NLP**  and uses it to retrieve data.

```python
import lettria
from lettria import Sentiment
nlp = lettria.NLP(api_key)
nlp.add_document(['sentence 1', 'sentence 2'])

sentiment = Sentiment(nlp)
```

### Attributes / Properties

Name|Type|Description
---|---|---
nlp|[NLP class](#nlp-class)|Instance of NLP class

### Methods

Name|Description
---|---
[get_emotion()](#get_emotion)|Returns emotion results at the specified hierarchical level
[get_sentiment()](#get_sentiment)|Returns sentiment results at the specified hierarchical level
[word_sentiment()](#word_sentiment)| Returns average sentiment for each word of the whole vocabulary
[meaning_sentiment()](#meaning_sentiment)|Returns average sentiment for each **meaning**
[filter_polarity()](#filter_polarity)|Filters **Sentence** or **Subsentence** of the specified polarity
[filter_emotion()](#filter_emotion)|Filters **Sentence** or **Subsentence** of the specified emotions

### get_emotion
``get_emotion(level='document')``

Returns emotion results at the specified hierarchical level.
For example **get_emotion(level='document')** will concatenate emotion  at the document level and return a list of emotions for each **Document**.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
level|string|Hierarchical level at which results are concatened. <br>One of 'global', 'document', 'sentence', 'subsentence'.|True

**Return**:

Type|Description
---|---
list of dict|List of dictionaries with emotions as keys and dict {'occurences','sum','average'} as values.


### get_sentiment
``get_sentiment(level='document')``

Returns sentiment results at the specified hierarchical level
For example **get_sentiment(level='document')** will concatenate sentiment  at the document level and return a list of emotions for each **Document**.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
level|string|Hierarchical level at which results are concatened. <br>One of 'global', 'document', 'sentence', 'subsentence'.|True

**Return**:

Type|Description
---|---
list of dict|List of dictionaries with polarity as keys and dict {'occurences','sum','average'} as values.


### word_sentiment
``word_sentiment(granularity = 'sentence', lemma = False, filter_pos = None)``

Returns an average sentiment score for each word or lemma in the data.
For each sentence or subsentence, the sentiment score is added to each of the words in the phrase. The scores are divided by the number of occurences to get an average.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
granularity|string|Whether to use sentiment by 'sentence' or 'subsentence' for scoring.|True
lemma|bool|Whether to use lemma or plain words.|True
filter_pos|list of string| POStags to use for filtering.|True

**Return**:

Type|Description
---|---
dictionary|Dictionary with words as keys and sentiment as value


### meaning_sentiment
``meaning_sentiment(granularity='sentence', filter_meaning=None)``

Returns average sentiment score for each **meaning**
For each sentence or subsentence, the sentiment score is added to each of the meaning in the phrase. The scores are divided by the number of occurences to get an average.
For example, this can be used with custom **meaning** to get a sentiment associated with customer service or pricing when analyzing reviews.


**Parameters**:

Name|Type|Description|Optional
---|---|---|---
granularity|string|Whether to use sentiment by 'sentence' or 'subsentence' for scoring.|True
filter_meaning|list of string|Filters results by list of meanings|True


**Return**:

Type|Description
---|---
dictionary|Dictionary with meanings as keys and sentiment as value

### filter_polarity
``filter_polarity(polarity, granularity='sentence')``

Filters **Sentence** or **Subsentence** of the specified polarity.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
polarity|string|Polarity, one of 'neutral', 'positive', 'negative'.|False
granularity|string|Whether to use sentiment by 'sentence' or 'subsentence' for scoring.|True

**Return**:

Type|Description
---|---
list of instances of **Sentence** or **Subsentence**|List of instances of objects with the specified polarity.


### filter_emotion
``filter_emotion(emotions, granularity='sentence')``

Filters **Sentence** of the specified emotions.


**Parameters**:

Name|Type|Description|Optional
---|---|---|---
emotions|list of string|Emotions to filter.|False
granularity|string|Whether to use sentiment by 'sentence' or 'subsentence' for scoring.|True


**Return**:

Type|Description
---|---
list of instances of **Sentence** or **Subsentence**|List of instances of objects with the specified emotions.

## _Client Class_
**Client** used to perform requests to our API.

### Attributes / Properties

Name|Type|Description
---|---|---
key|string|The API_KEY that will be used by the client.

### Methods

METHOD|DESCRIPTION
---|---
[request()](#request)|Send a request to our API

### request

`request(text)`

Performs a request to lettria API using the API_KEY provided.

**Parameters**:

Name|Type|Description|Optional
---|---|---|---
text|string|Text data to be sent to the API|False

**Return**:

Type|Description
---|---
list of dictionary|Each of these objects represents the informations collected for a sentence.
