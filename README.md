
<br/>

![](https://lettria.com/images/logo.png)


## Introduction

Lettria edits a NLP toolkit dedicated to the understanding of french.

This is our official SDK for Python, designed to make the usage of our API straightforward, quick and efficient.

Learn more about our API and its format with our [tutorials](https://lettria.com/fr/dev/guides/getting-started), [documentation](https://doc.lettria.com) and [demo](https://lettria.com/demo).

## Overview
* [Introduction](#introduction)
* [Features](#features)
* [Installation](#installation)
* [Getting your api key](#getting-your-api-key)
* [Quickstart](#quickstart)
	* [NLP](#nlp-class)
	* [Common properties](#common-properties)
* [Documentation](#documentation)

## Features


Name|Description
-|-
Tokenization|Segmenting text into sentences and sentences into words, punctuations marks etc.
Subsentence detection| Segmenting sentences into 'subsentences' for a finer analysis.
Part-of-speech (POS) Tagging|	Finding the word type of each token like noun, adjective or verb.
Dependency Parsing|Finding the relations between individual tokens by assigning them dependency labels, like subject, determinant or object.
Lemmatization|Finds for each token its 'base' form, for example the lemma of "est” is “être”, and the lemma of "oiseaux” is "oiseau”.
Named Entity Recognition (NER)| Detection of numerous "entities" such as locations, persons, quantities or dates.
Natural Language Understanding (NLU) | Interpreting the meaning of each token by identifying its meaning category and lexicon.
Coreference|Identifying coreference links between different tokens.
Sentiment Analysis|	Analysing sentimental value of input text (positive, negative or neutral), by sentence or subsentence.
Emotion Analysis|	Analysing emotional value of input text (positive, negative or neutral), by sentence or subsentence.
Sentence Type classification|Detecting the type of the sentence (question, assertion, command, exclamation).
Language detection | Detecting the language of the sentence.

## Installation

  ### pip (recommended)

Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a package manager for Python.

	pip install lettria

If you dont' have pip, you can install it by running this from the command line:

	$ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

  ### source code

You can [download the source code](https://github.com/Lettria/sdk-python/zipball/master "Lettria python sdk source code") and then run:

	python setup.py install

## Getting your API key
In order to start making requests you need an API key.
You can start right now by creating a [free key](https://app.lettria.com/signup).

## Quickstart

### NLP class

As a quick introduction we are going to perform a request on two documents and request relevant information from the results.
A 'document' is any bit of information that you wish to analyse individually, for example a review in a dataset of online reviews.

```python
import lettria

api_key = ' YOU API KEY'
nlp = lettria.NLP(api_key)

documents = [
	['first document, my first sentence. my second sentence'],
	['second document, my first sentence, my second sentence']
]

#Performs requests to Lettria's API
for doc in documents:
	nlp.add_document(doc)

#Saving results for further usage.
nlp.save_results("results.json")

#Print list of lemma for all the data requested
print(nlp.lemma)

#Print list of token per document
for document in nlp:
	print(document.token)

#Print POS tags, dependency tags by accessing sentences directly.
for sentence in nlp.sentences:
	print(sentence.pos, sentence.dep)
```

## Documentation
Our documentation is available online on our [website](https://doc.lettria.com) or [locally](./documentation/documentation_full.md). You can also find [tutorials](https://lettria.com/fr/dev/guides/getting-started) that will introduce you to our API and SDK and guide you to perform specific usecases.
