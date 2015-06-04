Public Suffix List module for Python
====================================

This module allows you to get the public suffix of a domain name using the
Public Suffix List from http://publicsuffix.org

A public suffix is a domain suffix under which you can register domain
names. Some examples of public suffixes are .com, .co.uk and pvt.k12.wy.us.
Accurately knowing the public suffix of a domain is useful when handling
web browser cookies, highlighting the most important part of a domain name
in a user interface or sorting URLs by web site.

This Python module includes with a copy of the Public Suffix List so that it is
usable out of the box. Newer version try to provide reasonably fresh copies of
this list.

The code is a fork of the publicsuffix package and uses the same module name and
API.

The code is MIT-licensed and the publicsuffix data list is MPL-2.0-licensed.

Usage
-----

Install with::
    pip install publicsuffix2

The module exports a single class that parses the Public Suffix List and allows
queries for individual domain names::

    >>> from publicsuffix import PublicSuffixList
    >>> psl = PublicSuffixList()
    >>> psl.get_public_suffix("www.example.com")
    'example.com'

Note that the ``host`` part of an URL can contain strings that are
not plain DNS domain names (IP addresses, Punycode-encoded names, name in
combination with a port number or an username, etc.). It is up to the
caller to ensure only domain names are passed to the get_public_suffix()
method.


Source
------

Get a local copy of the development repository. The development takes 
place in the ``develop`` branch. Stable releases are tagged in the ``master``
branch::

    git clone https://github.com/pombredanne/python-publicsuffix2.git
