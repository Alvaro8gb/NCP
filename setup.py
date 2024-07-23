from setuptools import setup, find_packages

setup(
    name="ncp",
    version="0.0.5",
    author="MEDAL",
    author_email="alvaro8gb@gmail.com",
    description="NLP Cancer Pipeline",
    url="https://github.com/Alvaro8gb/NCP",
    packages= find_packages(),
    install_requires = ['pandas==1.5.3', 'spacy==3.5.1', 'spacy-transformers==1.2.2','textacy==0.12.0'],
    include_package_data=False, # los archivos no .py  
    long_description = open('README.rst').read(),
    license = open('LICENSE').read(),
    scripts=[]
)
