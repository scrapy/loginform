loginform
=========

.. image:: https://secure.travis-ci.org/scrapy/loginform.png?branch=master
   :target: http://travis-ci.org/scrapy/loginform

.. image:: https://img.shields.io/codecov/c/github/scrapy/loginform/master.svg
   :target: http://codecov.io/github/scrapy/loginform?branch=master
   :alt: Coverage report


loginform is a library for filling HTML login forms given the login url,
username & password. Which form and fields to fill are inferred automatically.

It's implemented on top of `lxml form filling`_, and thus depends on lxml.

Usage
-----

Usage is very simple and best illustrated with an example::

    >>> from loginform import fill_login_form
    >>> import requests
    >>> url = "https://github.com/login"
    >>> r = requests.get(url)
    >>> fill_login_form(url, r.text, "john", "secret")
    ([('authenticity_token', 'FQgPiKd1waDL+pycPH8IGutirTnP69SiZgm0zXwn+VQ='),
      ('login', 'john'),
      ('password', 'secret')],
     u'https://github.com/session',
     'POST')

And it is possible to use it as a tool to quickly debug a login form::

    $ python -m loginform -u john -p secret https://github.com/login
    url: https://github.com/session
    method: POST
    payload:
    - authenticity_token: FQgPiKd1waDL+pycPH8IGutirTnP69SiZgm0zXwn+VQ=
    - login: john
    - password: secret


Testing
-------

A collection of real-world samples is used to keep this library tested. Those
samples are managed as follows:

First, you select a site to try, find out its login url, and run the following
command to try loginform on it::

    $ python test_samples.py https://github.com/login
    [
       "https://github.com/login", 
       [
          [
             [
                "authenticity_token", 
                "NsdVWGpzxKmn7zSJSOdgnDcLIzIdJlCTO754LiEv2W4="
             ], 
             [
                "login", 
                "USER"
             ], 
             [
                "password", 
                "PASS"
             ]
          ], 
          "https://github.com/session", 
          "POST"
       ]
    ]

From the output you can judge if it worked or not. If it worked, great. If it
didn't, you would hack ``loginform.py`` to make it work and then add the sample
with::

    $ python test_samples.py https://github.com/login -w github

Note that we gave the sample a name (``github`` in this case).

To list all available samples use::

    $ python test_samples.py -l

To run all tests, install tox and run::

    $ tox

.. _lxml form filling: http://lxml.de/lxmlhtml.html#forms
.. _tox: https://pypi.python.org/pypi/tox
