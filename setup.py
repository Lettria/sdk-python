# coding: utf-8

from setuptools import setup, find_packages

setup(
    name="lettria",
    version="2.0.0",
    packages=find_packages(),
    description="Lettria official SDK for python",
    author="Victor",
    author_email="victor@lettria.com",
    url="https://github.com/Lettria/sdk-python",
    license="MIT",
    install_requires=[
      "requests>=2.10",
    ],
    keywords="lettria french nlp taln chatbot bigdata text analysis"
)
