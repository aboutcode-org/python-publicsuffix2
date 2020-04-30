import unittest
import publicsuffix2 as ps2


class TestPSScenarios(unittest.TestCase):

    def setUp(self):
        self.psl = None

    def validate_tld_empty_label(self):
        self.assertIsNone(self.psl.get_tld(None))
        self.assertIsNone(self.psl.get_tld(''))
        self.assertIsNone(self.psl.get_tld('', strict=True))
        self.assertIsNone(self.psl.get_tld('', wildcard=False))
        self.assertIsNone(self.psl.get_tld('', strict=True, wildcard=False))
        self.assertIsNone(self.psl.get_tld('.'))
        self.assertIsNone(self.psl.get_tld('.', strict=True))
        self.assertIsNone(self.psl.get_tld('.', wildcard=False))
        self.assertIsNone(self.psl.get_tld('.', strict=True, wildcard=False))
        self.assertIsNone(self.psl.get_tld('..'))
        self.assertIsNone(self.psl.get_tld('..', strict=True))
        self.assertIsNone(self.psl.get_tld('..', wildcard=False))
        self.assertIsNone(self.psl.get_tld('..', strict=True, wildcard=False))
        self.assertIsNone(self.psl.get_tld('....'))
        self.assertIsNone(self.psl.get_tld('....', strict=True))
        self.assertIsNone(self.psl.get_tld('....', wildcard=False))
        self.assertIsNone(self.psl.get_tld('....', strict=True, wildcard=False))

    def validate_sld_empty_label(self):
        self.assertIsNone(self.psl.get_sld(None))
        self.assertIsNone(self.psl.get_sld(''))
        self.assertIsNone(self.psl.get_sld('', strict=True))
        self.assertIsNone(self.psl.get_sld('', wildcard=False))
        self.assertIsNone(self.psl.get_sld('', strict=True, wildcard=False))
        self.assertIsNone(self.psl.get_sld('.'))
        self.assertIsNone(self.psl.get_sld('.', strict=True))
        self.assertIsNone(self.psl.get_sld('.', wildcard=False))
        self.assertIsNone(self.psl.get_sld('.', strict=True, wildcard=False))
        self.assertIsNone(self.psl.get_sld('..'))
        self.assertIsNone(self.psl.get_sld('..', strict=True))
        self.assertIsNone(self.psl.get_sld('..', wildcard=False))
        self.assertIsNone(self.psl.get_sld('..', strict=True, wildcard=False))
        self.assertIsNone(self.psl.get_sld('....'))
        self.assertIsNone(self.psl.get_sld('....', strict=True))
        self.assertIsNone(self.psl.get_sld('....', wildcard=False))
        self.assertIsNone(self.psl.get_sld('....', strict=True, wildcard=False))

    def validate_components_empty_label(self):
        self.assertEqual((None, None, None), self.psl.get_components(None))
        self.assertEqual((None, None, None), self.psl.get_components(''))
        self.assertEqual((None, None, None), self.psl.get_components('', strict=True))
        self.assertEqual((None, None, None), self.psl.get_components('', wildcard=False))
        self.assertEqual((None, None, None), self.psl.get_components('', strict=True, wildcard=False))
        self.assertEqual((None, None, None), self.psl.get_components('.'))
        self.assertEqual((None, None, None), self.psl.get_components('.', strict=True))
        self.assertEqual((None, None, None), self.psl.get_components('.', wildcard=False))
        self.assertEqual((None, None, None), self.psl.get_components('.', strict=True, wildcard=False))
        self.assertEqual((None, None, None), self.psl.get_components('..'))
        self.assertEqual((None, None, None), self.psl.get_components('..', strict=True))
        self.assertEqual((None, None, None), self.psl.get_components('..', wildcard=False))
        self.assertEqual((None, None, None), self.psl.get_components('..', strict=True, wildcard=False))
        self.assertEqual((None, None, None), self.psl.get_components('....'))
        self.assertEqual((None, None, None), self.psl.get_components('....', strict=True))
        self.assertEqual((None, None, None), self.psl.get_components('....', wildcard=False))
        self.assertEqual((None, None, None), self.psl.get_components('....', strict=True, wildcard=False))

    def validate_tld(self, tld: str, expected: tuple):
        # tld-only case
        self.assertEqual(expected[0], self.psl.get_tld(tld))
        self.assertEqual(expected[1], self.psl.get_tld(tld, strict=True))
        self.assertEqual(expected[2], self.psl.get_tld(tld, wildcard=False))
        self.assertEqual(expected[3], self.psl.get_tld(tld, strict=True, wildcard=False))

        # empty SLD label
        self.assertEqual(expected[0], self.psl.get_tld('.' + tld))
        self.assertEqual(expected[1], self.psl.get_tld('.' + tld, strict=True))
        self.assertEqual(expected[2], self.psl.get_tld('.' + tld, wildcard=False))
        self.assertEqual(expected[3], self.psl.get_tld('.' + tld, strict=True, wildcard=False))

        # empty SLD label, multiple dots
        self.assertEqual(expected[0], self.psl.get_tld('....' + tld))
        self.assertEqual(expected[1], self.psl.get_tld('....' + tld, strict=True))
        self.assertEqual(expected[2], self.psl.get_tld('....' + tld, wildcard=False))
        self.assertEqual(expected[3], self.psl.get_tld('....' + tld, strict=True, wildcard=False))

        # <SLL>.<TLD> case
        self.assertEqual(expected[0], self.psl.get_tld('example.' + tld))
        self.assertEqual(expected[1], self.psl.get_tld('example.' + tld, strict=True))
        self.assertEqual(expected[2], self.psl.get_tld('example.' + tld, wildcard=False))
        self.assertEqual(expected[3], self.psl.get_tld('example.' + tld, strict=True, wildcard=False))

        # <SLL>..<TLD> case -> empty SLL + prefix
        self.assertEqual(expected[0], self.psl.get_tld('example..' + tld))
        self.assertEqual(expected[1], self.psl.get_tld('example..' + tld, strict=True))
        self.assertEqual(expected[2], self.psl.get_tld('example..' + tld, wildcard=False))
        self.assertEqual(expected[3], self.psl.get_tld('example..' + tld, strict=True, wildcard=False))

        # <prefix>.<SLL>.<TLD> case
        self.assertEqual(expected[0], self.psl.get_tld('www.example.' + tld))
        self.assertEqual(expected[1], self.psl.get_tld('www.example.' + tld, strict=True))
        self.assertEqual(expected[2], self.psl.get_tld('www.example.' + tld, wildcard=False))
        self.assertEqual(expected[3], self.psl.get_tld('www.example.' + tld, strict=True, wildcard=False))

    def validate_sld(self, domain: str, expected: tuple):
        self.assertEqual(expected[0], self.psl.get_sld(domain))
        self.assertEqual(expected[1], self.psl.get_sld(domain, strict=True))
        self.assertEqual(expected[2], self.psl.get_sld(domain, wildcard=False))
        self.assertEqual(expected[3], self.psl.get_sld(domain, strict=True, wildcard=False))

    def validate_components(self, domain: str, expected: tuple):
        self.assertEqual(expected[0], self.psl.get_components(domain))
        self.assertEqual(expected[1], self.psl.get_components(domain, strict=True))
        self.assertEqual(expected[2], self.psl.get_components(domain, wildcard=False))
        self.assertEqual(expected[3], self.psl.get_components(domain, strict=True, wildcard=False))

    def test_01a_unknown_tld(self):
        self.psl = ps2.PublicSuffixList([])

        self.validate_tld_empty_label()

        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='aBc', expected=('abc', None, 'abc', None))

    def test_01b_unknown_tld(self):
        self.psl = ps2.PublicSuffixList([])

        self.validate_sld_empty_label()

        self.validate_sld(domain='abc', expected=('abc', None, 'abc', None))
        self.validate_sld(domain='.abc', expected=(None, None, None, None))
        self.validate_sld(domain='abc.', expected=(None, None, None, None))
        self.validate_sld(domain='example..abc', expected=(None, None, None, None))
        self.validate_sld(domain='example.abc', expected=('example.abc', None, 'example.abc', None))
        self.validate_sld(domain='.exAMPle.abc', expected=('example.abc', None, 'example.abc', None))
        self.validate_sld(domain='www.example.abc', expected=('example.abc', None, 'example.abc', None))
        self.validate_sld(domain='www.en.example.abc', expected=('example.abc', None, 'example.abc', None))

    def test_01c_unknown_tld(self):
        self.psl = ps2.PublicSuffixList([])

        self.validate_components_empty_label()

        self.validate_components(domain='abc',
                                 expected=((None, None, 'abc'), (None, None, None),
                                           (None, None, 'abc'), (None, None, None)))
        self.validate_components(domain='.abc',
                                 expected=((None, None, 'abc'), (None, None, None),
                                           (None, None, 'abc'), (None, None, None)))
        self.validate_components(domain='abc.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.abc',
                                 expected=((None, 'example', 'abc'), (None, None, None),
                                           (None, 'example', 'abc'), (None, None, None)))
        self.validate_components(domain='example..abc',
                                 expected=(('example', None, 'abc'), (None, None, None),
                                           ('example', None, 'abc'), (None, None, None)))
        self.validate_components(domain='.example.abc',
                                 expected=((None, 'example', 'abc'), (None, None, None),
                                           (None, 'example', 'abc'), (None, None, None)))
        self.validate_components(domain='.example.abc.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.abc',
                                 expected=(('www', 'example', 'abc'), (None, None, None),
                                           ('www', 'example', 'abc'), (None, None, None)))
        self.validate_components(domain='www.en.example.abc',
                                 expected=(('www.en', 'example', 'abc'), (None, None, None),
                                           ('www.en', 'example', 'abc'), (None, None, None)))

    def test_02a_known_tld(self):
        self.psl = ps2.PublicSuffixList(['com'])

        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='co.uk', expected=('uk', None, 'uk', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='cOm', expected=('com', 'com', 'com', 'com'))

    def test_02b_known_tld(self):
        self.psl = ps2.PublicSuffixList(['com'])

        self.validate_sld(domain='com', expected=('com', 'com', 'com', 'com'))
        self.validate_sld(domain='.com', expected=(None, None, None, None))
        self.validate_sld(domain='com.', expected=(None, None, None, None))
        self.validate_sld(domain='example..com', expected=(None, None, None, None))
        self.validate_sld(domain='example.com.', expected=(None, None, None, None))
        self.validate_sld(domain='example.com',
                          expected=('example.com', 'example.com', 'example.com', 'example.com'))
        self.validate_sld(domain='.exAMPle.com',
                          expected=('example.com', 'example.com', 'example.com', 'example.com'))
        self.validate_sld(domain='www.example.com',
                          expected=('example.com', 'example.com', 'example.com', 'example.com'))
        self.validate_sld(domain='www.en.example.com',
                          expected=('example.com', 'example.com', 'example.com', 'example.com'))

    def test_02c_known_tld(self):
        self.psl = ps2.PublicSuffixList(['com'])

        self.validate_components(domain='com',
                                 expected=((None, None, 'com'), (None, None, 'com'),
                                           (None, None, 'com'), (None, None, 'com')))
        self.validate_components(domain='.com',
                                 expected=((None, None, 'com'), (None, None, 'com'),
                                           (None, None, 'com'), (None, None, 'com')))
        self.validate_components(domain='com.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.com',
                                 expected=((None, 'example', 'com'), (None, 'example', 'com'),
                                           (None, 'example', 'com'), (None, 'example', 'com')))
        self.validate_components(domain='example..com',
                                 expected=(('example', None, 'com'), ('example', None, 'com'),
                                           ('example', None, 'com'), ('example', None, 'com')))
        self.validate_components(domain='.example.com',
                                 expected=((None, 'example', 'com'), (None, 'example', 'com'),
                                           (None, 'example', 'com'), (None, 'example', 'com')))
        self.validate_components(domain='.example.com.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.com',
                                 expected=(('www', 'example', 'com'), ('www', 'example', 'com'),
                                           ('www', 'example', 'com'), ('www', 'example', 'com')))
        self.validate_components(domain='www.en.example.com',
                                 expected=(('www.en', 'example', 'com'), ('www.en', 'example', 'com'),
                                           ('www.en', 'example', 'com'), ('www.en', 'example', 'com')))

    def test_03a_negated_tld(self):
        self.psl = ps2.PublicSuffixList(['com', '!org'])

        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='org', expected=(None, None, None, None))
        self.validate_tld(tld='oRg', expected=(None, None, None, None))

    def test_03b_negated_tld(self):
        self.psl = ps2.PublicSuffixList(['com', '!org'])

        # validate the behavior with negated TLD
        self.validate_sld(domain='org', expected=(None, None, None, None))
        self.validate_sld(domain='.org', expected=(None, None, None, None))
        self.validate_sld(domain='org.', expected=(None, None, None, None))
        self.validate_sld(domain='example..org', expected=(None, None, None, None))
        self.validate_sld(domain='example.org.', expected=(None, None, None, None))
        self.validate_sld(domain='example.org', expected=(None, None, None, None))
        self.validate_sld(domain='.exAMPle.org', expected=(None, None, None, None))
        self.validate_sld(domain='www.example.org', expected=(None, None, None, None))
        self.validate_sld(domain='www.en.example.org', expected=(None, None, None, None))

    def test_03c_negated_tld(self):
        self.psl = ps2.PublicSuffixList(['!org'])

        self.validate_components(domain='org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='.org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='org.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example..org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='.example.org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='.example.org.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.en.example.org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))

    def test_04a_known_etld(self):
        self.psl = ps2.PublicSuffixList(['com', 'co.uk'])

        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='uk', expected=('uk', 'uk', 'uk', 'uk'))
        self.validate_tld(tld='co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))

    def test_04b_known_etld(self):
        self.psl = ps2.PublicSuffixList(['co.uk'])

        # TLD of eTLD is automatically registered
        self.validate_sld(domain='uk', expected=('uk', 'uk', 'uk', 'uk'))
        self.validate_sld(domain='.uk', expected=(None, None, None, None))
        self.validate_sld(domain='uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example..uk', expected=(None, None, None, None))
        self.validate_sld(domain='example.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))
        self.validate_sld(domain='.exAMPle.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))
        self.validate_sld(domain='www.example.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))
        self.validate_sld(domain='www.en.example.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))

        # validate ETLD
        self.validate_sld(domain='co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='.co.uk', expected=(None, None, None, None))
        self.validate_sld(domain='co.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example..co.uk', expected=(None, None, None, None))
        self.validate_sld(domain='example.co.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example.co.uk',
                          expected=('example.co.uk', 'example.co.uk', 'example.co.uk', 'example.co.uk'))
        self.validate_sld(domain='.exAMPle.co.uk',
                          expected=('example.co.uk', 'example.co.uk', 'example.co.uk', 'example.co.uk'))
        self.validate_sld(domain='www.example.co.uk',
                          expected=('example.co.uk', 'example.co.uk', 'example.co.uk', 'example.co.uk'))
        self.validate_sld(domain='www.en.example.co.uk',
                          expected=('example.co.uk', 'example.co.uk', 'example.co.uk', 'example.co.uk'))

    def test_04c_known_etld(self):
        self.psl = ps2.PublicSuffixList(['co.uk'])

        # TLD of eTLD is automatically registered
        self.validate_components(domain='uk',
                                 expected=((None, None, 'uk'), (None, None, 'uk'),
                                           (None, None, 'uk'), (None, None, 'uk')))
        self.validate_components(domain='.uk',
                                 expected=((None, None, 'uk'), (None, None, 'uk'),
                                           (None, None, 'uk'), (None, None, 'uk')))
        self.validate_components(domain='uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.uk',
                                 expected=((None, 'example', 'uk'), (None, 'example', 'uk'),
                                           (None, 'example', 'uk'), (None, 'example', 'uk')))
        self.validate_components(domain='example..uk',
                                 expected=(('example', None, 'uk'), ('example', None, 'uk'),
                                           ('example', None, 'uk'), ('example', None, 'uk')))
        self.validate_components(domain='.example.uk',
                                 expected=((None, 'example', 'uk'), (None, 'example', 'uk'),
                                           (None, 'example', 'uk'), (None, 'example', 'uk')))
        self.validate_components(domain='.example.uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.uk',
                                 expected=(('www', 'example', 'uk'), ('www', 'example', 'uk'),
                                           ('www', 'example', 'uk'), ('www', 'example', 'uk')))
        self.validate_components(domain='www.en.example.uk',
                                 expected=(('www.en', 'example', 'uk'), ('www.en', 'example', 'uk'),
                                           ('www.en', 'example', 'uk'), ('www.en', 'example', 'uk')))

        # Validate ETLD
        self.validate_components(domain='co.uk',
                                 expected=((None, None, 'co.uk'), (None, None, 'co.uk'),
                                           (None, None, 'co.uk'), (None, None, 'co.uk')))
        self.validate_components(domain='.co.uk',
                                 expected=((None, None, 'co.uk'), (None, None, 'co.uk'),
                                           (None, None, 'co.uk'), (None, None, 'co.uk')))
        self.validate_components(domain='co.uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.co.uk',
                                 expected=((None, 'example', 'co.uk'), (None, 'example', 'co.uk'),
                                           (None, 'example', 'co.uk'), (None, 'example', 'co.uk')))
        self.validate_components(domain='example..co.uk',
                                 expected=(('example', None, 'co.uk'), ('example', None, 'co.uk'),
                                           ('example', None, 'co.uk'), ('example', None, 'co.uk')))
        self.validate_components(domain='.example.co.uk',
                                 expected=((None, 'example', 'co.uk'), (None, 'example', 'co.uk'),
                                           (None, 'example', 'co.uk'), (None, 'example', 'co.uk')))
        self.validate_components(domain='.example.com.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.co.uk',
                                 expected=(('www', 'example', 'co.uk'), ('www', 'example', 'co.uk'),
                                           ('www', 'example', 'co.uk'), ('www', 'example', 'co.uk')))
        self.validate_components(domain='www.en.example.co.uk',
                                 expected=(('www.en', 'example', 'co.uk'), ('www.en', 'example', 'co.uk'),
                                           ('www.en', 'example', 'co.uk'), ('www.en', 'example', 'co.uk')))

    def test_05_simple_list_etld_with_negated_tld(self):
        self.psl = ps2.PublicSuffixList(['com', 'co.uk', '!org'])

        self.validate_tld_empty_label()
        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='uk', expected=('uk', 'uk', 'uk', 'uk'))
        self.validate_tld(tld='co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_tld(tld='org', expected=(None, None, None, None))

    def test_06_simple_list_etld_with_negated_etld(self):
        self.psl = ps2.PublicSuffixList(['com', 'gov.uk', '!org', '!co.uk'])

        self.validate_tld_empty_label()
        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='uk', expected=('uk', 'uk', 'uk', 'uk'))
        self.validate_tld(tld='gov.uk', expected=('gov.uk', 'gov.uk', 'gov.uk', 'gov.uk'))
        self.validate_tld(tld='org', expected=(None, None, None, None))
        self.validate_tld(tld='co.uk', expected=('uk', 'uk', 'uk', 'uk'))

    def test_07a_wildcard(self):
        self.psl = ps2.PublicSuffixList(['*'])
        self.validate_tld_empty_label()
        self.validate_tld(tld='abc', expected=('abc', 'abc', 'abc', None))
        self.validate_tld(tld='aBc', expected=('abc', 'abc', 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', None))
        self.validate_tld(tld='cOm', expected=('com', 'com', 'com', None))

    def test_07b_wildcard(self):
        self.psl = ps2.PublicSuffixList(['*'])

        self.validate_sld(domain='com', expected=('com', 'com', 'com', None))
        self.validate_sld(domain='.com', expected=(None, None, None, None))
        self.validate_sld(domain='com.', expected=(None, None, None, None))
        self.validate_sld(domain='example..com', expected=(None, None, None, None))
        self.validate_sld(domain='example.com.', expected=(None, None, None, None))
        self.validate_sld(domain='example.com',
                          expected=('example.com', 'example.com', 'example.com', None))
        self.validate_sld(domain='.exAMPle.com',
                          expected=('example.com', 'example.com', 'example.com', None))
        self.validate_sld(domain='www.example.com',
                          expected=('example.com', 'example.com', 'example.com', None))
        self.validate_sld(domain='www.en.example.com',
                          expected=('example.com', 'example.com', 'example.com', None))

    def test_07c_wildcard(self):
        self.psl = ps2.PublicSuffixList(['*'])

        self.validate_components(domain='com',
                                 expected=((None, None, 'com'), (None, None, 'com'),
                                           (None, None, 'com'), (None, None, None)))
        self.validate_components(domain='.com',
                                 expected=((None, None, 'com'), (None, None, 'com'),
                                           (None, None, 'com'), (None, None, None)))
        self.validate_components(domain='com.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.com',
                                 expected=((None, 'example', 'com'), (None, 'example', 'com'),
                                           (None, 'example', 'com'), (None, None, None)))
        self.validate_components(domain='example..com',
                                 expected=(('example', None, 'com'), ('example', None, 'com'),
                                           ('example', None, 'com'), (None, None, None)))
        self.validate_components(domain='.example.com',
                                 expected=((None, 'example', 'com'), (None, 'example', 'com'),
                                           (None, 'example', 'com'), (None, None, None)))
        self.validate_components(domain='.example.com.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.com',
                                 expected=(('www', 'example', 'com'), ('www', 'example', 'com'),
                                           ('www', 'example', 'com'), (None, None, None)))
        self.validate_components(domain='www.en.example.com',
                                 expected=(('www.en', 'example', 'com'), ('www.en', 'example', 'com'),
                                           ('www.en', 'example', 'com'), (None, None, None)))

    def test_08a_negated_wildcard(self):
        self.psl = ps2.PublicSuffixList(['!*'])

        self.validate_tld_empty_label()
        self.validate_tld(tld='abc', expected=(None, None, 'abc', None))
        self.validate_tld(tld='aBc', expected=(None, None, 'abc', None))
        self.validate_tld(tld='com', expected=(None, None, 'com', None))
        self.validate_tld(tld='cOm', expected=(None, None, 'com', None))

    def test_08b_negated_wildcard(self):
        self.psl = ps2.PublicSuffixList(['!*'])

        # validate the behavior with negated TLD
        self.validate_sld(domain='org', expected=(None, None, 'org', None))
        self.validate_sld(domain='.org', expected=(None, None, None, None))
        self.validate_sld(domain='org.', expected=(None, None, None, None))
        self.validate_sld(domain='example..org', expected=(None, None, None, None))
        self.validate_sld(domain='example.org.', expected=(None, None, None, None))
        self.validate_sld(domain='example.org', expected=(None, None, 'example.org', None))
        self.validate_sld(domain='.exAMPle.org', expected=(None, None, 'example.org', None))
        self.validate_sld(domain='www.example.org', expected=(None, None, 'example.org', None))
        self.validate_sld(domain='www.en.example.org', expected=(None, None, 'example.org', None))

    def test_08c_negated_wildcard(self):
        self.psl = ps2.PublicSuffixList(['!*'])

        self.validate_components(domain='org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, 'org'), (None, None, None)))
        self.validate_components(domain='.org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, 'org'), (None, None, None)))
        self.validate_components(domain='org.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, 'example', 'org'), (None, None, None)))
        self.validate_components(domain='example..org',
                                 expected=((None, None, None), (None, None, None),
                                           ('example', None, 'org'), (None, None, None)))
        self.validate_components(domain='.example.org',
                                 expected=((None, None, None), (None, None, None),
                                           (None, 'example', 'org'), (None, None, None)))
        self.validate_components(domain='.example.org.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.org',
                                 expected=((None, None, None), (None, None, None),
                                           ('www', 'example', 'org'), (None, None, None)))
        self.validate_components(domain='www.en.example.org',
                                 expected=((None, None, None), (None, None, None),
                                           ('www.en', 'example', 'org'), (None, None, None)))

    def test_09_simple_list_wildcard(self):
        self.psl = ps2.PublicSuffixList(['*', 'com'])
        self.validate_tld_empty_label()
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='abc', expected=('abc', 'abc', 'abc', None))

    def test_10_simple_list_negated_wildcard(self):
        self.psl = ps2.PublicSuffixList(['!*', 'com'])
        self.validate_tld_empty_label()
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='abc', expected=(None, None, 'abc', None))

    def test_11a_wildcard_etld(self):
        self.psl = ps2.PublicSuffixList(['*.uk', 'com'])

        self.validate_tld_empty_label()
        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='co.uk', expected=('co.uk', 'co.uk', 'uk', 'uk'))
        self.validate_tld(tld='gov.uk', expected=('gov.uk', 'gov.uk', 'uk', 'uk'))

    def test_11b_wildcard_etld(self):
        self.psl = ps2.PublicSuffixList(['*.uk'])

        # TLD of eTLD is automatically registered
        self.validate_sld(domain='uk', expected=('uk', 'uk', 'uk', 'uk'))
        self.validate_sld(domain='.uk', expected=(None, None, None, None))
        self.validate_sld(domain='uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example..uk', expected=(None, None, None, None))
        self.validate_sld(domain='example.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))
        self.validate_sld(domain='.exAMPle.uk',
                          expected=(None, None, 'example.uk', 'example.uk'))
        self.validate_sld(domain='www.example.uk',
                          expected=('www.example.uk', 'www.example.uk', 'example.uk', 'example.uk'))
        self.validate_sld(domain='www.en.example.uk',
                          expected=('en.example.uk', 'en.example.uk', 'example.uk', 'example.uk'))

        # validate ETLD
        self.validate_sld(domain='co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='.co.uk', expected=(None, None, 'co.uk', 'co.uk'))
        self.validate_sld(domain='co.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example..co.uk', expected=(None, None, 'co.uk', 'co.uk'))
        self.validate_sld(domain='example.co.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example.co.uk',
                          expected=('example.co.uk', 'example.co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='.exAMPle.co.uk',
                          expected=('example.co.uk', 'example.co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='www.example.co.uk',
                          expected=('example.co.uk', 'example.co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='www.en.example.co.uk',
                          expected=('example.co.uk', 'example.co.uk', 'co.uk', 'co.uk'))

    def test_11c_wildcard_etld(self):
        self.psl = ps2.PublicSuffixList(['*.uk'])

        # TLD of ETLD is auto-registered
        self.validate_components(domain='uk',
                                 expected=((None, None, 'uk'), (None, None, 'uk'),
                                           (None, None, 'uk'), (None, None, 'uk')))
        self.validate_components(domain='.uk',
                                 expected=((None, None, 'uk'), (None, None, 'uk'),
                                           (None, None, 'uk'), (None, None, 'uk')))
        self.validate_components(domain='uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.uk',
                                 expected=((None, None, 'example.uk'), (None, None, 'example.uk'),
                                           (None, 'example', 'uk'), (None, 'example', 'uk')))
        self.validate_components(domain='example..uk',
                                 expected=(('example', None, 'uk'), ('example', None, 'uk'),
                                           ('example', None, 'uk'), ('example', None, 'uk')))
        self.validate_components(domain='.example.uk',
                                 expected=((None, None, 'example.uk'), (None, None, 'example.uk'),
                                           (None, 'example', 'uk'), (None, 'example', 'uk')))
        self.validate_components(domain='.example.uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.uk',
                                 expected=((None, 'www', 'example.uk'), (None, 'www', 'example.uk'),
                                           ('www', 'example', 'uk'), ('www', 'example', 'uk')))
        self.validate_components(domain='www.en.example.uk',
                                 expected=(('www', 'en', 'example.uk'), ('www', 'en', 'example.uk'),
                                           ('www.en', 'example', 'uk'), ('www.en', 'example', 'uk')))

        # Validate wildcard ETLD
        self.validate_components(domain='co.uk',
                                 expected=((None, None, 'co.uk'), (None, None, 'co.uk'),
                                           (None, 'co', 'uk'), (None, 'co', 'uk')))
        self.validate_components(domain='.co.uk',
                                 expected=((None, None, 'co.uk'), (None, None, 'co.uk'),
                                           (None, 'co', 'uk'), (None, 'co', 'uk')))
        self.validate_components(domain='co.uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.co.uk',
                                 expected=((None, 'example', 'co.uk'), (None, 'example', 'co.uk'),
                                           ('example', 'co', 'uk'), ('example', 'co', 'uk')))
        self.validate_components(domain='example..co.uk',
                                 expected=(('example', None, 'co.uk'), ('example', None, 'co.uk'),
                                           ('example.', 'co', 'uk'), ('example.', 'co', 'uk')))
        self.validate_components(domain='.example.co.uk',
                                 expected=((None, 'example', 'co.uk'), (None, 'example', 'co.uk'),
                                           ('.example', 'co', 'uk'), ('.example', 'co', 'uk')))
        self.validate_components(domain='.example.co.uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.co.uk',
                                 expected=(('www', 'example', 'co.uk'), ('www', 'example', 'co.uk'),
                                           ('www.example', 'co', 'uk'), ('www.example', 'co', 'uk')))
        self.validate_components(domain='www.en.example.co.uk',
                                 expected=(('www.en', 'example', 'co.uk'), ('www.en', 'example', 'co.uk'),
                                           ('www.en.example', 'co', 'uk'), ('www.en.example', 'co', 'uk')))

    def test_12_wildcard_list_negated_etld(self):
        self.psl = ps2.PublicSuffixList(['*.uk', '!co.uk', 'com'])
        self.validate_tld_empty_label()
        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='gov.uk', expected=('gov.uk', 'gov.uk', 'uk', 'uk'))
        self.validate_tld(tld='co.uk', expected=('uk', 'uk', 'uk', 'uk'))

    def test_13a_negated_wildcard_etld(self):
        self.psl = ps2.PublicSuffixList(['!*.uk', 'co.uk', 'com'])
        self.validate_tld_empty_label()
        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_tld(tld='gov.uk', expected=('uk', 'uk', 'uk', 'uk'))

    def test_13b_negated_wildcard_etld(self):
        self.psl = ps2.PublicSuffixList(['!*.uk'])

        # TLD of eTLD is automatically registered
        self.validate_sld(domain='uk', expected=('uk', 'uk', 'uk', 'uk'))
        self.validate_sld(domain='.uk', expected=(None, None, None, None))
        self.validate_sld(domain='uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example..uk', expected=(None, None, None, None))
        self.validate_sld(domain='example.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))
        self.validate_sld(domain='.exAMPle.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))
        self.validate_sld(domain='www.example.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))
        self.validate_sld(domain='www.en.example.uk',
                          expected=('example.uk', 'example.uk', 'example.uk', 'example.uk'))

        # validate the behavior with negated TLD
        self.validate_sld(domain='co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='.co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='co.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example..co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='example.co.uk.', expected=(None, None, None, None))
        self.validate_sld(domain='example.co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='.exAMPle.co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='www.example.co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_sld(domain='www.en.example.co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))

    def test_13c_negated_wildcard_etld(self):
        self.psl = ps2.PublicSuffixList(['!*.uk'])

        # TLD of ETLD is auto-registered and positive even in the case of negated wildcard
        self.validate_components(domain='uk',
                                 expected=((None, None, 'uk'), (None, None, 'uk'),
                                           (None, None, 'uk'), (None, None, 'uk')))
        self.validate_components(domain='.uk',
                                 expected=((None, None, 'uk'), (None, None, 'uk'),
                                           (None, None, 'uk'), (None, None, 'uk')))
        self.validate_components(domain='uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.uk',
                                 expected=((None, 'example', 'uk'), (None, 'example', 'uk'),
                                           (None, 'example', 'uk'), (None, 'example', 'uk')))
        self.validate_components(domain='example..uk',
                                 expected=(('example', None, 'uk'), ('example', None, 'uk'),
                                           ('example', None, 'uk'), ('example', None, 'uk')))
        self.validate_components(domain='.example.uk',
                                 expected=((None, 'example', 'uk'), (None, 'example', 'uk'),
                                           (None, 'example', 'uk'), (None, 'example', 'uk')))
        self.validate_components(domain='.example.uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.uk',
                                 expected=(('www', 'example', 'uk'), ('www', 'example', 'uk'),
                                           ('www', 'example', 'uk'), ('www', 'example', 'uk')))
        self.validate_components(domain='www.en.example.uk',
                                 expected=(('www.en', 'example', 'uk'), ('www.en', 'example', 'uk'),
                                           ('www.en', 'example', 'uk'), ('www.en', 'example', 'uk')))

        # Verify negated wildcard etld
        self.validate_components(domain='co.uk',
                                 expected=((None, 'co', 'uk'), (None, 'co', 'uk'),
                                           (None, 'co', 'uk'), (None, 'co', 'uk')))
        self.validate_components(domain='.co.uk',
                                 expected=((None, 'co', 'uk'), (None, 'co', 'uk'),
                                           (None, 'co', 'uk'), (None, 'co', 'uk')))
        self.validate_components(domain='co.uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='example.co.uk',
                                 expected=(('example', 'co', 'uk'), ('example', 'co', 'uk'),
                                           ('example', 'co', 'uk'), ('example', 'co', 'uk')))
        self.validate_components(domain='example..co.uk',
                                 expected=(('example.', 'co', 'uk'), ('example.', 'co', 'uk'),
                                           ('example.', 'co', 'uk'), ('example.', 'co', 'uk')))
        self.validate_components(domain='.example.co.uk',
                                 expected=(('.example', 'co', 'uk'), ('.example', 'co', 'uk'),
                                           ('.example', 'co', 'uk'), ('.example', 'co', 'uk')))
        self.validate_components(domain='.example.co.uk.',
                                 expected=((None, None, None), (None, None, None),
                                           (None, None, None), (None, None, None)))
        self.validate_components(domain='www.example.co.uk',
                                 expected=(('www.example', 'co', 'uk'), ('www.example', 'co', 'uk'),
                                           ('www.example', 'co', 'uk'), ('www.example', 'co', 'uk')))
        self.validate_components(domain='www.en.example.co.uk',
                                 expected=(('www.en.example', 'co', 'uk'), ('www.en.example', 'co', 'uk'),
                                           ('www.en.example', 'co', 'uk'), ('www.en.example', 'co', 'uk')))

    def test_14_complex_list(self):
        self.psl = ps2.PublicSuffixList(['com', '!org', '!*.uk', 'co.uk', '*.us', '!ca.us', '*.ng'])
        self.validate_tld_empty_label()
        self.validate_tld(tld='abc', expected=('abc', None, 'abc', None))
        self.validate_tld(tld='com', expected=('com', 'com', 'com', 'com'))
        self.validate_tld(tld='org', expected=(None, None, None, None))
        self.validate_tld(tld='co.uk', expected=('co.uk', 'co.uk', 'co.uk', 'co.uk'))
        self.validate_tld(tld='gov.uk', expected=('uk', 'uk', 'uk', 'uk'))
        self.validate_tld(tld='wa.us', expected=('wa.us', 'wa.us', 'us', 'us'))
        self.validate_tld(tld='ca.us', expected=('us', 'us', 'us', 'us'))
        self.validate_tld(tld='abc.ng', expected=('abc.ng', 'abc.ng', 'ng', 'ng'))
