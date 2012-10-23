try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='loginner',
      version='0.1',
      license='BSD',
      description='Fill HTML login forms automatically',
      author='Scrapinghub',
      author_email='info@scrapinghub.com',
      url='http://github.com/scrapinghub/loginner',
      platforms = ['Any'],
      py_modules = ['loginform'],
      install_requires = ['lxml'],
      classifiers = [ 'Development Status :: 4 - Beta',
                      'License :: OSI Approved :: BSD License',
                      'Operating System :: OS Independent',
                      'Programming Language :: Python']
)

