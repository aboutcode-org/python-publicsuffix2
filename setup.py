#!/usr/bin/python

from distutils.core import Command, setup
from distutils.command.install import INSTALL_SCHEMES
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

# Install data file into the same path as the module
for scheme in INSTALL_SCHEMES.values():
	scheme['data'] = scheme['purelib']

setup(name='publicsuffix',
	version='1.0.4',
	description='Get a public suffix for a domain name using the Public Suffix List.',
	license='MIT',
	long_description=open("README").read(),
	author='Tomaz Solc',
	author_email='tomaz.solc@tablix.org',

	py_modules = ['publicsuffix'],
	data_files = [('', ['publicsuffix.txt'])],
	provides = [ 'publicsuffix' ],

	cmdclass = { 'test': TestCommand },

	classifiers = [
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Topic :: Internet :: Name Service (DNS)",
	],
)
