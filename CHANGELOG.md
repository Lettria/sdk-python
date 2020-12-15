on 2.0.0
# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.2] - commit name : Functional Interface Integration - 2020-12-15
### Added
- Sentiment methods are now accessible through the functional interface (get_sentiment(), word_sentiment() etc.).
- Methods list_entities(), word_frequency(), word_count(), statistics(), and vocabulary() are accessible through the functional interface.
- split_results() to split a result file into multiple files
-
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


