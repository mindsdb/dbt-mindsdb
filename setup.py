#!/usr/bin/env python
from setuptools import find_namespace_packages, setup

package_name = "dbt-mindsdb"
# make sure this always matches dbt/adapters/mindsdb/__version__.py
package_version = "1.0.2"
description = """The dbt adapter plugin for connecting to MindsDB"""
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='MindsDB Inc',
    author_email='admin@mindsdb.com',
    url='https://github.com/mindsdb/dbt-mindsdb',
    packages=find_namespace_packages(include=['dbt', 'dbt.*']),
    include_package_data=True,
    install_requires=[
        "dbt-core>=1.0.1",
        "mysql-connector-python~=8.0.22",
    ]
)
