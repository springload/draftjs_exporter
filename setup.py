#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals

import io
import re

from draftjs_exporter import __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

dependencies = []

html5lib_dependencies = [
    'beautifulsoup4>=4.4.1,<5',
    'html5lib>=0.999,<=1.0b10',
]

lxml_dependencies = [
    'lxml>=3.6.0',
]

testing_dependencies = [
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
] + html5lib_dependencies + lxml_dependencies

documentation_dependencies = [

]

RE_MD_CODE_BLOCK = re.compile(
    r'```(?P<language>\w+)?\n(?P<lines>.*?)```', re.S)
RE_LINK = re.compile(r'\[(?P<text>.*?)\]\((?P<url>.*?)\)')
RE_IMAGE = re.compile(r'\!\[(?P<text>.*?)\]\((?P<url>.*?)\)')
RE_TITLE = re.compile(r'^(?P<level>#+)\s*(?P<title>.*)$', re.M)
RE_CODE = re.compile(r'``([^<>]*?)``')

RST_TITLE_LEVELS = ['=', '-', '~']


def md2pypi(filename):
    '''
    Load .md (markdown) file and sanitize it for PyPI.
    '''
    content = io.open(filename).read()

    for match in RE_MD_CODE_BLOCK.finditer(content):
        rst_block = '\n'.join(
            ['.. code-block:: {language}'.format(**match.groupdict()), ''] +
            ['    {0}'.format(l) for l in match.group('lines').split('\n')] +
            ['']
        )
        content = content.replace(match.group(0), rst_block)

    for match in RE_IMAGE.finditer(content):
        content = content.replace(match.group(0), match.group(1))

    content = RE_LINK.sub('`\g<text> <\g<url>>`_', content)
    content = RE_CODE.sub('``\g<1>``', content)

    for match in RE_TITLE.finditer(content):
        level = len(match.group('level')) - 1
        underchar = RST_TITLE_LEVELS[level]
        title = match.group('title')
        underline = underchar * len(title)

        full_title = '\n'.join((title, underline))
        content = content.replace(match.group(0), full_title)

    return content


setup(
    name='draftjs_exporter',
    version=__version__,
    description='Library to convert rich text from Draft.js raw ContentState to HTML',
    long_description=md2pypi('README.md'),
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
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Editors :: Word Processors',
    ],
    install_requires=dependencies,
    extras_require={
        # Special extra installs for the built-in DOM engines.
        'lxml': lxml_dependencies,
        'html5lib': html5lib_dependencies,
        # Development extras.
        'testing': testing_dependencies,
        'docs': documentation_dependencies,
    },
    zip_safe=False)
