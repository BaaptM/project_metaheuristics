#!/usr/bin/python
# *-* coding: utf-8 -*-
#
# permet de creer une distribution du code sur les metaheuristics

from distutils.core import setup
setup(name='Tools',
      version='1.2',
      author='mmc',
      author_email='marc.corsini@u-bordeaux2.fr',
      packages=['meta'],
      package_dir={
          'meta' : '.'},
      package_data={
          'meta': ['apidocs/*.*']}
      )

