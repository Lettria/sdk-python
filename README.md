


<br/>

![](https://lettria.com/images/logo.png)


# Introduction

Lettria's official SDK for Python.

Learn more about our API and its format with our [documentation](https://doc.lettria.com) and [demo](https://lettria.com/demo).

# Overview
* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
	* [Client](#class-client)
	* [Classes available if raw is False](#classes-available-if-raw-is-false)
		* [Data](#class-data)
		* [Sentence](#class-sentence)
			* [ner](#class-ner)
			* [nlu](#class-nlu)
			* [nlp](#class-nlp)
			* [sentiment](#class-sentiment)
			* [emoticons](#class-emoticons)
			* [parser_dependency](#class-parser_dependency)
			* [postagger](#class-postagger)
			* [sentence_acts](#class-sentence_acts)
			* [coreference](#class-coreference)
		* [SharedClass](#class-sharedclass)
		* [ExtractClass](#class-extractclass)


# Installation

  ### pip (recommended)

Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a package manager for Python.

	pip install lettria

If you dont' have pip, you can install it by running this from the command line:

	$ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

  ### source code

You can [download the source code](https://github.com/Lettria/sdk-python/zipball/master "Lettria python sdk source code") and then run:

	python setup.py install

# Usage


```python
import lettria

client = lettria.Client('API_KEY')
response = client.request("my first sentence. my second sentence")
```

# `class Client`

Client used to perform requests to our API.

### Parameters:

|name|type|description | mandatory| default value
|--|--|--|--|--|
|`key`|`string`| The `API_KEY` that will be used by the client.<br/>Get your [free key](https://app.lettria.com/signup).|Yes|`None`|
|`raw`|`boolean`| Tell the client if it should return the raw json from our API or  a class [Data](#class-data) containing methods that you may want to use on the elements. More [here](#raw-disabled)|No|`True`

### Example
```
client = Client(key="API_KEY", raw=True)
```

### Methods:

|name|description | return value|
|--|--|--|
| `request()` | Send a request to our [API](https://lettria.com)  | `list` of objects.<br />Each of these objects represents the informations collected for a sentence. More information on our format on our [documentation](https://doc.lettria.com)
|`getKey()`|Retrieve the key used by the client|`string` representing your `API_KEY`.
|`setKey()`|Set the key that will be used bu the client| `boolean` that represent the operation status:<br/>`True` for success<br/>`False` for error


## `.request(text, [options...])`

Send a request to our [API](https://lettria.com/)

### Parameters:

|name|type|description | default value
|--|--|--|--|
|`text`|`string`| The text that you want to analyse|Empty string
|`raw`|`boolean`| Tell the client if it should return the raw json from our API or a list of classes containing methods that you may want to use on the elements. It will override the client's `raw` value| The value that was previously set on the client which has `True` as default.

### Return value:

|condition|value|
|--|--|
|`raw=True`|`list` of objects, which is the raw return of our API. more [here](https://doc.lettria.com)|
|`raw=False`|`list` of `Sentence`. Each of them contains the data per sentence and a toolkit of methods that you may want to use on them.

## `.getKey()`

Returns the  `API_KEY` used by the client as a `string`.

## `.setKey(API_KEY)`

Set the `API_KEY` that will be used by your client.

<br/><br/>

# Classes available if raw is false

When the `raw` parameter is disabled, the client will return a `class Data`

# `class Data`

Contains the data for each sentences in your text input as `Sentence` instances, and some methods to perform actions on them.

### Methods:

|name|description | return value|
|--|--|--|
|`getSentence()`|Returns the `Sentence` at the given index.|`class Sentence`
|`readSentence()`|Returns the `Sentence` classes one by one.|`class Sentence`
|`getNumberOfSentences()`|Returns the number sentences|`int`
| `map()` | Apply a function to all `Sentence` elements. |`boolean` that represent the operation status:<br/>`True` for success<br/>`False` for error|

## `.getSentence(index)`

Returns the `Sentence` at the given index.

If called without a specified index, it will return the sentence that follows the last index you called the method with.

### Parameters:

|name|type|description|mandatory|
|--|--|--|--|
|`index`|`int`|Index of the `Sentence` you want to retrieve|No|

### Return value:

Returns a `Sentence` instance.

### Examples:

```python
data = client.request(text='première phrase. deuxième phrase. troisième phrase')

sentence = data.getSentence(2)
# sentence.data['postagger'] = [['troisieme', 'JJ'], ['phrase', 'N']]
```
<br />

```python
data = client.request(text='première phrase. deuxième phrase. troisième phrase')

sentence_2 = data.getSentence(1)
sentence_3 = data.getSentence()

# sentence_2.postagger.data = [['deuxieme', 'JJ'], ['phrase', 'N'], ['.', 'PUNCT']]
# sentence_3.postagger.data = [['troisieme', 'JJ'], ['phrase', 'N']]
```
<br />

```python
data = client.request(text='première phrase. deuxième phrase. troisième phrase')

sentence = data.getSentence()

# sentence.postagger.data = [['premiere', 'JJ'], ['phrase', 'N'], ['.', 'PUNCT']]
```


## `.getNumberOfSentences()`

Returns the number of sentences.

### Example:

```python
data = client.request(text='première phrase. deuxième phrase')
number = data.getNumberOfSentence()
# number = 2
```

## `.map(function)`

Apply a `function` to all `Sentence`elements.

### Parameters:

|name|type|description|
|--|--|--|
|`function`|`function`|The function that will be applied to all the `Sentence` elements.|

### Return value:

`boolean` that represent the operation status:
- `True` for success  
- `False` for error

### Example:

```python
data = client.request(raw=False, text="J'aimais le café. Maintenant plus trop.")
def ma_fonction(sentence):
	print(sentence.data['postagger'])

data.map(ma_fonction)

#[['je', 'CLS'], ['aimai', 'V'], ['le', 'D'], ['cafe', 'N'], ['.', 'PUNCT']]
#[['Maintenant', 'NP'], ['plus', 'RB'], ['trop', 'RB'], ['.', 'PUNCT']]
```

# `class Sentence`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access the data for a sentence with a toolkit of methods/classes.

Contains subclasses for each analysis of a sentence:

All methods inherited from [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass),  and called directly on the `Sentence` class will be applied on the `global`  key of the sentence analysis.

|subclass|sentence analysis key|
|--|--|
|[ner](#class-ner)|`NER`|
|[nlu](#class-nlu)|`NLU`|
|[nlp](#class-nlp)|`NLP`|
|[sentiment](#class-sentiment)|`sentiment`
|[emoticons](#class-emoticons)|`emoticons`
|[parser_dependency](#class-parser_dependency)|`parser_dependency`|
|[postagger](#class-postagger)|`postagger`|
|[sentence_acts](#class-sentence_acts)|`sentence_acts`
|[coreference](#class-coreference)|`coreference`

# `class ner`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `NER` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.getSentence(0)

ner_analysis = sentence.ner.get()
ner_date_items = sentence.ner.getDateItems()
ner_kilo_items = sentence.ner.getByFilter('value.unit', 'kg')
```

# `class nlu`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `NLU` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.getSentence(0)

nlu_analysis = sentence.nlu.get()
nlu_kilo_items = sentence.nlu.getByFilter('value.unit', 'kg')
```

# `class nlp`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `NLP` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.getSentence(0)

nlp_analysis = sentence.nlp.get()
nlp_date_items = sentence.nlp.getDateItems()
nlp_kilo_items = sentence.nlp.getByFilter('value.unit', 'kg')
```

# `class sentiment`

> Inherits [SharedClass](#class-sharedclass)

Access and perform actions on the data located in the  `Sentiment` key.

The data contained in the `Sentiment` key is divised in two keys that has their specific format:
* `list` where the sentiments are listed.
* `group` where the sentiments are merged into groups.

That's why this class has two subsclass:

## `class list`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).


### Example:
```python
data = client.request("j'aime beaucoup apprendre.")
sentence = data.getSentence(0)

sentiment_analysis = sentence.sentiment.get()
happiness_items = sentence.sentiment.list.getHappinessItems()
happiness_items = sentence.sentiment.list.getByFilter('type', 'happiness')
```

## `class group`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).


### Example:

```python
data = client.request("j'aime beaucoup manger.")
sentence = data.getSentence(0)

sentiment_analysis = sentence.sentiment.get()
group_happiness = sentence.sentiment.group.getByFilter('type', 'happiness')
group_happiness = sentence.sentiment.group.getHappinessItems()
```

# `class emoticons`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `emoticons` key.

### Methods:

|name|description | return value|
|--|--|--|
| `getPresent()` | Returns the emoticon types that are present.| `list` of [emoticon types](https://www.doc.lettria.com/#emoticons)
|`getConfidence()`| Returns the confidence of the analysis.| `float` between 0 and 1

## `.getPresent()`

Returns the emoticon types that are present.

### Return value:

`list` of [emoticon types](https://www.doc.lettria.com/#emoticons)

### Example:

```python
data = client.request("cool 😁😛")
sentence = data.getSentence(0)

emoticons_analysis = sentence.emoticons.get()
present_emoticons = sentence.emoticons.getPresent()
# present_emoticons = ["playful", "very_happy"]
```

## `.getConfidence()`

Returns the emoticon types that are present.

### Return value:

`list` of [emoticon types](https://www.doc.lettria.com/#emoticons)

### Example:

```python
data = client.request("cool 😁😛")
sentence = data.getSentence(0)

emoticons_analysis = sentence.emoticons.get()
present_emoticons = sentence.emoticons.getConfidence()
# present_emoticons = ["playful", "very_happy"]
```

# `class parser_dependency`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `parser_dependency` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.getSentence(0)

parser_dependency_analysis = sentence.parser_dependency.get()
entities = sentence.parser_dependency.getByFilter('tag', 'ENTITY')
```

### Methods:

|name|description | return value|
|--|--|--|
| `getByRole()` | Returns the emoticon types that are present.| `list` of [emoticon types](https://www.doc.lettria.com/#emoticons)

## `.getByRole(role)`

### Parameters:

|name|type|description|
|--|--|--|
|`role`|`string`|Role on which we will base our filter.|

### Return value:

Returns a `list` of the items that match the queried role in `parser_dependency`.

### Example:

```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.getSentence(0)

subjects = sentence.parser_dependency.getByRole('nsubj')
```

# `class postagger`

Access and perform actions on the data located in the  `postagger` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.getSentence(0)

postagger_analysis = sentence.postagger.get()
```

### Methods:

|name|description | return value|
|--|--|--|
| `getByTag()` | Returns the elements that match the given tag| `list` of [postagger elements](https://www.doc.lettria.com/#pos-tagger)

## `.getByTag(tag)`

### Parameters:

|name|type|description|
|--|--|--|
|`tag`|`string` or `list`|Tag on which we will base our filter.|

### Return value:

Returns a `list` of the items that match the queried tag in `postagger`.

### Example:

```python
data = client.request("j'ai pesé 76kg mais maintenant j'en pese 42")
sentence = data.getSentence()

numbers = sentence.postagger.getByTag('CD')
verbs = sentence.postagger.getByTag(['V', 'VP'])
```

# `class sentence_acts`

Access and perform actions on the data located in the  `sentence_acts` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.getSentence()

sentence_acts_analysis = sentence.sentence_acts.get()
```

# `class coreference`

Access and perform actions on the data located in the  `coreference` key.

### Example:
```python
data = client.request("je pesais 76kg le 12 janvier et maintenant j'en pese 42")
sentence = data.getSentence()

coreference_analysis = sentence.coreference.get()
```

# `class SharedClass`

Used to share a group of methods.

If called from one of it's child classes, these methods will be applied on the data that their class contains.

#### Methods:

|name|description | return value|
|--|--|--|
|`get()`|Returns the data that an element contains|Depends on the element's class.|
|`getByFilter()`|Returns the item that was found based on the filter.|Depends on the element's class.
|`getNested()`|Returns the nested sub-property on an object.|Depends on the wanted value.|
|`set()`|Set the data for the element.<br/>All elements are already intialised when received.| `boolean` that represent the operation status:<br/>`True` for success<br/>`False` for error

## `.get()`

Returns the data that the class contains.

### Return value:

The returned value depends on which class you call it on.

|class|value|
|--|--|
|`Sentence`|An object containing all the analyzes performed for a sentence.
|`ner`|An object containing all the data of an entity.

## `.getByFilter(key, value, [options...])`

Returns a list of objects that match the filter, based on the data that the class contains.

### Parameters:

|name|type|description|
|--|--|--|
|`key`|`string`|Key on which the filter will be applied to find an element.|
|`value`|Depends on targeted key.|This value will be used to filter items by comparaison.|
|`list`|`list`|Used if you want to find an item on a different data then the one contained by your element.

### Return value:

`list` of objects that match the filter.
These objects depend on the class on which the method is called from.


### Example:
```python
data = client.request('phrase 0 zero@lettria.com . phrase 1 un@lettria.com')
phrase_1 = data.getSentence(1)

phrase_1_mails = phrase_1.getByFilter('type', 'mail')

print(phrase_1_mails)

[
	{
		"type": "mail",
		"lemma": "un@lettria.com",
		"word": "un@lettria.com",
		...
	}
]
```

## `.getNested(obj, key)`

Returns the value contained by a property in an object.

### Parameters:

|name|type|description|
|--|--|--|
|`key`|`string`|Key on which the filter will be applied to find an element.|
|`value`|Depends on targeted key.|This value will be used to filter items by comparaison.|
|`list`|`list`|Used if you want to find an item on a different data then the one contained by your element.

### Return value:

Depends on the object and the key.

### Examples:
With `shared_class` beeing an instance of `SharedClass` or of a class that inherits `SharedClass`.
```python
a = shared_class.getNested("type", {"type": 42})
# a = 42
```
Nested levels are accessible with this syntax:
```python
a = shared_class.getNested('data.person.name', {
	"data": {
		"person": {
			"name": "Paul"
		}
	}
})

# a = "Paul"
```

# `class ExtractClass`

Used to share a group of extraction methods.


### Methods:
|name| return type |description|
|---|---|--|
|`getDateItems()`|`list`| Returns items that match the `type` `date`|
|`getDistanceItems()`|`list`| Returns items that match the `type` `distance`|
|`getDurationItems()`|`list`| Returns items that match the `type` `duration`|
|`getElectricPowerItems()`|`list`| Returns items that match the `type` `electric power`|
|`getHexColorItems()`|`list`| Returns items that match the `type` `hex color`|
|`getIntervalItems()`|`list`| Returns items that match the `type` `interval`|
|`getIpItems()`|`list`| Returns items that match the `type` `ip`|
|`getIpv6Items()`|`list`| Returns items that match the `type` `ipv6`|
|`getLightIntensityItems()`|`list`| Returns items that match the `type` `light intensity`|
|`getMailItems()`|`list`| Returns items that match the `type` `mail`|
|`getMassItems()`|`list`| Returns items that match the `type` `mass`|
|`getMassByVolumeItems()`|`list`| Returns items that match the `type` `mass by volume`|
|`getMolItems()`|`list`| Returns items that match the `type` `mol`|
|`getMoneyItems()`|`list`| Returns items that match the `type` `money`|
|`getOrdinalItems()`|`list`| Returns items that match the `type` `ordinal`|
|`getPercentItems()`|`list`| Returns items that match the `type` `percent`|
|`getPhoneItems()`|`list`| Returns items that match the `type` `phone`|
|`getPressureItems()`|`list`| Returns items that match the `type` `pressure`|
|`getSetItems()`|`list`| Returns items that match the `type` `set`|
|`getSpeedItems()`|`list`| Returns items that match the `type` `speed`|
|`getStrengthItems()`|`list`| Returns items that match the `type` `strength`|
|`getSurfaceItems()`|`list`| Returns items that match the `type` `surface`|
|`getSurfaceTensionItems()`|`list`| Returns items that match the `type` `surface tension`|
|`getTemperatureItems()`|`list`| Returns items that match the `type` `temperature`|
|`getTimeItems()`|`list`| Returns items that match the `type` `time`|
|`getUrlItems()`|`list`| Returns items that match the `type` `url`|
|`getVoltageItems()`|`list`| Returns items that match the `type` `voltage`|
|`getVolumeItems()`|`list`| Returns items that match the `type` `volume`|
|`getHappinessItems()`|`list`| Returns items that match the `type` `happiness`|
|`getSadnessItems()`|`list`| Returns items that match the `type` `sadness`|
|`getFearItems()`|`list`| Returns items that match the `type` `fear`|
|`getDisgustItems()`|`list`| Returns items that match the `type` `disgust`|
|`getAngerItems()`|`list`| Returns items that match the `type` `anger`|
|`getSurpriseItems()`|`list`| Returns items that match the `type` `surprise`|
|`getJudgementItems()`|`list`| Returns items that match the `type` `judgement`|
