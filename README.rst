skosprovider_rdf
================

⚠️ This package is deprecated. Use skosprovider_ instead.

Starting from `skosprovider` 2.0.0 the functionality of this package has been
merged into the main `skosprovider <https://github.com/OnroerendErfgoed/skosprovider/>`_
repository. This package will remain usable with ``skosprovider < 2.0.0``, but is
no longer actively maintained. It is recommended to upgrade to
``skosprovider >= 2.0.0`` and use ``skosprovider_rdf`` from there.

Migrating to skosprovider 2.0.0
-------------------------------

1. Uninstall ``skosprovider_rdf`` and install ``skosprovider >= 2.0.0``::

       pip uninstall skosprovider_rdf
       pip install "skosprovider>=2.0.0"

2. Replace any ``skosprovider_rdf`` imports with their equivalent under
   ``skosprovider`` (see the `skosprovider
   <https://github.com/OnroerendErfgoed/skosprovider/>`_ documentation for the
   full mapping).

An implementation of the skosprovider_ interface that supports various RDF
serialisations through RDFLib.

.. image:: https://img.shields.io/pypi/v/skosprovider_rdf.svg
        :target: https://pypi.python.org/pypi/skosprovider_rdf
.. image:: https://readthedocs.org/projects/skosprovider_rdf/badge/?version=latest
        :target: https://readthedocs.org/projects/skosprovider_rdf/?badge=latest
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7002514.svg
        :target: https://doi.org/10.5281/zenodo.7002514
.. image:: https://app.travis-ci.com/OnroerendErfgoed/skosprovider_rdf.svg?branch=develop
        :target: https://app.travis-ci.com/OnroerendErfgoed/skosprovider_rdf
.. image:: https://img.shields.io/coveralls/OnroerendErfgoed/skosprovider_rdf.svg
        :target: https://coveralls.io/r/OnroerendErfgoed/skosprovider_rdf
.. image:: https://scrutinizer-ci.com/g/OnroerendErfgoed/skosprovider_rdf/badges/quality-score.png?b=master
        :target: https://scrutinizer-ci.com/g/OnroerendErfgoed/skosprovider_rdf/?branch=master

.. _skosprovider: https://github.com/OnroerendErfgoed/skosprovider

