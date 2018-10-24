#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals

import io

from draftjs_exporter import __version__

from setuptools import find_packages, setup

dependencies = {
    # Keep this in sync with the dependencies in tox.ini.
    'lxml': [
        'lxml>=4.2.0,<5',
    ],
    'html5lib': [
        'beautifulsoup4>=4.4.1,<5',
        'html5lib>=0.999,<=1.0.1',
    ],
    'docs': [],
}

# Development extras.
dependencies['testing'] = [
    # Required for running the tests.
    'tox>=2.3.1',

    # Benchmark dependencies.
    'markov_draftjs==0.1.1',
    'memory-profiler==0.47',
    'psutil==5.4.1',

    # For coverage and PEP8 linting.
    'coverage>=4.1.0',
    'flake8>=3.2.0',
    'isort==4.2.5',
] + dependencies['html5lib'] + dependencies['lxml']

long_description = io.open('README.md', encoding='utf-8').read()

setup(
    name='draftjs_exporter',
    version=__version__,
    description='Library to convert rich text from Draft.js raw ContentState to HTML',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Springload',
    author_email='hello@springload.co.nz',
    url='https://github.com/springload/draftjs_exporter',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Editors :: Word Processors',
    ],
    install_requires=[],
    extras_require=dependencies,
    zip_safe=False,
)
