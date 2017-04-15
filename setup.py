
from setuptools import setup
from setuptools.config import read_configuration

conf = read_configuration("setup.cfg")

setup(name='pypingdom',
      version="0.0.6",
      description='Client for Pingdom Services',
      long_description=conf['metadata']['long_description'],
      author='Paolo Sechi',
      author_email='sekipaolo@gmail.com',
      install_requires=['requests>=0.10.8', 'six>=1.10.0'],
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
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3'
                   ]
      )
