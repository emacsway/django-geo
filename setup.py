#!/usr/bin/env python
#
# Copyright (c) 2011 Ivan Zakrevsky and contributors.
import os.path
from setuptools import setup, find_packages
import metadata

app_name = metadata.name
version = metadata.version

setup(
    name = app_name,
    version = version,

    packages = find_packages(),

    author = "Ivan Zakrevsky",
    author_email = "ivzak@yandex.ru",
    description = "Django geo.",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    license = "BSD License",
    keywords = "django",
    dependency_links=[
        'hg+https://bitbucket.org/emacsway/django-ext#egg=django-ext',
        'hg+https://bitbucket.org/emacsway/django-tree-select#egg=django-tree-select',
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url = "https://bitbucket.org/emacsway/{0}".format(app_name),
)
