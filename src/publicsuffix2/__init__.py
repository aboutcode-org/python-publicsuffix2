# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 nexB Inc. and Renée Burton
# Copyright (c) 2015 nexB Inc.
# This code is based on Tomaž Šolc's fork of David Wilson's code originally at
# https://www.tablix.org/~avian/git/publicsuffix.git
#
# Copyright (c) 2014 Tomaž Šolc <tomaz.solc@tablix.org>
#
# David Wilson's code was originally at:
# from http://code.google.com/p/python-public-suffix-list/
#
# Copyright (c) 2009 David Wilson
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# The Public Suffix List vendored in this distribution has been downloaded
# from http://publicsuffix.org/public_suffix_list.dat
# This data file is licensed under the MPL-2.0 license.
# http://mozilla.org/MPL/2.0/

"""
Public Suffix List module for Python.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
from os import path
import warnings

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


PSL_URL = 'https://publicsuffix.org/list/public_suffix_list.dat'

BASE_DIR = path.dirname(__file__)
PSL_FILE = path.join(BASE_DIR, 'public_suffix_list.dat')
ABOUT_PSL_FILE = path.join(BASE_DIR, 'public_suffix_list.ABOUT')



class PublicSuffixList(object):

    def __init__(self, psl_file=None, idna=True):
        """
        Read and parse a public suffix list. `psl_file` is either a file
        location string, or a file-like object, or an iterable of lines from a
        public suffix data file.

        If psl_file is None, the vendored file named "public_suffix_list.dat" is
        loaded. It is stored side by side with this Python package.

        The Mozilla public suffix list is no longer IDNA-encoded, it is UTF-8.
        For use cases with domains that are IDNA encoded, choose idna=True and
        the list will be converted upon loading. The wrong encoding will provide
        incorrect answers in either use case.

        The file format is described at http://publicsuffix.org/

        :param psl_file: string or None
        :param idna: boolean, whether to convert file to IDNA-encoded strings
        """
        # Note: we test for None as we accept empty lists as inputs
        if psl_file is None or isinstance(psl_file, str):
            with codecs.open(psl_file or PSL_FILE, 'r', encoding='utf8') as psl:
                psl = psl.readlines()
        else:
            # assume file-like
            psl = psl_file

        # a list of eTLDs with their modifiers, e.g., *
        self.tlds = []
        root = self._build_structure(psl, idna)
        self.root = self._simplify(root)

    def _find_node(self, parent, parts):
        """
        Processing each line of the public suffix list recursively to build the
        Trie.  Each line is processed into a dictionary, which may contain sub-
        Trie, and nodes terminate in node of either 0 or 1 (negate).

        This method takes the current parent Trie, and searches it for the next
        part in the line (child). If not found, it adds a node to the Trie,
        creating a new branch with the [0]. If found, the existing sub-Trie is
        passed for the next part.

        :param parent: current Trie, form is Tuple (negate, dict of Trie)
        :param parts: list of strings
        :return: recursive search for remaining domain parts
        """
        if not parts:
            return parent

        # this initiates the Trie from a new node as [negate, dict()]
        if len(parent) == 1:
            parent.append({})

        assert len(parent) == 2
        _negate, children = parent

        child = parts.pop()

        # if child already exists as a node, grab the sub-Trie
        child_node = children.get(child, None)

        # if it doesn't exist, creates a new node and initialized with [0]
        if not child_node:
            children[child] = child_node = [0]

        return self._find_node(child_node, parts)

    def _add_rule(self, root, rule):
        """
        Initial setup for a line of the public suffix list. If it starts with !
        that is a negation operation. this calls the find_node() method
        recursively to build out the Trie for this rule.

        :param root: root Trie
        :param rule: string, line of public suffixlist
        :return: None
        """
        if rule.startswith('!'):
            negate = 1
            rule = rule[1:]
        else:
            negate = 0

        parts = rule.split('.')
        self._find_node(root, parts)[0] = negate

    def _simplify(self, node):
        """
        Condense the lines of the Trie in place.

        :param node: node in the Trie, either 0/1 or a subTrie
        :return: simplified Trie, form Tuple
        """
        if len(node) == 1:
            return node[0]

        return (node[0], dict((k, self._simplify(v)) for (k, v) in node[1].items()))

    def _build_structure(self, fp, idna):
        """
        Build a Trie from the public suffix list. If idna==True, idna-encode
        each line before building.

        The Trie is comprised of tuples that encode whether the line is a
        negation line (0 or 1), and terminate with 0. Each node is represented
        with two-tuple of the form (negate, dict of children / sub-Trie). A
        partial subTrie therefore looks like: (0, {'ac': 0, 'co': (0,
        {'blogspot': 0}), 'gv': 0,....}) where each tuple starts with the
        negation encoding, and each leaf in the Trie as a dictionary element
        returns 0.

        Also creates an instance attribute, tlds, which simply contains the
        publicsuffix list, with the modifiers such as wildcards, as a list. This
        can be accessed for post-processing by the application.

        :param fp: pointer for the public suffix list
        :param idna: boolean, convert lines to idna-encoded strings
        :return: Trie
        """
        root = [0]

        tlds = self.tlds

        for line in fp:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            if idna:
                line = line.encode('idna').decode()
            tlds.append(line)

            self._add_rule(root, line.split()[0].lstrip('.'))

        return root

    def _lookup_node(self, matches, depth, parent, parts, wildcard):
        """
        Traverses the Trie recursively to find the parts. By default, the
        traverse follows wildcards, as appropriate for the public suffix list,
        but if wildcard is set to False, it will stop at wildcard leaves. This
        can be useful for summarizing complex wildcard domains like those under
        amazonaws.com.

        The lookup is tracked via a list, initially set to all None, that marks
        the negation flags of nodes it matches. each match will be marked for
        later composition of the eTLD.

        :param matches: list, parts long, None (initial), 0, or 1
        :param depth: int, how far in the Trie this run is
        :param parent: Tuple, the current subTrie
        :param parts: list of domain parts, strings
        :param wildcard: boolean, whether to process wildcard nodes
        :return: None, recursive call
        """
        if wildcard and depth == 1:
            # if no rules match, the prevailing rule is "*"
            # See: Algorithm 2 at https://publicsuffix.org/list/
            matches[-depth] = 0

        if parent in (0, 1):
            return

        children = parent[1]

        if depth <= len(parts) and children:
            for name in ('*', parts[-depth]):
                child = children.get(name, None)
                if child is not None:
                    if wildcard or name != '*':
                        if child in (0, 1):
                            negate = child
                        else:
                            negate = child[0]
                        matches[-depth] = negate
                        self._lookup_node(matches, depth + 1, child, parts, wildcard)

    def get_sld(self, domain, wildcard=True, strict=False):
        """
        Return the second-level-domain (SLD) or private suffix of a given domain
        according to the public suffix list. The public suffix list includes
        wildcards, so if wildcard is set to True, this will follow the wildcard
        on traversal, otherwise it will stop at wildcard nodes.

        The logic does not check by default whether the TLD is in the Trie, so
        for example, 'www.this.local' will return 'this.local'. If you want to
        ensure the TLD is in the public suffix list, use strict=True.

        If domain is already an eTLD, it returns domain as-is instead of None
        value.

        :param domain: string, needs to match the encoding of the PSL (idna or UTF8)
        :param wildcard: boolean, follow wildcard patterns
        :param strict: boolean, check the TLD is valid, return None if not
        :return: string, the SLD for the domain
        """
        if not domain or len(domain) == 0:
            return None
        domain = domain.lower()
        return self.get_sld_unsafe(domain, wildcard, strict)

    def get_sld_unsafe(self, domain, wildcard=True, strict=False):
        """
        Return the second-level-domain (SLD) or private suffix of a given domain
        according to the public suffix list. The public suffix list includes
        wildcards, so if wildcard is set to True, this will follow the wildcard
        on traversal, otherwise it will stop at wildcard nodes.

        The logic does not check by default whether the TLD is in the Trie, so
        for example, 'www.this.local' will return 'this.local'. If you want to
        ensure the TLD is in the public suffix list, use strict=True.

        If domain is already an eTLD, it returns domain as-is instead of None
        value.

        In difference from get_sld method this method does not perform validation
        of the input string, transformation it to the lowercase or trimming of
        taildot.

        :param domain: string, needs to match the encoding of the PSL (idna or UTF8)
        :param wildcard: boolean, follow wildcard patterns
        :param strict: boolean, check the TLD is valid, return None if not
        :return: string, the SLD for the domain

        """
        tld = self.get_tld_unsafe(domain, wildcard, strict)
        if tld is None:
            return None
        rest = len(domain) - len(tld)
        if rest == 0:
            return tld
        else:
            sld_idx = domain.rfind('.', 0, rest - 1) + 1  # will be rest + 1 iff empty label
            return domain[sld_idx:] if rest - sld_idx > 1 else None

    def get_public_suffix(self, domain, wildcard=True, strict=False):
        """
        Use get_sld() instead.
        """
        return self.get_sld(domain, wildcard, strict)

    def get_tld(self, domain, wildcard=True, strict=False):
        """
        Return the TLD, or public suffix, of a domain using the public suffix
        list. uses wildcards if set, and checks for valid top TLD is
        strict=True.

        This will return the domain itself when it is an ICANN TLD, e.g., 'com'
        returns 'com', for follow on processing, while 'co.uk' return 'uk'. On
        the other hand, more complicated domains will return their public
        suffix, e.g.,
        'google.co.uk' will return 'co.uk'.  Root ('.') will return empty string.

        :param domain: string
        :param wildcard: boolean, follow wildcards in Trie
        :param strict: boolean, check that top TLD is valid in Trie
        :return: string, the TLD for the domain
        """
        if domain is None:
            return None
        domain = domain.lower()

        return self.get_tld_unsafe(domain, wildcard, strict)

    def get_tld_unsafe(self, domain, wildcard=True, strict=False):
        """
        Return the TLD, or public suffix, of a domain using the public suffix
        list. uses wildcards if set, and checks for valid top TLD is
        strict=True. The input domain should not have root '.' in the end.

        This will return the domain itself when it is an ICANN TLD, e.g., 'com'
        returns 'com', for follow on processing, while 'co.uk' return 'uk'. On
        the other hand, more complicated domains will return their public
        suffix, e.g., 'google.co.uk' will return 'co.uk'.

        Empty labels are not allowed:

        '.' -> <empty>.<empty> -> None

        'com.' -> <com>.<empty> -> None

        '.com' -> <empty>.<com> -> 'com'

        In difference from get_sld method this method does not perform validation
        of the input string, transformation it to the lowercase or trimming of
        taildot.

        :param domain: string the domain which TLD should be matched, without trailing '.'
        :param wildcard: boolean, follow wildcards in Trie
        :param strict: boolean, check that top TLD is valid in Trie
        :return: string, the TLD for the domain
        """
        lbl_end = -1
        lbl_start = len(domain)

        tld_start = None
        root = self.root
        if root == 0:  # exhausted case - empty root. Use last label as TLD if not strict
            lbl_start = None if strict else domain.rfind('.')

        while type(root) is tuple:
            if root[0] == 0:
                tld_start = lbl_start
            if lbl_start == -1:
                break
            lbl_end = lbl_start
            lbl_start = domain.rfind('.', 0, lbl_end)
            if len(domain[lbl_start + 1:lbl_end]) == 0:
                break
            p1 = root[1].get(domain[lbl_start + 1:lbl_end])
            root = root[1].get("*") if p1 is None and wildcard else p1

        if root == 0:
            tld_start = lbl_start
        # elif root == 1:  # we already have tld_start point to previous label
        #     tld_start = lbl_end
        elif root is None:  # only last label
            if strict or tld_start is not None and tld_start != len(domain):
                tld_start = lbl_end
            else:
                tld_start = lbl_start

        tld = domain[tld_start + 1:] if tld_start is not None else None
        return tld or None  # empty string -> None

    def get_components(self, domain: str, wildcard=True, strict=False) -> (str, str, str):
        """
        Returns 3-tuple of components of the domain name: (prefix, SLL, TLD/eTLD)
        where
        * TLD/ETLD is top-level domain (extended top-level domain) per publicsuffix
        * SLL - second level (registrable domain) label (the label on immediately
                on the left of TLD/eTLD. None if only TLD is present.
        * prefix - all the labels on the left side of TLD/eTLD. None if not present
        This method does not validate the conformity of prefix to DNS requirements.
        Note: this function as well as the appropriate method of PublicSuffixList
        class is crafted for use in bulk-processors (such as pandas), therefore it
        always returns 3-tuple:

        <code>
        psl = ps2.PublicSuffixList(idna=True)
        df['prefix']['sll']['tld'] = zip(*df.domain.apply(ps2.get_component)
        df = df.dropna(subset=['prefix','sll','tld'])
        </code>

        Examples of domain decomposition:
            '.' -> (None, None, None)
            'com.' -> (None, None, None)
            'com' -> (None, None, 'com')
            'google.com' -> (None, 'google', 'com')
            'www.google.com' -> ('www', 'google', 'com')
            'mail.l.google.com' -> ('mail.l', 'google', 'com')
            'mail.l..com' -> ('mail.l', 'None', 'com') - invalid case - empty label
            '.......com' -> ('.....', 'None', 'com') - invalid case - empty labels

        Optionally read, and parse a public suffix list. `psl_file` is either a file
        location string, or a file-like object, or an iterable of lines from a
        public suffix data file.

        If psl_file is None, the vendored file named "public_suffix_list.dat" is
        loaded. It is stored side by side with this Python package.

        The file format is described at http://publicsuffix.org/

        :param domain: string - domain name without trailing '.'
        :param wildcard: bool - whether wildcard rules are supported
        :param strict: bool - disable unknown TLDs
        :return: 3-tuple, (prefix, SLL, TLD/eTLD)
        """
        if not domain or len(domain) == 0:
            return None, None, None
        domain = domain.lower()
        return self.get_components_unsafe(domain, wildcard, strict)

    def get_components_unsafe(self, domain: str, wildcard=True, strict=False) -> (str, str, str):
        """
        This is unsafe method that does not checks if the domain is None. Also it does
        not perform conversion of the domain into lowercase.
        """

        tld = self.get_tld_unsafe(domain, wildcard, strict)
        sld = None
        prefix = None

        if tld is not None:
            sld_end_idx = len(domain) - len(tld) - 1
            if sld_end_idx > 0:
                idx = domain.rfind('.', 0, sld_end_idx)
                prefix = domain[:idx] if idx > 0 else None
                sld = domain[idx + 1:sld_end_idx]
                sld = None if len(sld) == 0 else sld
        return prefix, sld, tld


_PSL = None


def get_components(domain, psl_file=None, wildcard=True, idna=True, strict=False):
    """
    Returns 3-tuple of components of the domain name: (prefix, SLL, TLD/eTLD)
    where
    * TLD/ETLD is top-level domain (extended top-level domain) per publicsuffix
    * SLL - second level (registrable domain) label (the label on immediately
            on the left of TLD/eTLD. None if only TLD is present.
    * prefix - all the labels on the left side of TLD/eTLD. None if not present
    This method does not validate the conformity of prefix to DNS requirements.
    Note: this function as well as the appropriate method of PublicSuffixList
    class is crafted for use in bulk-processors (such as pandas), therefore it
    always returns 3-tuple:

    ```
    df['prefix']['sll']['tld'] = zip(*df.domain.apply(get_component, idna=True)
    df = df.dropna(subset=['prefix','sll','tld'])
    ```

    Examples of domain decomposition:
        '.' -> (None, None, None)
        'com.' -> (None, None, None)
        'com' -> (None, None, 'com')
        'google.com' -> (None, 'google', 'com')
        'www.google.com' -> ('www', 'google', 'com')
        'mail.l.google.com' -> ('mail.l', 'google', 'com')
        'mail.l..com' -> ('mail.l', 'None', 'com') - invalid case - empty label
        '.......com' -> ('.....', 'None', 'com') - invalid case - empty labels

    Optionally read, and parse a public suffix list. `psl_file` is either a file
    location string, or a file-like object, or an iterable of lines from a
    public suffix data file.

    If psl_file is None, the vendored file named "public_suffix_list.dat" is
    loaded. It is stored side by side with this Python package.

    The file format is described at http://publicsuffix.org/

    Convenience function that builds and caches a PublicSuffixList object.
    NOTE: this function caches the first set of parameters thar were used. If we
    have two subsequent calls:
    ```
        split_domain(domain, idna=False)
        split_domain(domain, idna=True)
    ```
    the second call will use the same non-idna publicsuffix as the first one.
    Use with caution.

    :param psl_file: the file name, if not available built in is used
    :param idna: only idna part of the public suffix is used
    :param domain: string - domain name without trailing '.'
    :param wildcard: bool - whether wildcard rules are supported
    :param strict: bool - disable unknown TLDs
    :return: 3-tuple, (prefix, SLL, TLD/eTLD)
    """
    global _PSL
    _PSL = _PSL or PublicSuffixList(psl_file, idna=idna)
    return _PSL.get_components(domain, wildcard=wildcard, strict=strict)


def get_sld(domain, psl_file=None, wildcard=True, idna=True, strict=False):
    """
    Return the private suffix or SLD for a `domain` DNS name string. The
    original publicsuffix2 library used the method get_public_suffix() for this
    purpose, but get_private_suffix() is more proper.

    Optionally read, and parse a public suffix list. `psl_file` is either a file
    location string, or a file-like object, or an iterable of lines from a
    public suffix data file.

    If psl_file is None, the vendored file named "public_suffix_list.dat" is
    loaded. It is stored side by side with this Python package.

    The file format is described at http://publicsuffix.org/

    Convenience function that builds and caches a PublicSuffixList object.
    NOTE: this function caches the first set of parameters thar were used. If we
    have two subsequent calls:
    ```
        get_sld(domain, idna=False)
        get_sld(domain, idna=True)
    ```
    the second call will use the same non-idna publicsuffix as the first one.
    Use with caution.

    :param psl_file: the file name, if not available built in is used
    :param idna: only idna part of the public suffix is used
    :param domain: string - domain name without trailing '.'
    :param wildcard: bool - whether wildcard rules are supported
    :param strict: bool - disable unknown TLDs
    :return: second-level (registrable) domain that is TLD/eTLD + one label on the left
        if only TLD is found it is returned. None if empty label or invalid input
    """
    global _PSL
    _PSL = _PSL or PublicSuffixList(psl_file, idna=idna)
    return _PSL.get_sld(domain, wildcard=wildcard, strict=strict)


def get_tld(domain, psl_file=None, wildcard=True, idna=True, strict=False):
    """
    Return the TLD or public suffix for a `domain` DNS name string. (this is
    actually the private suffix that is returned)

    Optionally read, and parse a public suffix list. `psl_file` is either a file
    location string, or a file-like object, or an iterable of lines from a
    public suffix data file.

    If psl_file is None, the vendored file named "public_suffix_list.dat" is
    loaded. It is stored side by side with this Python package.

    The file format is described at http://publicsuffix.org/

    Convenience function that builds and caches a PublicSuffixList object.
    NOTE: this function caches the first set of parameters thar were used. If we
    have two subsequent calls:
    ```
        get_tld(domain, idna=False)
        get_tld(domain, idna=True)
    ```
    the second call will use the same non-idna publicsuffix as the first one.
    Use with caution.

    :param psl_file: the file name, if not available built in is used
    :param idna: only idna part of the public suffix is used
    :param domain: string - domain name without trailing '.'
    :param wildcard: bool - whether wildcard rules are supported
    :param strict: bool - disable unknown TLDs
    :return: TLD/eTLD or None
    """
    global _PSL
    _PSL = _PSL or PublicSuffixList(psl_file, idna=idna)
    return _PSL.get_tld(domain, wildcard=wildcard, strict=strict)


def get_public_suffix(domain, psl_file=None, wildcard=True, idna=True, strict=False):
    """
    Included for compatibility with the original publicsuffix2 library -- this
    function returns the private suffix or SLD of the domain. To get the public
    suffix, use get_tld().

    Optionally read, and parse a public suffix list. `psl_file` is either a file
    location string, or a file-like object, or an iterable of lines from a
    public suffix data file.

    If psl_file is None, the vendored file named "public_suffix_list.dat" is
    loaded. It is stored side by side with this Python package.

    The file format is described at http://publicsuffix.org/
    """
    warnings.warn(
        'This function returns the private suffix, SLD, or registrable domain. '
        'This equivalent to function get_sld(). '
        'To get the public suffix itself, use get_tld().',
        UserWarning
    )
    return get_sld(domain, psl_file, wildcard, idna, strict)


def fetch():
    """
    Return a file-like object for the latest public suffix list downloaded from
    publicsuffix.org
    """
    req = Request(PSL_URL, headers={'User-Agent': 'python-publicsuffix2'})
    res = urlopen(req)
    try:
        encoding = res.headers.get_content_charset()
    except AttributeError:
        encoding = res.headers.getparam('charset')
    f = codecs.getreader(encoding)(res)
    return f
