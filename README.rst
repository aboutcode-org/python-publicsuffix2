Public Suffix List module for Python
====================================

This module allows you to get the public suffix, as well as the registrable domain,
 of a domain name using the Public Suffix List from http://publicsuffix.org

A public suffix is a domain suffix under which you can register domain
names. It is sometimes referred to as the extended TLD (eTLD).
Some examples of public suffixes are ".com", ".co.uk" and "pvt.k12.wy.us".
Accurately knowing the public suffix of a domain is useful when handling
web browser cookies, highlighting the most important part of a domain name
in a user interface or sorting URLs by web site.

This module builds the public suffix list as a Trie structure, making it more efficient
than other string-based modules available for the same purpose. It can be used
effectively in large-scale distributed environments, such as PySpark.

This Python module includes with a copy of the Public Suffix List so that it is
usable out of the box. Newer versions try to provide reasonably fresh copies of
this list. It also includes a convenience method to fetch the latest list.

The code is a fork of the publicsuffix2 package and includes the same base API. In
addition, it contains a few variants useful for certain use cases, such as the option to
ignore wildcards or return only the extended TLD (eTLD).
Publicsuffix2 is a an extension of publicsuffix, and uses the same base API.
You just need to import publicsuffix2 instead.

The public suffix list is now provided in UTF-8 format. To correctly process
IDNA-encoded domains, either the query or the list must be converted. This module
contains the option to IDNA-encode the public suffix list upon creating the Trie; this
is set to happen by default. If your use case includes UTF-8 domains, e.g., '食狮.com.cn',
you'll need to set the IDNA-encoding flag to False on instantiation (see examples below).
Failure to use the correct encoding for your use case can lead to incorrect results for
domains that utilize unicode characters.

The code is MIT-licensed and the publicsuffix data list is MPL-2.0-licensed.

.. image:: https://api.travis-ci.org/nexB/python-publicsuffix2.png?branch=master
   :target: https://travis-ci.org/nexB/python-publicsuffix2
   :alt: master branch tests status

.. image:: https://api.travis-ci.org/nexB/python-publicsuffix2.png?branch=develop
   :target: https://travis-ci.org/nexB/python-publicsuffix2
   :alt: develop branch tests status


Usage
-----

To install from source, first build the package file:
    python setup.py build sdist
and then pip install from the dist directory.

Install with::

    pip install publicsuffix2

The module provides a function to query a domain name::

    >>> from publicsuffix2 import get_public_suffix
    >>> get_public_suffix('www.example.com')
    'example.com'
    >>> get_public_suffix('www.example.co.uk')
    'example.co.uk'
    >>> get_public_suffix('www.super.example.co.uk')
    'example.co.uk'

This function loads and caches the public suffix list.

For more control, there is also a class that parses a Public
Suffix List and allows the same queries on individual domain names::

    >>> from publicsuffix2 import PublicSuffixList
    >>> psl = PublicSuffixList()
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


The get_public_suffix() function and the PublicSuffixList class initializer accept
an optional argument pointing to a public suffix file. This can either be a file
path, an iterable of public suffix lines, or a file-like object pointing to an
opened list::

    >>> from publicsuffix import get_public_suffix
    >>> psl_file = 'path to some psl data file'
    >>> get_public_suffix('www.example.com', psl_file)
    'example.com'

Note that when using get_public_suffix() a global cache keeps the latest provided
suffix list data.  This will use the cached latest loaded above::

    >>> get_public_suffix('www.example.co.uk')
    'example.co.uk'


To update the bundled suffix list use the provided setup.py command::

    python setup.py update_psl
    
The update list will be saved in `src/publicsuffix2/public_suffix_list.dat`
and you can build a new wheel with this bundled data.

Alternatively, there is a fetch() function that will fetch the latest version
of a Public Suffix data file from https://publicsuffix.org/list/public_suffix_list.dat
You can use it this way::

    >>> from publicsuffix import get_public_suffix
    >>> from publicsuffix import fetch
    >>> psl_file = fetch()
    >>> get_public_suffix('www.example.com', psl_file)
    'example.com'

Note that the once loaded, the data file is cached and therefore fetched only
once.

If using this library in large-scale pyspark processing, you should instantiate the class as
a global variable, not within a user function. The class methods can then be used within user
functions for distributed processing.

Changes in this Fork
--------------------

This fork of publicsuffix2 addresses a change in the format to the standard public suffix list,
which was previously IDNA-encoded and now is in UTF-8 format, as well as some additional
functionality useful to certain use cases. These additions include the ability to ignore
wildcards and to require strict adherence to the TLDs included in the list. Lastly, we include
some convenience functions for obtaining only the extended TLD (eTLD) rather than the
registrable domain (SLD). These are outlined below.

IDNA-encoding. The public suffix list is now provided in UTF-8 format. For those use cases that
include IDNA-encoded domains, the module will not return accurate results unless the list is
converted. In this fork, IDNA encoding is included as a parameter in the class and is on by
default.::

    >>> from publicsuffix2 import PublicSuffixList
    >>> psl = PublicSuffixList(idna=True)  # on by default
    >>> psl.get_public_suffix('www.google.com')
    'google.com'
    >>> psl = PublicSuffixList(idna=False)  # use UTF-8 encodings
    >>> psl.get_public_suffix('食狮.com.cn')
    '食狮.com.cn'

Ignore wildcards. In some use cases, particularly those related to large-scale domain processing,
the user might want to ignore wildcards to create more aggregation. This is possible by setting
the parameter wildcard=False.

Require valid eTLDs (strict). In the publicsuffix2 module, a domain with an invalid TLD will still return
a public suffix, e.g,::

    >>> psl.get_public_suffix('www.mine.local')
    'mine.local'


This is useful for many use cases, while in others, we want to ensure that the domain includes a
valid eTLD. In this case, the boolean parameter strict provides a solution. If this flag is set,
an invalid TLD will return None.::

    >>> psl.get_public_suffix('www.mine.local', strict=True) is None
    True

Return eTLD only. The standard use case for publicsuffix2 is to return the registrable domain
according to the public suffix list. In some cases, however, we only wish to find the eTLD
itself. In this fork, this is available via the get_tld() method.::

    >>> psl.get_tld('www.google.com')
    'com'

All of the methods and functions include the wildcard and strict parameters.

For convenience, the public method get_sld() is available. This is identical to the method
get_public_suffix() and is intended to clarify the output for some users.


Source
------

Get a local copy of the development repository. The development takes 
place in the ``develop`` branch. Stable releases are tagged in the ``master``
branch::

    git clone https://github.com/nexB/python-publicsuffix2.git


History
-------
This code is forked from NexB's fork of Tomaž Šolc's fork of David Wilson's code.

The original publicsuffix2 code is Copyright (c) 2015 nexB Inc.

David Wilson's code originally at:

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

Copyright (c) 2019 Renée Burton

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
