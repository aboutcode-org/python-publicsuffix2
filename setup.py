#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import codecs
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import Command
from setuptools import find_packages
from setuptools import setup


def read(filename):
    """
    Return the filename unicode text content stripping some reST lines and 
    updating some defaults"""
    lines = [l for l in codecs.open(join(dirname(__file__), filename), encoding='utf8')
             if not l.strip().startswith(('.. ', ':',))]
    return u''.join(lines)


class UpdatePslCommand(Command):
    """
    A setuptools command to update the vendored public suffix list to the latest.
    """
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        """
        Update the vendored public suffix list to the latest list from
        publicsuffix.org saved in the src directory of this package.

        Also create an ABOUT file with download info including the download UTC
        date/time as the version (see http://aboutcode.org)
        """

        from contextlib import closing
        from datetime import datetime
        import os

        import requests

        PSL_URL = 'https://publicsuffix.org/list/public_suffix_list.dat'
        BASE_DIR = os.path.join(os.path.dirname(__file__), 'src', 'publicsuffix2')
        PSL_FILE = os.path.join(BASE_DIR, 'public_suffix_list.dat')
        ABOUT_PSL_FILE = os.path.join(BASE_DIR, 'public_suffix_list.ABOUT')

        ABOUT_TEMPLATE = '''
about_resource: public_suffix_list.dat
name: Public Suffix List
version: %(version)s
download_url: %(PSL_URL)s
home_url: https://publicsuffix.org/

owner: Mozilla
copyright: Copyright (c) Mozilla and others
license: mpl-2.0
license_text_file: mpl-2.0.LICENSE
'''

        # current date and time as an ISO time stamp string
        version = datetime.isoformat(datetime.utcnow()).partition('.')[0]
        glocals = locals()
        print('Fetching latest list from: %(PSL_URL)s on: %(version)s' % glocals)

        fetched= requests.get(PSL_URL).content
        with open(PSL_FILE, 'wb') as pslout:
            pslout.write(fetched)
        with open(ABOUT_PSL_FILE, 'wb') as about:
            about.write(ABOUT_TEMPLATE % glocals)
        print('Saved updated %(PSL_FILE)s and %(ABOUT_PSL_FILE)s' % glocals)


setup(
    name='publicsuffix2',
    version='2.20190812',
    license='MIT and MPL-2.0',
    description='Get a public suffix for a domain name using the Public Suffix '
        'List. Forked from and using the same API as the publicsuffix package.',
    long_description_content_type = 'text/x-rst',
    long_description='%s\n%s' % (read('README.rst'), read('CHANGELOG.rst')),
    author='nexB Inc., Tomaz Solc and David Wilson',
    author_email='info@nexb.com',
    url='https://github.com/nexb/python-publicsuffix2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    setup_requires = [
        'requests >= 2.7.0',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Utilities',
        'Development Status :: 5 - Production/Stable',
    ],
    keywords=[
        'domain', 'public suffix', 'suffix', 'dns', 'tld', 'sld', 'psl', 'idna',
    ],
    cmdclass={'update_psl': UpdatePslCommand},
)
