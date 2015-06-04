#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='publicsuffix2',
    version='2.0.1',
    license='MIT and MPL-2.0',
    description='Get a public suffix for a domain name using the Public Suffix List. Forked from and using the same API as the publicsuffix package.',
    long_description='%s\n%s' % (read('README.rst'), re.sub(':obj:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    author='nexB Inc., Tomaz Solc and David Wilson',
    author_email='info@nexb.com',
    url='https://github.com/pombredanne/python-publicsuffix2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
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
        'domain', 'public suffix', 'suffix', 'dns', 'tld'
    ],
    install_requires=[
    ],
    extras_require={
        # eg: 'rst': ['docutils>=0.11'],
    },
    entry_points={}
    ,
)
