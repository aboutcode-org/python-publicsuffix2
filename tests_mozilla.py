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
from __future__ import unicode_literals

import unittest

import publicsuffix2 as publicsuffix


class TestPublicSuffixMozilla(unittest.TestCase):
    """
    Test suite borrowed from Mozilla and originally from:
    https://raw.githubusercontent.com/mozilla/gecko-dev/0678172d5b5c681061b904c776b668489e3355b0/netwerk/test/unit/data/test_psl.txt
        Any copyright is dedicated to the Public Domain.
        http://creativecommons.org/publicdomain/zero/1.0/
    """

    def test_get_tld_null_input(self):
        assert None == publicsuffix.get_tld(None)

    def test_get_tld_Mixed_case(self):
        assert 'com' == publicsuffix.get_tld('COM')

    def test_get_tld_Mixed_case2(self):
        assert 'com' == publicsuffix.get_tld('example.COM')

    def test_get_tld_Mixed_case3(self):
        assert 'com' == publicsuffix.get_tld('WwW.example.COM')

    def test_get_tld_Leading_dot1(self):
        assert 'com' == publicsuffix.get_tld('.com')

    def test_get_tld_Leading_dot2(self):
        assert 'example' == publicsuffix.get_tld('.example')

    def test_get_tld_Leading_dot3(self):
        assert 'com' == publicsuffix.get_tld('.example.com')

    def test_get_tld_Leading_dot4(self):
        assert 'example' == publicsuffix.get_tld('.example.example')

    def test_get_tld_Unlisted_TLD1(self):
        assert 'example' == publicsuffix.get_tld('example')

    def test_get_tld_Unlisted_TLD2(self):
        assert 'example' == publicsuffix.get_tld('example.example')

    def test_get_tld_Unlisted_TLD3(self):
        assert 'example' == publicsuffix.get_tld('b.example.example')

    def test_get_tld_Unlisted_TLD4(self):
        assert 'example' == publicsuffix.get_tld('a.b.example.example')

    def test_get_tld_Listed_but_non_Internet_TLD1(self):
        assert 'local' == publicsuffix.get_tld('local')

    def test_get_tld_Listed_but_non_Internet_TLD2(self):
        assert 'local' == publicsuffix.get_tld('example.local')

    def test_get_tld_Listed_but_non_Internet_TLD3(self):
        assert 'local' == publicsuffix.get_tld('b.example.local')

    def test_get_tld_Listed_but_non_Internet_TLD4(self):
        assert 'local' == publicsuffix.get_tld('a.b.example.local')

    def test_get_tld_TLD_with_only_1_rule1(self):
        assert 'biz' == publicsuffix.get_tld('biz')

    def test_get_tld_TLD_with_only_1_rule2(self):
        assert 'biz' == publicsuffix.get_tld('domain.biz')

    def test_get_tld_TLD_with_only_1_rule3(self):
        assert 'biz' == publicsuffix.get_tld('b.domain.biz')

    def test_get_tld_TLD_with_only_1_rule4(self):
        assert 'biz' == publicsuffix.get_tld('a.b.domain.biz')

    def test_get_tld_TLD_with_some_2_level_rules1(self):
        assert 'com' == publicsuffix.get_tld('com')

    def test_get_tld_TLD_with_some_2_level_rules2(self):
        assert 'com' == publicsuffix.get_tld('example.com')

    def test_get_tld_TLD_with_some_2_level_rules3(self):
        assert 'com' == publicsuffix.get_tld('b.example.com')

    def test_get_tld_TLD_with_some_2_level_rules4(self):
        assert 'com' == publicsuffix.get_tld('a.b.example.com')

    def test_get_tld_TLD_with_some_2_level_rules5(self):
        assert 'uk.com' == publicsuffix.get_tld('uk.com')

    def test_get_tld_TLD_with_some_2_level_rules6(self):
        assert 'uk.com' == publicsuffix.get_tld('example.uk.com')

    def test_get_tld_TLD_with_some_2_level_rules7(self):
        assert 'uk.com' == publicsuffix.get_tld('b.example.uk.com')

    def test_get_tld_TLD_with_some_2_level_rules8(self):
        assert 'uk.com' == publicsuffix.get_tld('a.b.example.uk.com')

    def test_get_tld_TLD_with_some_2_level_rules9(self):
        assert 'ac' == publicsuffix.get_tld('test.ac')

    def test_get_tld_TLD_with_only_1_wildcard_rule1(self):
        assert 'bd' == publicsuffix.get_tld('bd')

    def test_get_tld_TLD_with_only_1_wildcard_rule2(self):
        assert 'c.bd' == publicsuffix.get_tld('c.bd')

    def test_get_tld_TLD_with_only_1_wildcard_rule3(self):
        assert 'c.bd' == publicsuffix.get_tld('b.c.bd')

    def test_get_tld_TLD_with_only_1_wildcard_rule4(self):
        assert 'c.bd' == publicsuffix.get_tld('a.b.c.bd')

    def test_get_tld_More_complex_TLD1(self):
        assert 'jp' == publicsuffix.get_tld('jp')

    def test_get_tld_More_complex_TLD2(self):
        assert 'jp' == publicsuffix.get_tld('test.jp')

    def test_get_tld_More_complex_TLD3(self):
        assert 'jp' == publicsuffix.get_tld('www.test.jp')

    def test_get_tld_More_complex_TLD4(self):
        assert 'ac.jp' == publicsuffix.get_tld('ac.jp')

    def test_get_tld_More_complex_TLD5(self):
        assert 'ac.jp' == publicsuffix.get_tld('test.ac.jp')

    def test_get_tld_More_complex_TLD6(self):
        assert 'ac.jp' == publicsuffix.get_tld('www.test.ac.jp')

    def test_get_tld_More_complex_TLD7(self):
        assert 'kyoto.jp' == publicsuffix.get_tld('kyoto.jp')

    def test_get_tld_More_complex_TLD8(self):
        assert 'kyoto.jp' == publicsuffix.get_tld('test.kyoto.jp')

    def test_get_tld_More_complex_TLD9(self):
        assert 'ide.kyoto.jp' == publicsuffix.get_tld('ide.kyoto.jp')

    def test_get_tld_More_complex_TLD10(self):
        assert 'ide.kyoto.jp' == publicsuffix.get_tld('b.ide.kyoto.jp')

    def test_get_tld_More_complex_TLD11(self):
        assert 'ide.kyoto.jp' == publicsuffix.get_tld('a.b.ide.kyoto.jp')

    def test_get_tld_More_complex_TLD12(self):
        assert 'c.kobe.jp' == publicsuffix.get_tld('c.kobe.jp')

    def test_get_tld_More_complex_TLD13(self):
        assert 'c.kobe.jp' == publicsuffix.get_tld('b.c.kobe.jp')

    def test_get_tld_More_complex_TLD14(self):
        assert 'c.kobe.jp' == publicsuffix.get_tld('a.b.c.kobe.jp')

    def test_get_tld_More_complex_TLD15(self):
        assert 'kobe.jp' == publicsuffix.get_tld('city.kobe.jp')

    def test_get_tld_More_complex_TLD16(self):
        assert 'kobe.jp' == publicsuffix.get_tld('www.city.kobe.jp')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions1(self):
        assert 'ck' == publicsuffix.get_tld('ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions2(self):
        assert 'test.ck' == publicsuffix.get_tld('test.ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions3(self):
        assert 'test.ck' == publicsuffix.get_tld('b.test.ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions4(self):
        assert 'test.ck' == publicsuffix.get_tld('a.b.test.ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions5(self):
        assert 'ck' == publicsuffix.get_tld('www.ck')

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions6(self):
        assert 'ck' == publicsuffix.get_tld('www.www.ck')

    def test_get_tld_US_K121(self):
        assert 'us' == publicsuffix.get_tld('us')

    def test_get_tld_US_K122(self):
        assert 'us' == publicsuffix.get_tld('test.us')

    def test_get_tld_US_K123(self):
        assert 'us' == publicsuffix.get_tld('www.test.us')

    def test_get_tld_US_K124(self):
        assert 'ak.us' == publicsuffix.get_tld('ak.us')

    def test_get_tld_US_K125(self):
        assert 'ak.us' == publicsuffix.get_tld('test.ak.us')

    def test_get_tld_US_K126(self):
        assert 'ak.us' == publicsuffix.get_tld('www.test.ak.us')

    def test_get_tld_US_K127(self):
        assert 'k12.ak.us' == publicsuffix.get_tld('k12.ak.us')

    def test_get_tld_US_K128(self):
        assert 'k12.ak.us' == publicsuffix.get_tld('test.k12.ak.us')

    def test_get_tld_US_K129(self):
        assert 'k12.ak.us' == publicsuffix.get_tld('www.test.k12.ak.us')

    def test_get_tld_IDN_labels1(self):
        assert 'com.cn' == publicsuffix.get_tld('食狮.com.cn')

    def test_get_tld_IDN_labels2(self):
        assert 'cn' == publicsuffix.get_tld('食狮.公司.cn')

    def test_get_tld_IDN_labels3(self):
        assert 'cn' == publicsuffix.get_tld('www.食狮.公司.cn')

    def test_get_tld_IDN_labels4(self):
        assert 'cn' == publicsuffix.get_tld('shishi.公司.cn')

    def test_get_tld_IDN_labels5(self):
        assert 'cn' == publicsuffix.get_tld('公司.cn')

    def test_get_tld_IDN_labels6(self):
        assert '中国' == publicsuffix.get_tld('食狮.中国')

    def test_get_tld_IDN_labels7(self):
        assert '中国' == publicsuffix.get_tld('www.食狮.中国')

    def test_get_tld_IDN_labels8(self):
        assert '中国' == publicsuffix.get_tld('shishi.中国')

    def test_get_tld_IDN_labels9(self):
        assert '中国' == publicsuffix.get_tld('中国')

    def test_get_tld_Same_as_above_but_punycoded1(self):
        assert 'com.cn' == publicsuffix.get_tld('xn--85x722f.com.cn')

    def test_get_tld_Same_as_above_but_punycoded2(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_tld('xn--85x722f.xn--55qx5d.cn')

    def test_get_tld_Same_as_above_but_punycoded3(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_tld('www.xn--85x722f.xn--55qx5d.cn')

    def test_get_tld_Same_as_above_but_punycoded4(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_tld('shishi.xn--55qx5d.cn')

    def test_get_tld_Same_as_above_but_punycoded5(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_tld('xn--55qx5d.cn')

    def test_get_tld_Same_as_above_but_punycoded6(self):
        assert 'xn--fiqs8s' == publicsuffix.get_tld('xn--85x722f.xn--fiqs8s')

    def test_get_tld_Same_as_above_but_punycoded7(self):
        assert 'xn--fiqs8s' == publicsuffix.get_tld('www.xn--85x722f.xn--fiqs8s')

    def test_get_tld_Same_as_above_but_punycoded8(self):
        assert 'xn--fiqs8s' == publicsuffix.get_tld('shishi.xn--fiqs8s')

    def test_get_tld_Same_as_above_but_punycoded9(self):
        assert 'xn--fiqs8s' == publicsuffix.get_tld('xn--fiqs8s')


class TestPublicSuffixMozillaStrict(unittest.TestCase):
    """
    Test suite borrowed from Mozilla and originally from:
    https://raw.githubusercontent.com/mozilla/gecko-dev/0678172d5b5c681061b904c776b668489e3355b0/netwerk/test/unit/data/test_psl.txt
        Any copyright is dedicated to the Public Domain.
        http://creativecommons.org/publicdomain/zero/1.0/
    """

    def test_get_tld_null_input(self):
        assert None == publicsuffix.get_tld(None, strict=True)

    def test_get_tld_Mixed_case(self):
        assert 'com' == publicsuffix.get_tld('COM', strict=True)

    def test_get_tld_Mixed_case2(self):
        assert 'com' == publicsuffix.get_tld('example.COM', strict=True)

    def test_get_tld_Mixed_case3(self):
        assert 'com' == publicsuffix.get_tld('WwW.example.COM', strict=True)

    def test_get_tld_Leading_dot1(self):
        assert 'com' == publicsuffix.get_tld('.com', strict=True)

    def test_get_tld_Leading_dot2(self):
        assert None == publicsuffix.get_tld('.example', strict=True)

    def test_get_tld_Leading_dot3(self):
        assert 'com' == publicsuffix.get_tld('.example.com', strict=True)

    def test_get_tld_Leading_dot4(self):
        assert None == publicsuffix.get_tld('.example.example', strict=True)

    def test_get_tld_Unlisted_TLD1(self):
        assert None == publicsuffix.get_tld('example', strict=True)

    def test_get_tld_Unlisted_TLD2(self):
        assert None == publicsuffix.get_tld('example.example', strict=True)

    def test_get_tld_Unlisted_TLD3(self):
        assert None == publicsuffix.get_tld('b.example.example', strict=True)

    def test_get_tld_Unlisted_TLD4(self):
        assert None == publicsuffix.get_tld('a.b.example.example', strict=True)

    def test_get_tld_Listed_but_non_Internet_TLD1(self):
        assert None == publicsuffix.get_tld('local', strict=True)

    def test_get_tld_Listed_but_non_Internet_TLD2(self):
        assert None == publicsuffix.get_tld('example.local', strict=True)

    def test_get_tld_Listed_but_non_Internet_TLD3(self):
        assert None == publicsuffix.get_tld('b.example.local', strict=True)

    def test_get_tld_Listed_but_non_Internet_TLD4(self):
        assert None == publicsuffix.get_tld('a.b.example.local', strict=True)

    def test_get_tld_TLD_with_only_1_rule1(self):
        assert 'biz' == publicsuffix.get_tld('biz', strict=True)

    def test_get_tld_TLD_with_only_1_rule2(self):
        assert 'biz' == publicsuffix.get_tld('domain.biz', strict=True)

    def test_get_tld_TLD_with_only_1_rule3(self):
        assert 'biz' == publicsuffix.get_tld('b.domain.biz', strict=True)

    def test_get_tld_TLD_with_only_1_rule4(self):
        assert 'biz' == publicsuffix.get_tld('a.b.domain.biz', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules1(self):
        assert 'com' == publicsuffix.get_tld('com', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules2(self):
        assert 'com' == publicsuffix.get_tld('example.com', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules3(self):
        assert 'com' == publicsuffix.get_tld('b.example.com', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules4(self):
        assert 'com' == publicsuffix.get_tld('a.b.example.com', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules5(self):
        assert 'uk.com' == publicsuffix.get_tld('uk.com', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules6(self):
        assert 'uk.com' == publicsuffix.get_tld('example.uk.com', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules7(self):
        assert 'uk.com' == publicsuffix.get_tld('b.example.uk.com', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules8(self):
        assert 'uk.com' == publicsuffix.get_tld('a.b.example.uk.com', strict=True)

    def test_get_tld_TLD_with_some_2_level_rules9(self):
        assert 'ac' == publicsuffix.get_tld('test.ac', strict=True)

    def test_get_tld_TLD_with_only_1_wildcard_rule1(self):
        assert 'bd' == publicsuffix.get_tld('bd', strict=True)

    def test_get_tld_TLD_with_only_1_wildcard_rule2(self):
        assert 'c.bd' == publicsuffix.get_tld('c.bd', strict=True)

    def test_get_tld_TLD_with_only_1_wildcard_rule3(self):
        assert 'c.bd' == publicsuffix.get_tld('b.c.bd', strict=True)

    def test_get_tld_TLD_with_only_1_wildcard_rule4(self):
        assert 'c.bd' == publicsuffix.get_tld('a.b.c.bd', strict=True)

    def test_get_tld_More_complex_TLD1(self):
        assert 'jp' == publicsuffix.get_tld('jp', strict=True)

    def test_get_tld_More_complex_TLD2(self):
        assert 'jp' == publicsuffix.get_tld('test.jp', strict=True)

    def test_get_tld_More_complex_TLD3(self):
        assert 'jp' == publicsuffix.get_tld('www.test.jp', strict=True)

    def test_get_tld_More_complex_TLD4(self):
        assert 'ac.jp' == publicsuffix.get_tld('ac.jp', strict=True)

    def test_get_tld_More_complex_TLD5(self):
        assert 'ac.jp' == publicsuffix.get_tld('test.ac.jp', strict=True)

    def test_get_tld_More_complex_TLD6(self):
        assert 'ac.jp' == publicsuffix.get_tld('www.test.ac.jp', strict=True)

    def test_get_tld_More_complex_TLD7(self):
        assert 'kyoto.jp' == publicsuffix.get_tld('kyoto.jp', strict=True)

    def test_get_tld_More_complex_TLD8(self):
        assert 'kyoto.jp' == publicsuffix.get_tld('test.kyoto.jp', strict=True)

    def test_get_tld_More_complex_TLD9(self):
        assert 'ide.kyoto.jp' == publicsuffix.get_tld('ide.kyoto.jp', strict=True)

    def test_get_tld_More_complex_TLD10(self):
        assert 'ide.kyoto.jp' == publicsuffix.get_tld('b.ide.kyoto.jp', strict=True)

    def test_get_tld_More_complex_TLD11(self):
        assert 'ide.kyoto.jp' == publicsuffix.get_tld('a.b.ide.kyoto.jp', strict=True)

    def test_get_tld_More_complex_TLD12(self):
        assert 'c.kobe.jp' == publicsuffix.get_tld('c.kobe.jp', strict=True)

    def test_get_tld_More_complex_TLD13(self):
        assert 'c.kobe.jp' == publicsuffix.get_tld('b.c.kobe.jp', strict=True)

    def test_get_tld_More_complex_TLD14(self):
        assert 'c.kobe.jp' == publicsuffix.get_tld('a.b.c.kobe.jp', strict=True)

    def test_get_tld_More_complex_TLD15(self):
        assert 'kobe.jp' == publicsuffix.get_tld('city.kobe.jp', strict=True)

    def test_get_tld_More_complex_TLD16(self):
        assert 'kobe.jp' == publicsuffix.get_tld('www.city.kobe.jp', strict=True)

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions1(self):
        assert 'ck' == publicsuffix.get_tld('ck', strict=True)

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions2(self):
        assert 'test.ck' == publicsuffix.get_tld('test.ck', strict=True)

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions3(self):
        assert 'test.ck' == publicsuffix.get_tld('b.test.ck', strict=True)

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions4(self):
        assert 'test.ck' == publicsuffix.get_tld('a.b.test.ck', strict=True)

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions5(self):
        assert 'ck' == publicsuffix.get_tld('www.ck', strict=True)

    def test_get_tld_TLD_with_a_wildcard_rule_and_exceptions6(self):
        assert 'ck' == publicsuffix.get_tld('www.www.ck', strict=True)

    def test_get_tld_US_K121(self):
        assert 'us' == publicsuffix.get_tld('us', strict=True)

    def test_get_tld_US_K122(self):
        assert 'us' == publicsuffix.get_tld('test.us', strict=True)

    def test_get_tld_US_K123(self):
        assert 'us' == publicsuffix.get_tld('www.test.us', strict=True)

    def test_get_tld_US_K124(self):
        assert 'ak.us' == publicsuffix.get_tld('ak.us', strict=True)

    def test_get_tld_US_K125(self):
        assert 'ak.us' == publicsuffix.get_tld('test.ak.us', strict=True)

    def test_get_tld_US_K126(self):
        assert 'ak.us' == publicsuffix.get_tld('www.test.ak.us', strict=True)

    def test_get_tld_US_K127(self):
        assert 'k12.ak.us' == publicsuffix.get_tld('k12.ak.us', strict=True)

    def test_get_tld_US_K128(self):
        assert 'k12.ak.us' == publicsuffix.get_tld('test.k12.ak.us', strict=True)

    def test_get_tld_US_K129(self):
        assert 'k12.ak.us' == publicsuffix.get_tld('www.test.k12.ak.us', strict=True)

    def test_get_tld_IDN_labels1(self):
        assert 'com.cn' == publicsuffix.get_tld('食狮.com.cn', strict=True)

    def test_get_tld_IDN_labels2(self):
        assert 'cn' == publicsuffix.get_tld('食狮.公司.cn', strict=True)

    def test_get_tld_IDN_labels3(self):
        assert 'cn' == publicsuffix.get_tld('www.食狮.公司.cn', strict=True)

    def test_get_tld_IDN_labels4(self):
        assert 'cn' == publicsuffix.get_tld('shishi.公司.cn', strict=True)

    def test_get_tld_IDN_labels5(self):
        assert 'cn' == publicsuffix.get_tld('公司.cn', strict=True)

    def test_get_tld_IDN_labels6(self):
        assert None == publicsuffix.get_tld('食狮.中国', strict=True)

    def test_get_tld_IDN_labels7(self):
        assert None == publicsuffix.get_tld('www.食狮.中国', strict=True)

    def test_get_tld_IDN_labels8(self):
        assert None == publicsuffix.get_tld('shishi.中国', strict=True)

    def test_get_tld_IDN_labels9(self):
        assert None == publicsuffix.get_tld('中国', strict=True)

    def test_get_tld_Same_as_above_but_punycoded1(self):
        assert 'com.cn' == publicsuffix.get_tld('xn--85x722f.com.cn', strict=True)

    def test_get_tld_Same_as_above_but_punycoded2(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_tld('xn--85x722f.xn--55qx5d.cn', strict=True)

    def test_get_tld_Same_as_above_but_punycoded3(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_tld('www.xn--85x722f.xn--55qx5d.cn', strict=True)

    def test_get_tld_Same_as_above_but_punycoded4(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_tld('shishi.xn--55qx5d.cn', strict=True)

    def test_get_tld_Same_as_above_but_punycoded5(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_tld('xn--55qx5d.cn', strict=True)

    def test_get_tld_Same_as_above_but_punycoded6(self):
        assert 'xn--fiqs8s' == publicsuffix.get_tld('xn--85x722f.xn--fiqs8s', strict=True)

    def test_get_tld_Same_as_above_but_punycoded7(self):
        assert 'xn--fiqs8s' == publicsuffix.get_tld('www.xn--85x722f.xn--fiqs8s', strict=True)

    def test_get_tld_Same_as_above_but_punycoded8(self):
        assert 'xn--fiqs8s' == publicsuffix.get_tld('shishi.xn--fiqs8s', strict=True)

    def test_get_tld_Same_as_above_but_punycoded9(self):
        assert 'xn--fiqs8s' == publicsuffix.get_tld('xn--fiqs8s', strict=True)


class TestPublicSuffixMozillaSld(unittest.TestCase):
    """
    Test suite borrowed from Mozilla and originally from:
    https://raw.githubusercontent.com/mozilla/gecko-dev/0678172d5b5c681061b904c776b668489e3355b0/netwerk/test/unit/data/test_psl.txt
        Any copyright is dedicated to the Public Domain.
        http://creativecommons.org/publicdomain/zero/1.0/
    """

    def test_get_sld_null_input(self):
        assert None == publicsuffix.get_sld(None)

    def test_get_sld_Mixed_case(self):
        assert 'com' == publicsuffix.get_sld('COM')

    def test_get_sld_Mixed_case2(self):
        assert 'example.com' == publicsuffix.get_sld('example.COM')

    def test_get_sld_Mixed_case3(self):
        assert 'example.com' == publicsuffix.get_sld('WwW.example.COM')

    def test_get_sld_Leading_dot1(self):
        assert 'com' == publicsuffix.get_sld('.com')

    def test_get_sld_Leading_dot2(self):
        assert 'example' == publicsuffix.get_sld('.example')

    def test_get_sld_Leading_dot3(self):
        assert 'example.com' == publicsuffix.get_sld('.example.com')

    def test_get_sld_Leading_dot4(self):
        assert 'example' == publicsuffix.get_sld('.example.example')

    def test_get_sld_Unlisted_sld1(self):
        assert 'example' == publicsuffix.get_sld('example')

    def test_get_sld_Unlisted_sld2(self):
        assert 'example' == publicsuffix.get_sld('example.example')

    def test_get_sld_Unlisted_sld3(self):
        assert 'example' == publicsuffix.get_sld('b.example.example')

    def test_get_sld_Unlisted_sld4(self):
        assert 'example' == publicsuffix.get_sld('a.b.example.example')

    def test_get_sld_Listed_but_non_Internet_sld1(self):
        assert 'local' == publicsuffix.get_sld('local')

    def test_get_sld_Listed_but_non_Internet_sld2(self):
        assert 'local' == publicsuffix.get_sld('example.local')

    def test_get_sld_Listed_but_non_Internet_sld3(self):
        assert 'local' == publicsuffix.get_sld('b.example.local')

    def test_get_sld_Listed_but_non_Internet_sld4(self):
        assert 'local' == publicsuffix.get_sld('a.b.example.local')

    def test_get_sld_tld_with_only_1_rule1(self):
        assert 'biz' == publicsuffix.get_sld('biz')

    def test_get_sld_tld_with_only_1_rule2(self):
        assert 'domain.biz' == publicsuffix.get_sld('domain.biz')

    def test_get_sld_tld_with_only_1_rule3(self):
        assert 'domain.biz' == publicsuffix.get_sld('b.domain.biz')

    def test_get_sld_tld_with_only_1_rule4(self):
        assert 'domain.biz' == publicsuffix.get_sld('a.b.domain.biz')

    def test_get_sld_tld_with_some_2_level_rules1(self):
        assert 'com' == publicsuffix.get_sld('com')

    def test_get_sld_tld_with_some_2_level_rules2(self):
        assert 'example.com' == publicsuffix.get_sld('example.com')

    def test_get_sld_tld_with_some_2_level_rules3(self):
        assert 'example.com' == publicsuffix.get_sld('b.example.com')

    def test_get_sld_tld_with_some_2_level_rules4(self):
        assert 'example.com' == publicsuffix.get_sld('a.b.example.com')

    def test_get_sld_tld_with_some_2_level_rules5(self):
        assert 'uk.com' == publicsuffix.get_sld('uk.com')

    def test_get_sld_tld_with_some_2_level_rules6(self):
        assert 'example.uk.com' == publicsuffix.get_sld('example.uk.com')

    def test_get_sld_tld_with_some_2_level_rules7(self):
        assert 'example.uk.com' == publicsuffix.get_sld('b.example.uk.com')

    def test_get_sld_tld_with_some_2_level_rules8(self):
        assert 'example.uk.com' == publicsuffix.get_sld('a.b.example.uk.com')

    def test_get_sld_tld_with_some_2_level_rules9(self):
        assert 'test.ac' == publicsuffix.get_sld('test.ac')

    def test_get_sld_tld_with_only_1_wildcard_rule1(self):
        assert 'bd' == publicsuffix.get_sld('bd')

    def test_get_sld_tld_with_only_1_wildcard_rule2(self):
        assert 'c.bd' == publicsuffix.get_sld('c.bd')

    def test_get_sld_tld_with_only_1_wildcard_rule3(self):
        assert 'b.c.bd' == publicsuffix.get_sld('b.c.bd')

    def test_get_sld_tld_with_only_1_wildcard_rule4(self):
        assert 'b.c.bd' == publicsuffix.get_sld('a.b.c.bd')

    def test_get_sld_More_complex_sld1(self):
        assert 'jp' == publicsuffix.get_sld('jp')

    def test_get_sld_More_complex_sld2(self):
        assert 'test.jp' == publicsuffix.get_sld('test.jp')

    def test_get_sld_More_complex_sld3(self):
        assert 'test.jp' == publicsuffix.get_sld('www.test.jp')

    def test_get_sld_More_complex_sld4(self):
        assert 'ac.jp' == publicsuffix.get_sld('ac.jp')

    def test_get_sld_More_complex_sld5(self):
        assert 'test.ac.jp' == publicsuffix.get_sld('test.ac.jp')

    def test_get_sld_More_complex_sld6(self):
        assert 'test.ac.jp' == publicsuffix.get_sld('www.test.ac.jp')

    def test_get_sld_More_complex_sld7(self):
        assert 'kyoto.jp' == publicsuffix.get_sld('kyoto.jp')

    def test_get_sld_More_complex_sld8(self):
        assert 'test.kyoto.jp' == publicsuffix.get_sld('test.kyoto.jp')

    def test_get_sld_More_complex_sld9(self):
        assert 'ide.kyoto.jp' == publicsuffix.get_sld('ide.kyoto.jp')

    def test_get_sld_More_complex_sld10(self):
        assert 'b.ide.kyoto.jp' == publicsuffix.get_sld('b.ide.kyoto.jp')

    def test_get_sld_More_complex_sld11(self):
        assert 'b.ide.kyoto.jp' == publicsuffix.get_sld('a.b.ide.kyoto.jp')

    def test_get_sld_More_complex_sld12(self):
        assert 'c.kobe.jp' == publicsuffix.get_sld('c.kobe.jp')

    def test_get_sld_More_complex_sld13(self):
        assert 'b.c.kobe.jp' == publicsuffix.get_sld('b.c.kobe.jp')

    def test_get_sld_More_complex_sld14(self):
        assert 'b.c.kobe.jp' == publicsuffix.get_sld('a.b.c.kobe.jp')

    def test_get_sld_More_complex_sld15(self):
        assert 'city.kobe.jp' == publicsuffix.get_sld('city.kobe.jp')

    def test_get_sld_More_complex_sld16(self):
        assert 'city.kobe.jp' == publicsuffix.get_sld('www.city.kobe.jp')

    def test_get_sld_tld_with_a_wildcard_rule_and_exceptions1(self):
        assert 'ck' == publicsuffix.get_sld('ck')

    def test_get_sld_tld_with_a_wildcard_rule_and_exceptions2(self):
        assert 'test.ck' == publicsuffix.get_sld('test.ck')

    def test_get_sld_tld_with_a_wildcard_rule_and_exceptions3(self):
        assert 'b.test.ck' == publicsuffix.get_sld('b.test.ck')

    def test_get_sld_tld_with_a_wildcard_rule_and_exceptions4(self):
        assert 'b.test.ck' == publicsuffix.get_sld('a.b.test.ck')

    def test_get_sld_tld_with_a_wildcard_rule_and_exceptions5(self):
        assert 'www.ck' == publicsuffix.get_sld('www.ck')

    def test_get_sld_tld_with_a_wildcard_rule_and_exceptions6(self):
        assert 'www.ck' == publicsuffix.get_sld('www.www.ck')

    def test_get_sld_US_K121(self):
        assert 'us' == publicsuffix.get_sld('us')

    def test_get_sld_US_K122(self):
        assert 'test.us' == publicsuffix.get_sld('test.us')

    def test_get_sld_US_K123(self):
        assert 'test.us' == publicsuffix.get_sld('www.test.us')

    def test_get_sld_US_K124(self):
        assert 'ak.us' == publicsuffix.get_sld('ak.us')

    def test_get_sld_US_K125(self):
        assert 'test.ak.us' == publicsuffix.get_sld('test.ak.us')

    def test_get_sld_US_K126(self):
        assert 'test.ak.us' == publicsuffix.get_sld('www.test.ak.us')

    def test_get_sld_US_K127(self):
        assert 'k12.ak.us' == publicsuffix.get_sld('k12.ak.us')

    def test_get_sld_US_K128(self):
        assert 'test.k12.ak.us' == publicsuffix.get_sld('test.k12.ak.us')

    def test_get_sld_US_K129(self):
        assert 'test.k12.ak.us' == publicsuffix.get_sld('www.test.k12.ak.us')

    def test_get_sld_IDN_labels1(self):
        assert '食狮.com.cn' == publicsuffix.get_sld('食狮.com.cn')

    def test_get_sld_IDN_labels2(self):
        assert '公司.cn' == publicsuffix.get_sld('食狮.公司.cn')

    def test_get_sld_IDN_labels3(self):
        assert '公司.cn' == publicsuffix.get_sld('www.食狮.公司.cn')

    def test_get_sld_IDN_labels4(self):
        assert '公司.cn' == publicsuffix.get_sld('shishi.公司.cn')

    def test_get_sld_IDN_labels5(self):
        assert '公司.cn' == publicsuffix.get_sld('公司.cn')

    def test_get_sld_IDN_labels6(self):
        assert '中国' == publicsuffix.get_sld('食狮.中国')

    def test_get_sld_IDN_labels7(self):
        assert '中国' == publicsuffix.get_sld('www.食狮.中国')

    def test_get_sld_IDN_labels8(self):
        assert '中国' == publicsuffix.get_sld('shishi.中国')

    def test_get_sld_IDN_labels9(self):
        assert '中国' == publicsuffix.get_sld('中国')

    def test_get_sld_Same_as_above_but_punycoded1(self):
        assert 'xn--85x722f.com.cn' == publicsuffix.get_sld('xn--85x722f.com.cn')

    def test_get_sld_Same_as_above_but_punycoded2(self):
        assert 'xn--85x722f.xn--55qx5d.cn' == publicsuffix.get_sld('xn--85x722f.xn--55qx5d.cn')

    def test_get_sld_Same_as_above_but_punycoded3(self):
        assert 'xn--85x722f.xn--55qx5d.cn' == publicsuffix.get_sld('www.xn--85x722f.xn--55qx5d.cn')

    def test_get_sld_Same_as_above_but_punycoded4(self):
        assert 'shishi.xn--55qx5d.cn' == publicsuffix.get_sld('shishi.xn--55qx5d.cn')

    def test_get_sld_Same_as_above_but_punycoded5(self):
        assert 'xn--55qx5d.cn' == publicsuffix.get_sld('xn--55qx5d.cn')

    def test_get_sld_Same_as_above_but_punycoded6(self):
        assert 'xn--85x722f.xn--fiqs8s' == publicsuffix.get_sld('xn--85x722f.xn--fiqs8s')

    def test_get_sld_Same_as_above_but_punycoded7(self):
        assert 'xn--85x722f.xn--fiqs8s' == publicsuffix.get_sld('www.xn--85x722f.xn--fiqs8s')

    def test_get_sld_Same_as_above_but_punycoded8(self):
        assert 'shishi.xn--fiqs8s' == publicsuffix.get_sld('shishi.xn--fiqs8s')

    def test_get_sld_Same_as_above_but_punycoded9(self):
        assert 'xn--fiqs8s' == publicsuffix.get_sld('xn--fiqs8s')


if __name__ == '__main__':
    unittest.main('tests')
