# -*- coding: utf-8 -*-
"""Well this is our setup tools definition for this project."""
import os

from setuptools import setup
# from setuptools.config import read_configuration  # only works in newer setuptools
# conf = read_configuration("setup.cfg")
#       long_description=conf['metadata']['long_description'],

BASEDIR = os.path.dirname(__file__)

with open(os.path.join(BASEDIR, 'README.rst'), 'r') as f:
    README = f.read()


setup(name='pypingdom',
      version='0.2.2',
      description='Client for Pingdom Services',
      long_description=README,
      author='Paolo Sechi',
      author_email='sekipaolo@gmail.com',
      install_requires=['requests>=0.10.8', 'six>=1.10.0'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest>=3.0.7', 'requests-mock>=1.3.0'],
      url='https://github.com/sekipaolo/pypingdom',
      packages=['pypingdom'],
      license='Apache v2.0',
      platforms='Posix; MacOS X; Windows',
      zip_safe=True,
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Topic :: System :: Monitoring',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.6'
                   ]
      )
