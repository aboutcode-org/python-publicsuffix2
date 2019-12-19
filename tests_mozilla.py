# -*- coding: utf-8 -*-
# Copyright (c) nexB Inc. and others.
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
# This test suite is borrowed from Mozilla and originally from:
# https://raw.githubusercontent.com/mozilla/gecko-dev/0678172d5b5c681061b904c776b668489e3355b0/netwerk/test/unit/data/test_psl.txt
#     Any copyright is dedicated to the Public Domain.
#     http://creativecommons.org/publicdomain/zero/1.0/


from __future__ import absolute_import
from __future__ import print_function

import sys
import unittest

import publicsuffix2 as publicsuffix

if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


class TestPublicSuffixMozilla(unittest.TestCase):
    """
    Test suite borrowed from Mozilla and originally from:
    https://raw.githubusercontent.com/mozilla/gecko-dev/0678172d5b5c681061b904c776b668489e3355b0/netwerk/test/unit/data/test_psl.txt
        Any copyright is dedicated to the Public Domain.
        http://creativecommons.org/publicdomain/zero/1.0/
    """

    def test_get_tld_null_input(self):
        assert publicsuffix.get_tld(None) == None

    def test_get_tld_Mixed_case(self):
        assert publicsuffix.get_tld('COM') == None

    def test_get_tld_Mixed_case2(self):
        assert publicsuffix.get_tld('example.COM') == 'example.com'

    def test_get_tld_Mixed_case3(self):
        assert publicsuffix.get_tld('WwW.example.COM') == 'example.com'

    def test_get_tld_Leading_dot1(self):
        assert publicsuffix.get_tld('.com') == None

    def test_get_tld_Leading_dot2(self):
        assert None == publicsuffix.get_tld('.example')

    def test_get_tld_Leading_dot3(self):
        assert None == publicsuffix.get_tld('.example.com')

    def test_get_tld_Leading_dot4(self):
        assert None == publicsuffix.get_tld('.example.example')

    def test_get_tld_Unlisted_TLD1(self):
        assert None == publicsuffix.get_tld('example')

    def test_get_tld_Unlisted_TLD2(self):
        assert 'example.example' == publicsuffix.get_tld('example.example')

    def test_get_tld_Unlisted_TLD3(self):
        assert 'example.example' == publicsuffix.get_tld('b.example.example')

    def test_get_tld_Unlisted_TLD4(self):
        assert 'example.example' == publicsuffix.get_tld('a.b.example.example')

    def test_get_tld_Listed_but_non_Internet_TLD1(self):
        assert None == publicsuffix.get_tld('local')

    def test_get_tld_Listed_but_non_Internet_TLD2(self):
        assert None == publicsuffix.get_tld('example.local')

    def test_get_tld_Listed_but_non_Internet_TLD3(self):
        assert None == publicsuffix.get_tld('b.example.local')

    def test_get_tld_Listed_but_non_Internet_TLD4(self):
        assert None == publicsuffix.get_tld('a.b.example.local')

    def test_get_tld_TLD_with_only_1_rule1(self):
        assert None == publicsuffix.get_tld('biz')

    def test_get_tld_TLD_with_only_1_rule2(self):
        assert 'domain.biz' == publicsuffix.get_tld('domain.biz')

    def test_get_tld_TLD_with_only_1_rule3(self):
        assert 'domain.biz' == publicsuffix.get_tld('b.domain.biz')

    def test_get_tld_TLD_with_only_1_rule4(self):
        assert 'domain.biz' == publicsuffix.get_tld('a.b.domain.biz')

    def test_get_tld_TLD_with_some_2_level_rules1(self):
        assert None == publicsuffix.get_tld('com')

    def test_get_tld_TLD_with_some_2_level_rules2(self):
        assert 'example.com' == publicsuffix.get_tld('example.com')

    def test_get_tld_TLD_with_some_2_level_rules3(self):
        assert 'example.com' == publicsuffix.get_tld('b.example.com')

    def test_get_tld_TLD_with_some_2_level_rules4(self):
        assert 'example.com' == publicsuffix.get_tld('a.b.example.com')

    def test_get_tld_TLD_with_some_2_level_rules5(self):
        assert None == publicsuffix.get_tld('uk.com')

    def test_get_tld_TLD_with_some_2_level_rules6(self):
        assert 'example.uk.com' == publicsuffix.get_tld('example.uk.com')

    def test_get_tld_TLD_with_some_2_level_rules7(self):
        assert 'example.uk.com' == publicsuffix.get_tld('b.example.uk.com')

    def test_get_tld_TLD_with_some_2_level_rules8(self):
        assert 'example.uk.com' == publicsuffix.get_tld('a.b.example.uk.com')

    def test_get_tld_TLD_with_some_2_level_rules9(self):
        assert 'test.ac' == publicsuffix.get_tld('test.ac')

    def test_get_tld_TLD_with_only_1_wildcard_rule1(self):
        assert None == publicsuffix.get_tld('bd')

    def test_get_tld_TLD_with_only_1_wildcard_rule2(self):
        assert None == publicsuffix.get_tld('c.bd')

    def test_get_tld_TLD_with_only_1_wildcard_rule3(self):
        assert 'b.c.bd' == publicsuffix.get_tld('b.c.bd')

    def test_get_tld_TLD_with_only_1_wildcard_rule4(self):
        assert 'b.c.bd' == publicsuffix.get_tld('a.b.c.bd')

    def test_get_tld_More_complex_TLD1(self):
        assert None == publicsuffix.get_tld('jp')

    def test_get_tld_More_complex_TLD2(self):
        assert 'test.jp' == publicsuffix.get_tld('test.jp')

    def test_get_tld_More_complex_TLD3(self):
        assert 'test.jp' == publicsuffix.get_tld('www.test.jp')

    def test_get_tld_More_complex_TLD4(self):
        assert None == publicsuffix.get_tld('ac.jp')

    def test_get_tld_More_complex_TLD5(self):
        assert 'test.ac.jp' == publicsuffix.get_tld('test.ac.jp')

    def test_get_tld_More_complex_TLD6(self):
        assert 'test.ac.jp' == publicsuffix.get_tld('www.test.ac.jp')

    def test_get_tld_More_complex_TLD7(self):
        assert None == publicsuffix.get_tld('kyoto.jp')

    def test_get_tld_More_complex_TLD8(self):
        assert 'test.kyoto.jp' == publicsuffix.get_tld('test.kyoto.jp')

    def test_get_tld_More_complex_TLD9(self):
        assert None == publicsuffix.get_tld('ide.kyoto.jp')

    def test_get_tld_More_complex_TLD10(self):
        assert 'b.ide.kyoto.jp' == publicsuffix.get_tld('b.ide.kyoto.jp')

    def test_get_tld_More_complex_TLD11(self):
        assert 'b.ide.kyoto.jp' == publicsuffix.get_tld('a.b.ide.kyoto.jp')

    def test_get_tld_More_complex_TLD12(self):
        assert None == publicsuffix.get_tld('c.kobe.jp')

    def test_get_tld_More_complex_TLD13(self):
        assert 'b.c.kobe.jp' == publicsuffix.get_tld('b.c.kobe.jp')

    def test_get_tld_More_complex_TLD14(self):
        assert 'b.c.kobe.jp' == publicsuffix.get_tld('a.b.c.kobe.jp')

    def test_get_tld_More_complex_TLD15(self):
        assert 'city.kobe.jp' == publicsuffix.get_tld('city.kobe.jp')

    def test_get_tld_More_complex_TLD16(self):
        assert 'city.kobe.jp' == publicsuffix.get_tld('www.city.kobe.jp')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions1(self):
        assert None == publicsuffix.get_tld('ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions2(self):
        assert None == publicsuffix.get_tld('test.ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions3(self):
        assert 'b.test.ck' == publicsuffix.get_tld('b.test.ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions4(self):
        assert 'b.test.ck' == publicsuffix.get_tld('a.b.test.ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions5(self):
        assert 'www.ck' == publicsuffix.get_tld('www.ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions6(self):
        assert 'www.ck' == publicsuffix.get_tld('www.www.ck')

    def test_get_tld_US_K121(self):
        assert None == publicsuffix.get_tld('us')

    def test_get_tld_US_K122(self):
        assert 'test.us' == publicsuffix.get_tld('test.us')

    def test_get_tld_US_K123(self):
        assert 'test.us' == publicsuffix.get_tld('www.test.us')

    def test_get_tld_US_K124(self):
        assert None == publicsuffix.get_tld('ak.us')

    def test_get_tld_US_K125(self):
        assert 'test.ak.us' == publicsuffix.get_tld('test.ak.us')

    def test_get_tld_US_K126(self):
        assert 'test.ak.us' == publicsuffix.get_tld('www.test.ak.us')

    def test_get_tld_US_K127(self):
        assert None == publicsuffix.get_tld('k12.ak.us')

    def test_get_tld_US_K128(self):
        assert 'test.k12.ak.us' == publicsuffix.get_tld('test.k12.ak.us')

    def test_get_tld_US_K129(self):
        assert 'test.k12.ak.us' == publicsuffix.get_tld('www.test.k12.ak.us')

    def test_get_tld_IDN_labels1(self):
        assert '食狮.com.cn' == publicsuffix.get_tld('食狮.com.cn')

    def test_get_tld_IDN_labels2(self):
        assert '食狮.公司.cn' == publicsuffix.get_tld('食狮.公司.cn')

    def test_get_tld_IDN_labels3(self):
        assert '食狮.公司.cn' == publicsuffix.get_tld('www.食狮.公司.cn')

    def test_get_tld_IDN_labels4(self):
        assert 'shishi.公司.cn' == publicsuffix.get_tld('shishi.公司.cn')

    def test_get_tld_IDN_labels5(self):
        assert None == publicsuffix.get_tld('公司.cn')

    def test_get_tld_IDN_labels6(self):
        assert '食狮.中国' == publicsuffix.get_tld('食狮.中国')

    def test_get_tld_IDN_labels7(self):
        assert '食狮.中国' == publicsuffix.get_tld('www.食狮.中国')

    def test_get_tld_IDN_labels8(self):
        assert 'shishi.中国' == publicsuffix.get_tld('shishi.中国')

    def test_get_tld_IDN_labels9(self):
        assert None == publicsuffix.get_tld('中国')

    def test_get_tld_Same_as_above_but_punycoded1(self):
        assert 'xn--85x722f.com.cn' == publicsuffix.get_tld('xn--85x722f.com.cn')

    def test_get_tld_Same_as_above_but_punycoded2(self):
        assert 'xn--85x722f.xn--55qx5d.cn' == publicsuffix.get_tld('xn--85x722f.xn--55qx5d.cn')

    def test_get_tld_Same_as_above_but_punycoded3(self):
        assert 'xn--85x722f.xn--55qx5d.cn' == publicsuffix.get_tld('www.xn--85x722f.xn--55qx5d.cn')

    def test_get_tld_Same_as_above_but_punycoded4(self):
        assert 'shishi.xn--55qx5d.cn' == publicsuffix.get_tld('shishi.xn--55qx5d.cn')

    def test_get_tld_Same_as_above_but_punycoded5(self):
        assert None == publicsuffix.get_tld('xn--55qx5d.cn')

    def test_get_tld_Same_as_above_but_punycoded6(self):
        assert 'xn--85x722f.xn--fiqs8s' == publicsuffix.get_tld('xn--85x722f.xn--fiqs8s')

    def test_get_tld_Same_as_above_but_punycoded7(self):
        assert 'xn--85x722f.xn--fiqs8s' == publicsuffix.get_tld('www.xn--85x722f.xn--fiqs8s')

    def test_get_tld_Same_as_above_but_punycoded8(self):
        assert 'shishi.xn--fiqs8s' == publicsuffix.get_tld('shishi.xn--fiqs8s')

    def test_get_tld_Same_as_above_but_punycoded9(self):
        assert None == publicsuffix.get_tld('xn--fiqs8s')


if __name__ == '__main__':
    unittest.main('tests')
