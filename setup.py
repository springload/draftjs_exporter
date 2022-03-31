#!/usr/bin/env python

from setuptools import find_packages, setup  # type: ignore

from draftjs_exporter import __version__

with open("README.md", encoding="utf-8") as readme_file:
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Editors :: Word Processors",
        "Typing :: Typed",
    ],
    package_data={"draftjs_exporter": ["py.typed"]},
    extras_require={
        # Keep this in sync with the dependencies in setup.py, requirements.txt, tox.ini.
        "lxml": ["lxml>=4.2.0,<5"],
        "html5lib": ["beautifulsoup4>=4.4.1,<5", "html5lib>=0.999,<2"],
    },
    zip_safe=False,
)
