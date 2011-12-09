# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(name='django-awesome-snippets',
      version=version,
      description="A decorator to generate and cache html snippets",
      long_description=open('README.txt').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url="http://django-awesome-snippets.rtfd.org",
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['Django'],
      entry_points="""
      """
      )
