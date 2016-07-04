#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals

from codecs import open

from draftjs_exporter import __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


install_requires = [
    'lxml>=3.6.0',
]

# Testing dependencies
testing_extras = [
    # Required for running the tests
    'tox>=2.3.1',

    # For coverage and PEP8 linting
    'coverage>=4.1.0',
    'flake8>=2.2.0',
    'isort>=4.2.5',
]

# Documentation dependencies
documentation_extras = [

]

# Will look strange because pypi expects rst markup. Oh well!
# TODO Use pandoc at publish time to circumvent this? Convert README to rst?
with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='draftjs_exporter',
    version=__version__,
    description='Library to convert the Facebook Draft.js editor\'s raw ContentState to HTML',
    author='Springload',
    author_email='hello@springload.co.nz',
    url='https://github.com/springload/draftjs_exporter',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Editors :: Word Processors',
    ],
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        'docs': documentation_extras,
    },
    zip_safe=False)
