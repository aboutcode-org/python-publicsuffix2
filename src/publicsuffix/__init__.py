# -*- coding: utf-8 -*-
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
import os.path


class PublicSuffixList(object):

    def __init__(self, input_file=None):
        """
        Read and parse a public suffix list.
        input_file is a file-like object or lines iterable from a publicsuffix
        data file. If input_file is None, the vendored file named
        "public_suffix_list.dat" is loaded. It is stored side by side with this
        Python package.

        The file format is described at http://publicsuffix.org/
        """

        # Note: we test for None as we accept empty lists as inputs
        if input_file is None:
            base_dir = os.path.dirname(__file__)
            input_path = os.path.join(base_dir, 'public_suffix_list.dat')
            input_file = codecs.open(input_path, 'r', 'utf8')

        root = self._build_structure(input_file)
        self.root = self._simplify(root)

    def get_public_suffix(self, domain):
        """
        Return the public suffix for a `domain` name.

        For example::
            >>> get_public_suffix("www.example.com")
            "example.com"

        Note that for internationalized domains the list at
        http://publicsuffix.org uses decoded names, so it is
        up to the caller to decode any Punycode-encoded names.
        """

        parts = domain.lower().strip('.').split('.')
        hits = [None] * len(parts)

        self._lookup_node(hits, 1, self.root, parts)

        for i, what in enumerate(hits):
            if what is not None and what == 0:
                return '.'.join(parts[i:])

    def _find_node(self, parent, parts):
        if not parts:
            return parent

        if len(parent) == 1:
            parent.append({})

        assert len(parent) == 2
        _negate, children = parent

        child = parts.pop()

        child_node = children.get(child, None)

        if not child_node:
            children[child] = child_node = [0]

        return self._find_node(child_node, parts)

    def _add_rule(self, root, rule):
        if rule.startswith('!'):
            negate = 1
            rule = rule[1:]
        else:
            negate = 0

        parts = rule.split('.')
        self._find_node(root, parts)[0] = negate

    def _simplify(self, node):
        if len(node) == 1:
            return node[0]

        return (node[0], dict((k, self._simplify(v)) for (k, v) in node[1].items()))

    def _build_structure(self, fp):
        root = [0]

        for line in fp:
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            self._add_rule(root, line.split()[0].lstrip('.'))

        return root

    def _lookup_node(self, matches, depth, parent, parts):
        if parent in (0, 1):
            negate = parent
            children = None
        else:
            negate, children = parent

        matches[-depth] = negate

        if depth < len(parts) and children:
            for name in ('*', parts[-depth]):
                child = children.get(name, None)
                if child is not None:
                    self._lookup_node(matches, depth + 1, child, parts)
