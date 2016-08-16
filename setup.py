from setuptools import setup


setup(
    name='loginform',
    version='1.2.0',
    license='BSD',
    description='Fill HTML login forms automatically',
    author='Scrapinghub',
    author_email='info@scrapinghub.com',
    url='http://github.com/scrapy/loginform',
    platforms=['Any'],
    py_modules=['loginform'],
    install_requires=['lxml'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
