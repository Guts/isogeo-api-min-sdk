# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
    Setup script to package Isogeo PySDK Python module

    see: https://github.com/isogeo/isogeo-api-py-minsdk/
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pathlib

from setuptools import find_packages, setup

# package (to get version)
import isogeo_pysdk

# SETUP ######################################################################

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# setup metadata
setup(
    # meta
    name="isogeo-pysdk",
    version=isogeo_pysdk.__version__,
    author="Isogeo",
    author_email="support@isogeo.com",
    description="Python package to make it easy to use Isogeo REST API",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="GIS metadata INSPIRE Isogeo API REST geographical data ISO19139",
    license="LGPL3",
    url="https://github.com/isogeo/isogeo-api-py-minsdk",
    project_urls={
        "Docs": "https://isogeo-api-pysdk.readthedocs.io/",
        "Bug Reports": "https://github.com/isogeo/isogeo-api-py-minsdk/issues/",
        "Source": "https://github.com/isogeo/isogeo-api-py-minsdk/",
        "Isogeo API": "http://help.isogeo.com/api/"
    },
    # dependencies
    install_requires=["requests>=2.20.0"],
    extras_require={
        "api-write": ["requests_oauthlib"],
        "dev": ["configparser"],
        "test": ["coverage", "pycodestyle", "python-dateutil"],
    },
    python_requires=">=3.6, <4",
    # packaging
    packages=find_packages(
        exclude=["contrib", "docs", "*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
