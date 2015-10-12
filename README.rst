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
usable out of the box. Newer versions try to provide reasonably fresh copies of
this list. It also includes a convenience method to fetch the latest list.

The code is a fork of the publicsuffix package and uses the same module name and
base API.

The code is MIT-licensed and the publicsuffix data list is MPL-2.0-licensed.

.. image:: https://api.travis-ci.org/pombredanne/python-publixsuffix2.png?branch=master
   :target: https://travis-ci.org/pombredanne/python-publixsuffix2
   :alt: master branch tests status

.. image:: https://api.travis-ci.org/pombredanne/python-publixsuffix2.png?branch=develop
   :target: https://travis-ci.org/pombredanne/python-publixsuffix2
   :alt: develop branch tests status


Usage
-----

Install with::

    pip install publicsuffix2

The module provides a function to query a domain name::

    >>> from publicsuffix import get_public_suffix
    >>> get_public_suffix('www.example.com')
    'example.com'
    >>> get_public_suffix('www.example.co.uk')
    'example.co.uk'
    >>> get_public_suffix('www.super.example.co.uk')
    'example.co.uk'

This function loads and caches the public suffix list.

For more control and compatibility, there is also a class that parses a Public
Suffix List and allows the same queries on individual domain names::

    >>> from publicsuffix import PublicSuffixList
    >>> psl= PublicSuffixList()
    >>> psl.get_public_suffix('www.example.com')
    'example.com'
    >>> psl.get_public_suffix('www.example.co.uk')
    'example.co.uk'
    >>> psl.get_public_suffix('www.super.example.co.uk')
    'example.co.uk'

Note that the ``host`` part of an URL can contain strings that are
not plain DNS domain names (IP addresses, Punycode-encoded names, name in
combination with a port number or a username, etc.). It is up to the
caller to ensure only domain names are passed to the get_public_suffix()
method.


The get_public_suffix function and the PublicSuffixList class initializer accept
an optional argument pointing to a public suffix file. This can either be a file
path, an iterable of public suffix lines, or a file-like object pointing to an
opened list. The fetch function fetches the latest list::

    >>> from publicsuffix import get_public_suffix, fetch
    >>> latest = fetch()
    >>> get_public_suffix('www.example.com', latest)
    'example.com'

This will use the cached latest loaded above::

    >>> get_public_suffix('www.example.co.uk')
    'example.co.uk'



Source
------

Get a local copy of the development repository. The development takes 
place in the ``develop`` branch. Stable releases are tagged in the ``master``
branch::

    git clone https://github.com/pombredanne/python-publicsuffix2.git


History
-------
This code is forked from Tomaž Šolc's fork of David Wilson's code originally at:
https://www.tablix.org/~avian/git/publicsuffix.git
Copyright (c) 2014 Tomaž Šolc <tomaz.solc@tablix.org>

The API is essentially the same as publicsuffix including using the same package
name to allow a straight forward replacement.

David Wilson's code was originally at:
from http://code.google.com/p/python-public-suffix-list/
Copyright (c) 2009 David Wilson


License
-------

The code is MIT-licensed. 
The vendored public suffix list data from Mozilla is under the MPL-2.0.


Copyright (c) 2015 nexB Inc.
Copyright (c) 2014 Tomaž Šolc <tomaz.solc@tablix.org>
Copyright (c) 2009 David Wilson
  
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
  
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
  
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
