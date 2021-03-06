# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.5] - commit name : Various improvments - 2021-06-29
### Added
- NLP.reset_data() allows to reset the nlp object and erase all documents data.
### Changed
- Multiple NLP instances can be used at the same time, documents ids are not common anymore accross all NLP instances.
- Changes to calculation of average for word_emotion, meaning_emotion, word_sentiment, meaning_sentiment.
- emotion and emotion_ml attributes now return different values. 'emotion_ml' stays the same while 'emotion' is now a mix of our ML model with another algorithm.
- Fix for subsentences tokens.

## [5.0.4] - commit name : Various improvments - 2021-06-05
### Added
- New argument 'skip_errors' for match_pattern.
- New attribute 'original_text' for retrieving input text before tokenization.

## [5.0.3] - commit name : Pattern Matching Update - 2021-06-05
### Added
- New feature: Pattern Matcher
- New feature: Dependency Pattern Matcher
- New function (lettria.load_results) that can return an iterator of NLP objects for reading files chunk by chunk.
### Changed
- Default save format changed from json to jsonlines, this allows to load huge files in memory by reading them chunk by chunk
- Default representation for TextChunk object has changed from raw json data to token text.
- Important decrease of memory requirements and results file size (Around -70%).

## [5.0.2] - commit name : Functional Interface Integration - 2020-12-15
### Added
- Sentiment methods are now accessible through the functional interface (get_sentiment(), word_sentiment() etc.).
- Methods list_entities(), word_frequency(), word_count(), statistics(), and vocabulary() are accessible through the functional interface.
- split_results() to split a result file into multiple files
- filter_type() for filtering sentences based on their type (command, assert, question_open, question_closed).
- pos_detail, lemma_detail properties accessible at all levels through functional interface.
### Changed
### Deprecated
- Sentiment module is deprecated and will be removed in a future release.
### Removed
- Methods list_entities(), word_frequency(), word_count() and vocabulary() had their 'level' argument removed.
The 'level' is now chosen by using the method at the approriate level 
Before: self.nlp.vocabulary(level='documents') => After: [doc.vocabulary() for doc in self.nlp]
### Fixed
- pos_detail property for Token class has been fixed.
### Security
 
## [5.0.1] - commit name : NLP Interface - 2020-10-15
### Added
- SDK redone from the ground up ! Look at our tutorials and documentation to get started.
- New interface with the class NLP that provides an easy access to relevant results.
- New document system that allows you to classify and name your data the way you want.
- Sentiment class provides additional functionalities for sentiment and emotion analysis
- Easy to save and load results from the API.
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [4.1.2] - commit name : base - 2019-12-18
### Added
- Analyser class to provide easy access and analysis of API result..
### Changed
### Deprecated
### Removed
### Fixed
### Security


