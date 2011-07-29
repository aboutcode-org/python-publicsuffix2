#!/usr/bin/python

from distutils.core import Command, setup
import unittest

UNITTESTS = [
		"tests", 
	]

class TestCommand(Command):
	user_options = [ ]

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		suite = unittest.TestSuite()

		suite.addTests( 
			unittest.defaultTestLoader.loadTestsFromNames( 
								UNITTESTS ) )

		result = unittest.TextTestRunner(verbosity=2).run(suite)

setup(name='publicsuffix',
	version='1.0.0',
	description='Get a public suffix for a domain name using the Public Suffix List.',
	license='MIT',
	long_description=open("README").read(),
	author=u'Toma\N{latin small letter z with caron} \N{latin capital letter s with caron}olc',
	author_email='tomaz.solc@tablix.org',

	py_modules = ['publicsuffix'],
	data_files = [('lib/python', ['publicsuffix.txt'])],
	provides = [ 'publicsuffix' ],

	cmdclass = { 'test': TestCommand }
)
