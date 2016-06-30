#!/usr/bin/env python

from distutils.core import setup


install_requires = [
    'lxml==3.6.0',
]

# Testing dependencies
testing_extras = [
    # Required for running the tests
    # Nothing. Ha!

    # For coverage and PEP8 linting
    # 'coverage>=3.7.0',
    'flake8>=2.2.0',
    'isort>=4.2.0',
]

# Documentation dependencies
documentation_extras = [

]

setup(name='draftjs_exporter',
      version='0.1.0',
      description='Library to convert the Facebook Draft.js editor\'s raw ContentState to HTML.',
      author='Springload',
      author_email='hello@springload.co.nz',
      url='https://github.com/springload/draftjs_exporter',
      packages=['draftjs_exporter'],
      include_package_data=True,
      license='MIT',
      # Will look strange because pypi expects rst markup. Oh well!
      # TODO Use pandoc at publish time to circumvent this?
      # long_description=open('README.md').read(),
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Web Environment',
          'Framework :: Draft.js',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Topic :: Internet :: WWW/HTTP :: Site Management',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      install_requires=install_requires,
      extras_require={
          'testing': testing_extras,
          'docs': documentation_extras,
      },
     )
