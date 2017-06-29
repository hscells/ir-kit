IR Kit
======

Information Retrieval Kit - Utilities for IR in python

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