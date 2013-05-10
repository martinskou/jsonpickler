#!/usr/bin/env python

import os
import sys

import jsonpickler

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'jsonpickler'
]

requires = []

setup(
    name='jsonpickler',
    version=jsonpickler.__version__,
    description='Python JSON Pickler.',
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.md').read(),
    author='Martin Skou',
    author_email='martinskou@gmail.com',
    url='',
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=requires,
    setup_requires=[],
    license='MIT license',
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT license',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ),
)