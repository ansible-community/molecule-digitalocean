**************************************
DigitalOcean driver installation guide
**************************************

Requirements
============

* ``DO_API_KEY``, ``DO_API_TOKEN``, ``DO_OAUTH_TOKEN``, or ``OAUTH_TOKEN``
  exposed in your environment

Install
=======

Please refer to the `Virtual environment`_ documentation for installation best
practices. If not using a virtual environment, please consider passing the
widely recommended `'--user' flag`_ when invoking ``pip``.

.. _Virtual environment: https://virtualenv.pypa.io/en/latest/
.. _'--user' flag: https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site

.. code-block:: bash

    $ pip install 'molecule[digitalocean]'
