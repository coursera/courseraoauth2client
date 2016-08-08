courseraoauth2client
====================

.. image:: https://travis-ci.org/coursera/courseraoauth2client.svg
    :target: https://travis-ci.org/coursera/courseraoauth2client

This project is a library consisting of a command line interface and a client
for interacting with Coursera's OAuth2 authorized APIs.

Installation
------------

To install this sdk, simply execute::

    sudo pip install courseraoauth2client

`pip <https://pip.pypa.io/en/latest/index.html>`_ is a python package manager.
If you do not have ``pip`` installed on your machine, please follow the
installation instructions for your platform found at:
https://pip.pypa.io/en/latest/installing.html#install-or-upgrade-pip

Setup
-----

Before using Coursera's OAuth2 APIs, be sure you know your client id,
client secret, and scopes you want for for your application. You may create
an application at https://accounts.coursera.org/console. When creating the
application, set the
``Redirect URI`` to be ``http://localhost:9876``.

Next, authorize your application by running ``courseraoauth2client config authorize --app APP``
where ``APP`` is a disambiguating identifier to be referred to later when making Coursera API calls.


Command Line Interface
----------------------

The project includes a command line tool. Simply run::

    courseraoauth2client -h

for a complete list of features, flags, and documentation.


config
^^^^^^

Configures the Coursera OAuth2 client library.

Examples:
 - ``courseraoauth2client config authorize --app APP``

   Configures the tool to go through the `authorization secret <https://tools.ietf.org/html/rfc6749#section-4.1>`_ flow for application ``APP``.
 - ``courseraoauth2client config check-auth --app APP``

   Checks whether the current instance can authorize against Coursera's API server for application ``APP``

Usage
-----------

::

  import requests
  from courseraoauth2client import oauth2
  ...
  app = 'my_application_name'
  url = 'https://api.coursera.org/api/externalBasicProfiles.v1?q=me&fields=name'
  auth = oauth2.build_oauth2(app=app).build_authorizer()
  response = requests.get(url, auth=auth)
  print response.json()

If ``my_application_name`` was successfully configured, you will be able to
successfully make a request. Otherwise, an exception will be thrown telling you
to set up your application for API access.

Bugs / Issues / Feature Requests
--------------------------------

Please us the github issue tracker to document any bugs or other issues you
encounter while using this tool.


Developing / Contributing
-------------------------

We recommend developing ``courseraoauth2client`` within a python
`virtualenv <https://pypi.python.org/pypi/virtualenv>`_.
To get your environment set up properly, do the following::

    virtualenv venv
    source venv/bin/activate
    python setup.py develop
    pip install -r test_requirements.txt

Tests
^^^^^

To run tests, simply run: ``nosetests``, or ``tox``.

Code Style
^^^^^^^^^^

Code should conform to pep8 style requirements. To check, simply run::

    pep8 courseraoauth2client tests
