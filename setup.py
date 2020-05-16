#!/usr/bin/env python

import io

from setuptools import find_packages, setup

from draftjs_exporter import __version__

dependencies = {
    # Keep this in sync with the dependencies in tox.ini.
    "lxml": ["lxml>=4.2.0,<5"],
    "html5lib": ["beautifulsoup4>=4.4.1,<5", "html5lib>=0.999,<=1.0.1"],
    "docs": [],
}

# Development extras.
dependencies["testing"] = (
    [
        # Required for running the tests.
        "tox==3.15.0",
        # Benchmark dependencies.
        "markov_draftjs==0.1.1",
        "memory-profiler==0.57",
        "psutil==5.7.0",
        # For coverage and PEP8 linting.
        "coverage==5.1",
        "flake8==3.8.1",
        "isort==4.3.21",
        "mypy==0.770",
        "black==19.10b0",
    ]
    + dependencies["html5lib"]
    + dependencies["lxml"]
)

with io.open("README.md", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="draftjs_exporter",
    version=__version__,
    description="Library to convert rich text from Draft.js raw ContentState to HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Springload",
    author_email="hello@springload.co.nz",
    url="https://github.com/springload/draftjs_exporter",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Editors :: Word Processors",
        "Typing :: Typed",
    ],
    package_data={"draftjs_exporter": ["py.typed"]},
    install_requires=[],
    extras_require=dependencies,
    zip_safe=False,
)
