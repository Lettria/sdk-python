# coding: utf-8

from setuptools import setup, find_packages

setup(
    name="lettria",
    version="5.0.0",
    packages=find_packages(),
    description="Lettria official SDK for python",
    author="Maxence",
    author_email="maxence@lettria.com",
    url="https://github.com/Lettria/sdk-python",
    license="MIT",
    install_requires=[
      "requests>=2.10",
    ],
    keywords="lettria french nlp taln ner nlu chatbot bigdata text analysis sentiment emotion"
)
