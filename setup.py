import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'HISTORY.rst')) as f:
    HISTORY = f.read()

packages = [
    'skosprovider_rdf',
]

requires = [
    'skosprovider>=0.5.0',
    'rdflib',
    'html5lib'
]

setup(
    name='skosprovider_rdf',
    version='0.5.0.dev0',
    description='skosprovider_rdf',
    long_description=README + '\n\n' + HISTORY,
    package_data={'': ['LICENSE']},
    package_dir={'skosprovider_rdf': 'skosprovider_rdf'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    url='http://github.com/OnroerendErfgoed/skosprovider_rdf',
    keywords='rdf skos skosprovider vocabularies thesauri',
    packages=find_packages(),
    tests_require=requires,
    test_suite="skosprovider_rdf"
)
