
import sys
from setuptools import setup

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(name='pypingdom',
      version="0.0.1",
      description='Client for Pingdom Services',
      long_description="""3rd-party Python interface to Pingdom services (REST API and maintenance windows).""",
      author='Paolo Sechi',
      author_email='sekipaolo@gmail.com',
      install_requires=['requests>=0.10.8'],
      url='https://github.com/sekipaolo/pypingdom',
      packages=['pypingdom'],
      license='Apache v2.0',
      platforms='Posix; MacOS X; Windows',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Topic :: System :: Monitoring', ],
      **extra
      )
