#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals

from codecs import open

from draftjs_exporter import __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


dependencies = [
    'beautifulsoup4>=4.4.1,<5',
    'html5lib>=0.999,<=1.0b10',
]

lxml_dependencies = [
    'lxml>=3.6.0',
]

testing_dependencies = [
    # Required for running the tests.
    'tox>=2.3.1',

    # For coverage and PEP8 linting.
    'coverage>=4.1.0',
    'flake8>=3.2.0',
    'isort>=4.2.5',
] + lxml_dependencies

documentation_dependencies = [

]

with open('README.rst', 'r', 'utf-8') as f:
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
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Editors :: Word Processors',
    ],
    install_requires=dependencies,
    extras_require={
        'testing': testing_dependencies,
        'docs': documentation_dependencies,
        'lxml': lxml_dependencies,
    },
    zip_safe=False)
