<br/>

![](https://lettria.com/images/logo.png)


# Introduction

Lettria edits a NLP toolkit dedicated to the understanding of french.

This is our official SDK for Python.

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
			* [emotion](#class-emotion)
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
|`get_key()`|Retrieve the key used by the client|`string` representing your `API_KEY`.
|`set_key()`|Set the key that will be used bu the client| `boolean` that represent the operation status:<br/>`True` for success<br/>`False` for error


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

## `.get_key()`

Returns the  `API_KEY` used by the client as a `string`.

## `.set_key(API_KEY)`

Set the `API_KEY` that will be used by your client.

<br/><br/>

# Classes available if raw is false

When the `raw` parameter is disabled, the client will return a `class Data`

# `class Data`

Contains the data for each sentences in your text input as `Sentence` instances, and some methods to perform actions on them.

### Methods:

|name|description | return value|
|--|--|--|
|`get_sentence()`|Returns the `Sentence` at the given index.|`class Sentence`
|`get_number_of_sentences()`|Returns the number sentences|`int`
| `map()` | Apply a function to all `Sentence` elements. |`boolean` that represent the operation status:<br/>`True` for success<br/>`False` for error|

## `.get_sentence(index)`

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

sentence = data.get_sentence(2)

# sentence.data['postagger'] = [['troisieme', 'JJ'], ['phrase', 'N']]
```
<br />

```python
data = client.request(text='première phrase. deuxième phrase. troisième phrase')

sentence_2 = data.get_sentence(1)
sentence_3 = data.get_sentence()

# sentence_2.postagger.data = [['deuxieme', 'JJ'], ['phrase', 'N'], ['.', 'PUNCT']]
# sentence_3.postagger.data = [['troisieme', 'JJ'], ['phrase', 'N']]
```
<br />

```python
data = client.request(text='première phrase. deuxième phrase. troisième phrase')

sentence = data.get_sentence()

# sentence.postagger.data = [['premiere', 'JJ'], ['phrase', 'N'], ['.', 'PUNCT']]
```


## `.get_number_of_sentences()`

Returns the number of sentences.

### Example:

```python
data = client.request(text='première phrase. deuxième phrase')
number = data.get_number_of_sentences()
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
|[emotion](#class-emotion)|`emotion`
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
sentence = data.get_sentence(0)

ner_analysis = sentence.ner.get()
ner_date_items = sentence.ner.get_date_items()
ner_kilo_items = sentence.ner.get_by_filter('value.unit', 'kg')
```

# `class nlu`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `NLU` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.get_sentence(0)

nlu_analysis = sentence.nlu.get()
nlu_kilo_items = sentence.nlu.get_by_filter('value.unit', 'kg')
```

# `class nlp`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `NLP` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.get_sentence(0)

nlp_analysis = sentence.nlp.get()
nlp_date_items = sentence.nlp.get_date_items()
nlp_kilo_items = sentence.nlp.get_by_filter('value.unit', 'kg')
```

# `class sentiment`

> Inherits [SharedClass](#class-sharedclass)

Access and perform actions on the data located in the  `sentiment` key.

The data contained in the `sentiment` key is divised in two keys that has their specific format:
* `elements` where the sentiments are listed.
* `values` where the sentiments values are set.

That's why this class has two subsclass:

## `class elements`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).


### Example:
```python
data = client.request("j'aime beaucoup manger.")
sentence = data.get_sentence(0)

sentiment_analysis = sentence.sentiment.get()
sentiment_elements = sentence.sentiment.elements.get()
```

## `class values`


### Example:

```python
data = client.request("j'aime beaucoup manger.")
sentence = data.get_sentence(0)

sentiment_analysis = sentence.sentiment.get()
sentiment_values = sentence.sentiment.values.get()
```
# `class emotion`

> Inherits [SharedClass](#class-sharedclass)

Access and perform actions on the data located in the  `emotion` key.

The data contained in the `emotion` key is divised in two keys that has their specific format:
* `elements` where the sentiments are listed.
* `values` where the sentiments values are set.

That's why this class has two subsclass:

## `class elements`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).


### Example:
```python
data = client.request("j'aime beaucoup manger.")
sentence = data.get_sentence(0)

emotion_analysis = sentence.emotion.get()
emotion_elements = sentence.emotion.elements.get_happiness_items()
emotion_elements = sentence.emotion.elements.get_by_filter('type', 'happiness')
```

## `class values`


### Example:

```python
data = client.request("j'aime beaucoup manger.")
sentence = data.get_sentence(0)

emotion_analysis = sentence.emotion.get()
emotion_values = sentence.emotion.values.get()
```

# `class emoticons`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `emoticons` key.

### Methods:

|name|description | return value|
|--|--|--|
| `get_present()` | Returns the emoticon types that are present.| `list` of [emoticon types](https://www.doc.lettria.com/#emoticons)
|`get_confidence()`| Returns the confidence of the analysis.| `float` between 0 and 1

## `.get_present()`

Returns the emoticon types that are present.

### Return value:

`list` of [emoticon types](https://www.doc.lettria.com/#emoticons)

### Example:

```python
data = client.request("cool 😁😛")
sentence = data.get_sentence(0)

emoticons_analysis = sentence.emoticons.get()
present_emoticons = sentence.emoticons.get_present()
# present_emoticons = ["playful", "very_happy"]
```

## `.getConfidence()`

Returns the emoticon types that are present.

### Return value:

`list` of [emoticon types](https://www.doc.lettria.com/#emoticons)

### Example:

```python
data = client.request("cool 😁😛")
sentence = data.get_sentence(0)

emoticons_analysis = sentence.emoticons.get()
present_emoticons = sentence.emoticons.get_confidence()
# present_emoticons = ["playful", "very_happy"]
```

# `class parser_dependency`

> Inherits [SharedClass](#class-sharedclass) and [ExtractClass](#class-extractclass).

Access and perform actions on the data located in the  `parser_dependency` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.get_sentence(0)

parser_dependency_analysis = sentence.parser_dependency.get()
entities = sentence.parser_dependency.get_by_filter('tag', 'ENTITY')
```

### Methods:

|name|description | return value|
|--|--|--|
| `get_by_role()` | Returns the emoticon types that are present.| `list` of [emoticon types](https://www.doc.lettria.com/#emoticons)

## `.get_by_role(role)`

### Parameters:

|name|type|description|
|--|--|--|
|`role`|`string`|Role on which we will base our filter.|

### Return value:

Returns a `list` of the items that match the queried role in `parser_dependency`.

### Example:

```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.get_sentence(0)

subjects = sentence.parser_dependency.get_by_role('nsubj')
```

# `class postagger`

Access and perform actions on the data located in the  `postagger` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.get_sentence(0)

postagger_analysis = sentence.postagger.get()
```

### Methods:

|name|description | return value|
|--|--|--|
| `get_by_tag()` | Returns the elements that match the given tag| `list` of [postagger elements](https://www.doc.lettria.com/#pos-tagger)

## `.get_by_tag(tag)`

### Parameters:

|name|type|description|
|--|--|--|
|`tag`|`string` or `list`|Tag on which we will base our filter.|

### Return value:

Returns a `list` of the items that match the queried tag in `postagger`.

### Example:

```python
data = client.request("j'ai pesé 76kg mais maintenant j'en pese 42")
sentence = data.get_sentence()

numbers = sentence.postagger.get_by_tag('CD')
verbs = sentence.postagger.get_by_tag(['V', 'VP'])
```

# `class sentence_acts`

Access and perform actions on the data located in the  `sentence_acts` key.

### Example:
```python
data = client.request('je pesais 76kg le 12 janvier 2017')
sentence = data.get_sentence()

sentence_acts_analysis = sentence.sentence_acts.get()
```

# `class coreference`

Access and perform actions on the data located in the  `coreference` key.

### Example:
```python
data = client.request("je pesais 76kg le 12 janvier et maintenant j'en pese 42")
sentence = data.get_sentence()

coreference_analysis = sentence.coreference.get()
```

# `class SharedClass`

Used to share a group of methods.

If called from one of it's child classes, these methods will be applied on the data that their class contains.

#### Methods:

|name|description | return value|
|--|--|--|
|`get()`|Returns the data that an element contains|Depends on the element's class.|
|`get_by_filter()`|Returns the item that was found based on the filter.|Depends on the element's class.
|`get_nested()`|Returns the nested sub-property on an object.|Depends on the wanted value.|
|`set()`|Set the data for the element.<br/>All elements are already intialised when received.| `boolean` that represent the operation status:<br/>`True` for success<br/>`False` for error

## `.get()`

Returns the data that the class contains.

### Return value:

The returned value depends on which class you call it on.

|class|value|
|--|--|
|`Sentence`|An object containing all the analyzes performed for a sentence.
|`ner`|An object containing all the data of an entity.

## `.get_by_filter(key, value, [options...])`

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
phrase_1 = data.get_sentence(1)

phrase_1_mails = phrase_1.get_by_filter('type', 'mail')

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

## `.get_nested(obj, key)`

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
a = shared_class.get_nested("type", {"type": 42})
# a = 42
```
Nested levels are accessible with this syntax:
```python
a = shared_class.get_nested('data.person.name', {
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
|`get_date_items()`|`list`| Returns items that match the `type` `date`|
|`get_distance_items()`|`list`| Returns items that match the `type` `distance`|
|`get_duration_items()`|`list`| Returns items that match the `type` `duration`|
|`get_electric_power_items()`|`list`| Returns items that match the `type` `electric power`|
|`get_hex_color_items()`|`list`| Returns items that match the `type` `hex color`|
|`get_interval_items()`|`list`| Returns items that match the `type` `interval`|
|`get_ip_items()`|`list`| Returns items that match the `type` `ip`|
|`get_ipv6_items()`|`list`| Returns items that match the `type` `ipv6`|
|`get_light_intensity_items()`|`list`| Returns items that match the `type` `light intensity`|
|`get_mail_items()`|`list`| Returns items that match the `type` `mail`|
|`get_mass_items()`|`list`| Returns items that match the `type` `mass`|
|`get_mass_by_volume_items()`|`list`| Returns items that match the `type` `mass by volume`|
|`get_mol_items()`|`list`| Returns items that match the `type` `mol`|
|`get_money_items()`|`list`| Returns items that match the `type` `money`|
|`get_ordinal_items()`|`list`| Returns items that match the `type` `ordinal`|
|`get_percent_items()`|`list`| Returns items that match the `type` `percent`|
|`get_phone_items()`|`list`| Returns items that match the `type` `phone`|
|`get_pressure_items()`|`list`| Returns items that match the `type` `pressure`|
|`get_set_items()`|`list`| Returns items that match the `type` `set`|
|`get_speed_items()`|`list`| Returns items that match the `type` `speed`|
|`get_strength_items()`|`list`| Returns items that match the `type` `strength`|
|`get_surface_items()`|`list`| Returns items that match the `type` `surface`|
|`get_surface_tension_items()`|`list`| Returns items that match the `type` `surface tension`|
|`get_temperature_items()`|`list`| Returns items that match the `type` `temperature`|
|`get_time_items()`|`list`| Returns items that match the `type` `time`|
|`get_url_items()`|`list`| Returns items that match the `type` `url`|
|`get_voltage_items()`|`list`| Returns items that match the `type` `voltage`|
|`get_volume_items()`|`list`| Returns items that match the `type` `volume`|
|`get_happiness_items()`|`list`| Returns items that match the `type` `happiness`|
|`get_sadness_items()`|`list`| Returns items that match the `type` `sadness`|
|`get_fear_items()`|`list`| Returns items that match the `type` `fear`|
|`get_disgust_items()`|`list`| Returns items that match the `type` `disgust`|
|`get_anger_items()`|`list`| Returns items that match the `type` `anger`|
|`get_surprise_items()`|`list`| Returns items that match the `type` `surprise`|
|`get_judgement_items()`|`list`| Returns items that match the `type` `judgement`|
