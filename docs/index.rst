.. ir-kit documentation master file, created by
   sphinx-quickstart on Thu Jun 29 11:39:19 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ir-kit's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   trec
   plot

Installing
----------

IR Kit can be installed via pip:

``pip3 install ir-kit``

Usage
-----

Command line tools:
^^^^^^^^^^^^^^^^^^^

For generating precision-recall curves and plotting the average precision of a topic there is trecplot:

``trecplot --help``

Libraries
^^^^^^^^^

Dealing with trec-related files is done using the ``trec`` package. This package contains classes for dealing with qrel
files, trec run files, and trec result files.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
