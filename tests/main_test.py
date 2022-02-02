import lettria
import pytest
import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


patterns_json = {
    "pattern_verb":
    [
        {
            "RIGHT_ID": "qualificatif",
            "RIGHT_ATTRS": {"POS": {"IN": ["V"]}}
        },
        {
            "LEFT_ID": "qualificatif",
            "REL_OP": ">>",
            "RIGHT_ID": "support",
            "RIGHT_ATTRS": {"POS": "NP", "OP": "+"}
        }
    ],
    "pattern_NNP":
    [
        {
            "RIGHT_ID": "qualificatif",
            "RIGHT_ATTRS": {"POS": {"IN": ["N"]}}
        },
        {
            "LEFT_ID": "qualificatif",
            "REL_OP": ">>",
            "RIGHT_ID": "support",
            "RIGHT_ATTRS": {"POS": "NP", "OP": "+"}
        }
    ],
}

tests = []


@pytest.fixture
def nlp_object():
    nlp = lettria.NLP()
    filename = os.path.join(os.path.dirname(__file__), "./test_data.jsonl")
    nlp.load_result(filename, verbose=False)
    return nlp


def evaluate_field(object, field, error_fields, level):
    try:
        _ = getattr(object, field)
    except Exception as e:
        if (level, field) not in error_fields:
            error_fields += [(level, field)]

def test_attributes_tokens(nlp_object):
    nlp = nlp_object
    fields = nlp.token_fields
    error_fields = []
    for field in fields:
        level = 'nlp'
        evaluate_field(nlp, field, error_fields, level)
        for doc in nlp:
            level = 'document'
            evaluate_field(doc, field, error_fields, level)
            for subsentence in doc.sentences:
                level = 'subsentence'
                evaluate_field(subsentence, field, error_fields, level)
            for sentence in doc.sentences:
                level = 'sentence'
                evaluate_field(sentence, field, error_fields, level)
                for token in sentence.tokens:
                    level = 'token'
                    evaluate_field(token, field, error_fields, level)
    if error_fields:
        raise Exception(
            "The following fields give an error: {}".format(error_fields))

def test_attributes_sentence(nlp_object):
    nlp = nlp_object
    fields = nlp.sentence_fields
    error_fields = []
    for field in fields:
        level = 'nlp'
        evaluate_field(nlp, field, error_fields, level)
        for doc in nlp:
            level = 'document'
            evaluate_field(doc, field, error_fields, level)
            for subsentence in doc.sentences:
                level = 'subsentence'
                evaluate_field(subsentence, field, error_fields, level)
            for sentence in doc.sentences:
                level = 'sentence'
                evaluate_field(sentence, field, error_fields, level)
    if error_fields:
        raise Exception(
            "The following fields give an error: {}".format(error_fields))

def test_attributes_document(nlp_object):
    nlp = nlp_object
    fields = nlp.document_fields
    error_fields = []
    for field in fields:
        level = 'nlp'
        evaluate_field(nlp, field, error_fields, level)
        for doc in nlp:
            level = 'document'
            evaluate_field(doc, field, error_fields, level)
    if error_fields:
        raise Exception(
            "The following fields give an error: {}".format(error_fields))

def evaluate_func(object, field, error_fields, level):
    try:
        _ = getattr(object, field)
    except Exception as e:
        if (level, field) not in error_fields:
            error_fields += [(level, field)]

def test_methods_chunk(nlp_object):
    nlp = nlp_object
    polarity = 'positive'
    emotions = ['anger', 'annoyance', 'caring']
    hierarchy = ['nlp','documents', 'sentences', 'subsentences']
    sentence_type = ['assert']
    for level in hierarchy:
        for _iter in getattr(nlp, level):
            _iter.match_pattern(patterns_json, level = None, print_tree=False, skip_errors=False)
            _iter.match_pattern(patterns_json, level = 'documents', print_tree=False, skip_errors=False)
            _iter.match_pattern(patterns_json, level = 'sentences', print_tree=False, skip_errors=False)
            _iter.vocabulary(filter_pos = None, lemma=False)
            _iter.vocabulary(filter_pos = None, lemma=True)
            _iter.vocabulary(filter_pos = ['V'], lemma=False)
            _iter.vocabulary(filter_pos = ['V'], lemma=True)
            _iter.list_entities()
            _iter.word_count(filter_pos = None, lemma=False)
            _iter.word_count(filter_pos = None, lemma=True)
            _iter.word_count(filter_pos = ['V'], lemma=True)
            _iter.word_count(filter_pos = ['N', 'NP'], lemma=True)
            _iter.word_frequency(filter_pos = None, lemma=False)
            _iter.word_frequency(filter_pos = None, lemma=True)
            _iter.word_frequency(filter_pos = ['N', 'NP'], lemma=False)
            _iter.word_frequency(filter_pos = ['N', 'NP'], lemma=True)
            _iter.statistics()
            _iter.get_emotion(granularity ='sentence')
            _iter.get_emotion(granularity ='subsentence')
            _iter.get_sentiment(granularity='sentence')
            _iter.get_sentiment(granularity='subsentence')
            _iter.filter_polarity(polarity, granularity='sentence')
            _iter.filter_polarity(polarity, granularity='subsentence')
            _iter.filter_emotion(emotions, granularity='sentence')
            _iter.filter_emotion(emotions, granularity='subsentence')
            _iter.filter_type(sentence_type)
            _iter.word_sentiment(granularity = 'sentence', lemma = False, filter_pos = None, average=True)
            _iter.word_sentiment(granularity = 'sentence', lemma = True, filter_pos = None, average=True)
            _iter.word_sentiment(granularity = 'sentence', lemma = True, filter_pos = None, average=False)
            _iter.word_sentiment(granularity = 'sentence', lemma = True, filter_pos = ['N', 'NP'], average=False)
            _iter.word_sentiment(granularity = 'subsentence', lemma = True, filter_pos = ['N', 'NP'], average=False)
            _iter.word_emotion(granularity = 'sentence', lemma = False, filter_pos = None, average=True)
            _iter.word_emotion(granularity = 'sentence', lemma = True, filter_pos = None, average=True)
            _iter.word_emotion(granularity = 'sentence', lemma = True, filter_pos = None, average=False)
            _iter.word_emotion(granularity = 'sentence', lemma = True, filter_pos = ['N', 'NP'], average=False)
            _iter.word_emotion(granularity = 'subsentence', lemma = True, filter_pos = ['N', 'NP'], average=False)
            _iter.meaning_sentiment(granularity='sentence', filter_meaning=None, average=True)
            _iter.meaning_sentiment(granularity='sentence', filter_meaning=None, average=False)
            _iter.meaning_sentiment(granularity='sentence', filter_meaning=['ACTION'], average=False)
            _iter.meaning_sentiment(granularity='subsentence', filter_meaning=None, average=True)
            _iter.meaning_sentiment(granularity='subsentence', filter_meaning=None, average=False)
            _iter.meaning_sentiment(granularity='subsentence', filter_meaning=['ACTION'], average=False)
            _iter.meaning_emotion(granularity='sentence', filter_meaning=None, average=True)
            _iter.meaning_emotion(granularity='sentence', filter_meaning=None, average=False)
            _iter.meaning_emotion(granularity='sentence', filter_meaning=['ACTION'], average=False)
            _iter.meaning_emotion(granularity='subsentence', filter_meaning=None, average=True)
            _iter.meaning_emotion(granularity='subsentence', filter_meaning=None, average=False)
            _iter.meaning_emotion(granularity='subsentence', filter_meaning=['ACTION'], average=False)



