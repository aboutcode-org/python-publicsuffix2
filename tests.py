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


from __future__ import absolute_import
from __future__ import print_function

import publicsuffix
import unittest
import sys


if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


class TestPublicSuffix(unittest.TestCase):

    def test_get_public_suffix_from_empty_list(self):
        psl = publicsuffix.PublicSuffixList([])

        assert 'com' == psl.get_public_suffix('com')
        assert 'com' == psl.get_public_suffix('COM')
        assert 'com' == psl.get_public_suffix('.com')
        assert 'com' == psl.get_public_suffix('a.example.com')

    def test_get_public_suffix_from_list(self):
        psl = publicsuffix.PublicSuffixList(['com'])

        assert 'example.com' == psl.get_public_suffix('a.example.com')
        assert 'example.com' == psl.get_public_suffix('a.a.example.com')
        assert 'example.com' == psl.get_public_suffix('a.a.a.example.com')
        assert 'example.com' == psl.get_public_suffix('A.example.com')
        assert 'example.com' == psl.get_public_suffix('.a.a.example.com')

    def test_get_public_suffix_from_list_with_exception_rule(self):
        psl = publicsuffix.PublicSuffixList(['*.example.com', '!b.example.com'])

        assert 'a.example.com' == psl.get_public_suffix('a.example.com')
        assert 'a.a.example.com' == psl.get_public_suffix('a.a.example.com')
        assert 'a.a.example.com' == psl.get_public_suffix('a.a.a.example.com')
        assert 'a.a.example.com' == psl.get_public_suffix('a.a.a.a.example.com')

        assert 'b.example.com' == psl.get_public_suffix('b.example.com')
        assert 'b.example.com' == psl.get_public_suffix('b.b.example.com')
        assert 'b.example.com' == psl.get_public_suffix('b.b.b.example.com')
        assert 'b.example.com' == psl.get_public_suffix('b.b.b.b.example.com')

    def test_get_public_suffix_from_list_with_fqdn(self):
        psl = publicsuffix.PublicSuffixList(['com'])

        assert 'example.com' == psl.get_public_suffix('example.com.')

    def test_get_public_suffix_from_list_with_unicode(self):
        psl = publicsuffix.PublicSuffixList([u('\u0440\u0444')])

        assert u('\u0440\u0444') == psl.get_public_suffix(u('\u0440\u0444'))
        assert u('example.\u0440\u0444') == psl.get_public_suffix(u('example.\u0440\u0444'))
        assert u('example.\u0440\u0444') == psl.get_public_suffix(u('a.example.\u0440\u0444'))
        assert u('example.\u0440\u0444') == psl.get_public_suffix(u('a.a.example.\u0440\u0444'))

    def test_fetch_amd_get_public_suffix(self):
        f = publicsuffix.fetch()
        psl = publicsuffix.PublicSuffixList(f)
        assert 'example.com' == psl.get_public_suffix('www.example.com')
        assert u('www.\u9999\u6e2f') == psl.get_public_suffix(u('www.\u9999\u6e2f'))

    def test_get_public_suffix_from_builtin_full_publicsuffix_org_using_func(self):
        assert 'com' == publicsuffix.get_public_suffix('COM')
        assert 'example.com' == publicsuffix.get_public_suffix('example.COM')
        assert 'example.com' == publicsuffix.get_public_suffix('WwW.example.COM')


class TestPublicSuffixCurrent(unittest.TestCase):
    """Test using the vendored list"""
    psl = None

    def test_get_public_suffix_from_builtin_full_publicsuffix_org(self):
        psl = publicsuffix.PublicSuffixList(self.psl)

        # Mixed case.
        assert 'com' == psl.get_public_suffix('COM')
        assert 'example.com' == psl.get_public_suffix('example.COM')
        assert 'example.com' == psl.get_public_suffix('WwW.example.COM')

        # Leading dot.
        assert 'com' == psl.get_public_suffix('.com')
        assert 'example' == psl.get_public_suffix('.example')
        assert 'example.com' == psl.get_public_suffix('.example.com')
        assert 'example' == psl.get_public_suffix('.example.example')

        # Unlisted TLD.
        assert 'example' == psl.get_public_suffix('example')
        assert 'example' == psl.get_public_suffix('example.example')
        assert 'example' == psl.get_public_suffix('b.example.example')
        assert 'example' == psl.get_public_suffix('a.b.example.example')

        # Listed, but non-Internet, TLD.
        assert 'local' == psl.get_public_suffix('local')
        assert 'local' == psl.get_public_suffix('example.local')
        assert 'local' == psl.get_public_suffix('b.example.local')
        assert 'local' == psl.get_public_suffix('a.b.example.local')

        # TLD with only one rule.
        assert 'biz' == psl.get_public_suffix('biz')
        assert 'domain.biz' == psl.get_public_suffix('domain.biz')
        assert 'domain.biz' == psl.get_public_suffix('b.domain.biz')
        assert 'domain.biz' == psl.get_public_suffix('a.b.domain.biz')

        # TLD with some two-level rules.
        assert 'com' == psl.get_public_suffix('com')
        assert 'example.com' == psl.get_public_suffix('example.com')
        assert 'example.com' == psl.get_public_suffix('b.example.com')
        assert 'example.com' == psl.get_public_suffix('a.b.example.com')
        assert 'uk.com' == psl.get_public_suffix('uk.com')
        assert 'example.uk.com' == psl.get_public_suffix('example.uk.com')
        assert 'example.uk.com' == psl.get_public_suffix('b.example.uk.com')
        assert 'example.uk.com' == psl.get_public_suffix('a.b.example.uk.com')
        assert 'test.ac' == psl.get_public_suffix('test.ac')

        # TLD with only one wildcard rule.
        assert 'er' == psl.get_public_suffix('er')
        assert 'c.er' == psl.get_public_suffix('c.er')
        assert 'b.c.er' == psl.get_public_suffix('b.c.er')
        assert 'b.c.er' == psl.get_public_suffix('a.b.c.er')

        # More complex TLD.
        assert 'jp' == psl.get_public_suffix('jp')
        assert 'test.jp' == psl.get_public_suffix('test.jp')
        assert 'test.jp' == psl.get_public_suffix('www.test.jp')
        assert 'ac.jp' == psl.get_public_suffix('ac.jp')
        assert 'test.ac.jp' == psl.get_public_suffix('test.ac.jp')
        assert 'test.ac.jp' == psl.get_public_suffix('www.test.ac.jp')
        assert 'kobe.jp' == psl.get_public_suffix('kobe.jp')
        assert 'c.kobe.jp' == psl.get_public_suffix('c.kobe.jp')
        assert 'b.c.kobe.jp' == psl.get_public_suffix('b.c.kobe.jp')
        assert 'b.c.kobe.jp' == psl.get_public_suffix('a.b.c.kobe.jp')

        # Exception rule.
        assert 'city.kobe.jp' == psl.get_public_suffix('city.kobe.jp')
        assert 'city.kobe.jp' == psl.get_public_suffix('www.city.kobe.jp')

        # US K12.
        assert 'us' == psl.get_public_suffix('us')
        assert 'test.us' == psl.get_public_suffix('test.us')
        assert 'test.us' == psl.get_public_suffix('www.test.us')
        assert 'ak.us' == psl.get_public_suffix('ak.us')
        assert 'test.ak.us' == psl.get_public_suffix('test.ak.us')
        assert 'test.ak.us' == psl.get_public_suffix('www.test.ak.us')
        assert 'k12.ak.us' == psl.get_public_suffix('k12.ak.us')
        assert 'test.k12.ak.us' == psl.get_public_suffix('test.k12.ak.us')
        assert 'test.k12.ak.us' == psl.get_public_suffix('www.test.k12.ak.us')

        # unicode
        assert u('www.\u9999\u6e2f') == psl.get_public_suffix(u('www.\u9999\u6e2f'))


class TestPublicSuffixLatest(TestPublicSuffixCurrent):
    """Test using the latest list"""
    psl = publicsuffix.fetch()


if __name__ == '__main__':
    unittest.main('tests')
