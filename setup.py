import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

packages = [
    'skosprovider_rdf',
]

requires = [
    'skosprovider>=0.3.0a1',
    'rdflib',
]

setup(
    name='skosprovider_rdf',
    version='0.0',
    description='skosprovider_rdf',
    long_description=README + '\n\n' + CHANGES,
    package_data={'': ['LICENSE']},
    package_dir={'skosprovider_rdf': 'skosprovider_rdf'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='rdf skos skosprovider',
    packages=find_packages(),
    tests_require=requires,
    test_suite="skosprovider_rdf",
    entry_points="""\
    [paste.app_factory]
    main = skosprovider_rdf:main
    """,
)
