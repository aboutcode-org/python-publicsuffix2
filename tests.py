# -*- coding: utf-8 -*-
# Copyright (c) nexB Inc. and others.
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
from __future__ import unicode_literals

import unittest

import publicsuffix2 as publicsuffix


class TestPublicSuffix(unittest.TestCase):

    def test_get_sld_from_empty_list(self):
        psl = publicsuffix.PublicSuffixList([])
        assert 'com' == psl.get_sld('com')
        assert 'com' == psl.get_sld('COM')
        assert 'com' == psl.get_sld('.com')
        assert 'com' == psl.get_sld('a.example.com')

    def test_get_sld_from_empty_list_in_strict_mode(self):
        psl = publicsuffix.PublicSuffixList([])
        assert None == psl.get_sld('com', strict=True)

    def test_get_sld_from_list(self):
        psl = publicsuffix.PublicSuffixList(['com'])
        assert 'example.com' == psl.get_sld('a.example.com')
        assert 'example.com' == psl.get_sld('a.a.example.com')
        assert 'example.com' == psl.get_sld('a.a.a.example.com')
        assert 'example.com' == psl.get_sld('A.example.com')
        assert 'example.com' == psl.get_sld('.a.a.example.com')

    def test_get_sld_from_list_with_exception_rule(self):
        psl = publicsuffix.PublicSuffixList(['*.example.com', '!b.example.com'])
        assert 'a.example.com' == psl.get_sld('a.example.com')
        assert 'a.a.example.com' == psl.get_sld('a.a.example.com')
        assert 'a.a.example.com' == psl.get_sld('a.a.a.example.com')
        assert 'a.a.example.com' == psl.get_sld('a.a.a.a.example.com')

        assert 'b.example.com' == psl.get_sld('b.example.com')
        assert 'b.example.com' == psl.get_sld('b.b.example.com')
        assert 'b.example.com' == psl.get_sld('b.b.b.example.com')
        assert 'b.example.com' == psl.get_sld('b.b.b.b.example.com')

    def test_get_sld_from_list_with_fqdn(self):
        psl = publicsuffix.PublicSuffixList(['com'])
        assert 'example.com' == psl.get_sld('example.com.')

    def test_get_sld_from_list_with_unicode(self):
        psl = publicsuffix.PublicSuffixList([u'\u0440\u0444'], idna=False)
        assert u'\u0440\u0444' == psl.get_sld(u'\u0440\u0444')
        assert u'example.\u0440\u0444' == psl.get_sld(u'example.\u0440\u0444')
        assert u'example.\u0440\u0444' == psl.get_sld(u'a.example.\u0440\u0444')
        assert u'example.\u0440\u0444' == psl.get_sld(u'a.a.example.\u0440\u0444')

    def test_get_public_suffix_from_builtin_full_publicsuffix_org_using_top_level_function(self):
        assert 'com' == publicsuffix.get_public_suffix('COM')
        assert 'example.com' == publicsuffix.get_public_suffix('example.COM')
        assert 'example.com' == publicsuffix.get_public_suffix('WwW.example.COM')


class TestPublicSuffixUsingTheCurrentVendoredPSL(unittest.TestCase):

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_mixed_case(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'com' == psl.get_sld('COM')
        assert 'example.com' == psl.get_sld('example.COM')
        assert 'example.com' == psl.get_sld('WwW.example.COM')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_leading_dot(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'com' == psl.get_sld('.com')
        assert 'example' == psl.get_sld('.example')
        assert 'example.com' == psl.get_sld('.example.com')
        assert 'example' == psl.get_sld('.example.example')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_unlisted_tld(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'example' == psl.get_sld('example')
        assert 'example' == psl.get_sld('example.example')
        assert 'example' == psl.get_sld('b.example.example')
        assert 'example' == psl.get_sld('a.b.example.example')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_listed_ut_non_internet_tld(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'local' == psl.get_sld('local')
        assert 'local' == psl.get_sld('example.local')
        assert 'local' == psl.get_sld('b.example.local')
        assert 'local' == psl.get_sld('a.b.example.local')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_one_rule(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'biz' == psl.get_sld('biz')
        assert 'domain.biz' == psl.get_sld('domain.biz')
        assert 'domain.biz' == psl.get_sld('b.domain.biz')
        assert 'domain.biz' == psl.get_sld('a.b.domain.biz')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_two_level_rules(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'com' == psl.get_sld('com')
        assert 'example.com' == psl.get_sld('example.com')
        assert 'example.com' == psl.get_sld('b.example.com')
        assert 'example.com' == psl.get_sld('a.b.example.com')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_two_level_uk_rules(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'uk.com' == psl.get_sld('uk.com')
        assert 'example.uk.com' == psl.get_sld('example.uk.com')
        assert 'example.uk.com' == psl.get_sld('b.example.uk.com')
        assert 'example.uk.com' == psl.get_sld('a.b.example.uk.com')
        assert 'test.ac' == psl.get_sld('test.ac')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_wildcard_rule(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'er' == psl.get_sld('er')
        assert 'c.er' == psl.get_sld('c.er')
        assert 'b.c.er' == psl.get_sld('b.c.er')
        assert 'b.c.er' == psl.get_sld('a.b.c.er')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_japanese_domain(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'jp' == psl.get_sld('jp')
        assert 'test.jp' == psl.get_sld('test.jp')
        assert 'test.jp' == psl.get_sld('www.test.jp')
        assert 'ac.jp' == psl.get_sld('ac.jp')
        assert 'test.ac.jp' == psl.get_sld('test.ac.jp')
        assert 'test.ac.jp' == psl.get_sld('www.test.ac.jp')
        assert 'kobe.jp' == psl.get_sld('kobe.jp')
        assert 'c.kobe.jp' == psl.get_sld('c.kobe.jp')
        assert 'b.c.kobe.jp' == psl.get_sld('b.c.kobe.jp')
        assert 'b.c.kobe.jp' == psl.get_sld('a.b.c.kobe.jp')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_japanese_domain_exception_rule(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'city.kobe.jp' == psl.get_sld('city.kobe.jp')
        assert 'city.kobe.jp' == psl.get_sld('www.city.kobe.jp')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_ys(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'us' == psl.get_sld('us')
        assert 'test.us' == psl.get_sld('test.us')
        assert 'test.us' == psl.get_sld('www.test.us')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_us_k12(self):
        psl = publicsuffix.PublicSuffixList(None)
        assert 'ak.us' == psl.get_sld('ak.us')
        assert 'test.ak.us' == psl.get_sld('test.ak.us')
        assert 'test.ak.us' == psl.get_sld('www.test.ak.us')
        assert 'k12.ak.us' == psl.get_sld('k12.ak.us')
        assert 'test.k12.ak.us' == psl.get_sld('test.k12.ak.us')
        assert 'test.k12.ak.us' == psl.get_sld('www.test.k12.ak.us')


class TestPublicSuffixGetSldIdna(unittest.TestCase):

    def test_get_sld_idna_encoded(self):
        # actually the default
        psl = publicsuffix.PublicSuffixList(idna=True)
        assert 'xn--85x722f.com.cn' == psl.get_sld('xn--85x722f.com.cn')
        assert 'xn--85x722f.xn--55qx5d.cn' == psl.get_sld('xn--85x722f.xn--55qx5d.cn')
        assert 'xn--85x722f.xn--55qx5d.cn' == psl.get_sld('www.xn--85x722f.xn--55qx5d.cn')
        assert 'shishi.xn--55qx5d.cn' == psl.get_sld('shishi.xn--55qx5d.cn')

    def test_get_sld_with_utf8_encoded(self):
        # uses the list provided utf-8 defaults
        psl = publicsuffix.PublicSuffixList(idna=False)
        assert u'食狮.com.cn' == psl.get_sld(u'食狮.com.cn')
        assert u'食狮.公司.cn' == psl.get_sld(u'食狮.公司.cn')
        assert u'食狮.公司.cn' == psl.get_sld(u'www.食狮.公司.cn')
        assert u'shishi.公司.cn' == psl.get_sld(u'shishi.公司.cn')

    def test_get_sld_exceptions(self):
        psl = publicsuffix.PublicSuffixList()
        # www is the exception
        assert 'www.ck' == psl.get_sld('www.www.ck')
        assert 'this.that.ck' == psl.get_sld('this.that.ck')

    def test_get_sld_no_wildcard(self):
        psl = publicsuffix.PublicSuffixList()
        # test completion when no wildcards should be processed
        assert 'com.pg' == psl.get_sld('telinet.com.pg', wildcard=False)
        expected = 'ap-southeast-1.elb.amazonaws.com'
        result = psl.get_sld('blah.ap-southeast-1.elb.amazonaws.com', wildcard=False)
        assert expected == result

    def test_get_sld_top_convenience_function_is_the_same_as_PublicSuffixList_method(self):
        psl = publicsuffix.PublicSuffixList()
        # these functions should be identical
        assert psl.get_sld('www.google.com') == publicsuffix.get_sld('www.google.com')
        assert psl.get_sld('www.test.ak.us') == publicsuffix.get_sld('www.test.ak.us')

    def test_get_tld_returns_correct_tld_or_etld(self):
        psl = publicsuffix.PublicSuffixList()
        assert 'com' == psl.get_tld('com')
        assert 'kobe.jp' == psl.get_tld('city.kobe.jp')
        assert 'kobe.jp' == psl.get_tld('kobe.jp')
        assert 'amazonaws.com' == psl.get_tld('amazonaws.com')
        assert 'com.pg' == psl.get_tld('telinet.com.pg', wildcard=True)
        assert 'pg' == psl.get_tld('telinet.com.pg', wildcard=False)
        assert 'com.pg' == psl.get_tld('com.pg', wildcard=True)
        assert 'pg' == psl.get_tld('com.pg', wildcard=False)
        assert 'co.uk' == psl.get_tld('telinet.co.uk', wildcard=False)
        assert 'co.uk' == psl.get_tld('co.uk', wildcard=True)
        assert 'co.uk' == psl.get_tld('co.uk', wildcard=False)
        assert None == psl.get_tld('blah.local', strict=True)
        assert None == psl.get_tld('blah.local', wildcard=False)
        assert 'local' == psl.get_tld('blah.local')

    def test_get_tld_returns_correct_tld_or_etld_for_fqdn(self):
        psl = publicsuffix.PublicSuffixList()
        assert 'com' == psl.get_tld('www.foo.com.')

    def test_get_tld_returns_correct_tld_or_etld_for_root_domain(self):
        psl = publicsuffix.PublicSuffixList()
        assert '' == psl.get_tld('.')

    def test_get_tld_returns_correct_tld_or_etld_for_empty_string(self):
        psl = publicsuffix.PublicSuffixList()
        assert None == psl.get_tld('')

    def test_PublicSuffixList_tlds_is_loaded_correctly(self):
        psl = publicsuffix.PublicSuffixList()
        assert psl.tlds


class TestPublicSuffixGetSld(unittest.TestCase):

    def test_get_sld_backward_compatibility(self):
        psl = publicsuffix.PublicSuffixList()
        assert 'com' == psl.get_sld('com')
        assert 'foo.com' == psl.get_sld('foo.com')
        assert 'foo.co.jp' == psl.get_sld('foo.co.jp')
        assert 'co.jp' == psl.get_sld('co.jp')
        assert 'jp' == psl.get_sld('jp')

    def test_get_sld_backward_compatibility_strict_and_wildcard_flags(self):
        psl = publicsuffix.PublicSuffixList()
        assert 'local' == psl.get_sld('local')
        assert 'local' == psl.get_sld('foo.local')
        assert None == psl.get_sld('local', strict=True)
        assert None == psl.get_sld('foo.local', strict=True)
        assert 'local' == psl.get_sld('local', wildcard=False)
        assert 'local' == psl.get_sld('foo.local', strict=False)

    def test_get_sld_backward_compatibility_sld_for_empty_string(self):
        psl = publicsuffix.PublicSuffixList()
        assert None == psl.get_sld('')
        assert None == psl.get_sld('', strict=True)
        assert None == psl.get_sld('', wildcard=False)

    def test_get_sld_backward_compatibility_sld_for_fqdn(self):
        psl = publicsuffix.PublicSuffixList()
        assert 'foo.com' == psl.get_sld('www.foo.com.')

    def test_get_sld_backward_compatibility_sld_for_root_domain(self):
        psl = publicsuffix.PublicSuffixList()
        assert '' == psl.get_sld('.')
        assert None == psl.get_sld('.', strict=True)
        assert '' == psl.get_sld('.', wildcard=False)


if __name__ == '__main__':
    unittest.main('tests')
