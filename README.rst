######
WPBiff
######

Wordpress Two-Factor Authentication Brute-forcer

.. image:: https://img.shields.io/travis/gszathmari/wpbiff.svg
    :target: https://travis-ci.org/gszathmari/wpbiff
    :alt: Travis CI

.. image:: https://img.shields.io/pypi/dm/wpbiff.svg
   :target: https://pypi.python.org/pypi/wpbiff
   :alt: PyPI

.. image:: https://img.shields.io/requires/github/gszathmari/wpbiff.svg
   :target: https://requires.io/github/gszathmari/wpbiff/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://img.shields.io/pypi/pyversions/wpbiff.svg
   :alt: Python Versions

Features
========

This utility brute-forces two-factor protected Wordpress dashboards by iterating
through every possible 6-digit Google Authenticator TOTP token.

WPBiff is meant to be used together with man-in-the-middle based attacks against NTP.

Supported Plugins
-----------------

WPBiff is able to brute-force Wordpress login pages protected by the following
two-factor authentication plugins:

* `Google Authenticator`_ by Henrik Schack
* `WP Google Authenticator`_ by Julien Liabeuf

.. _Google Authenticator: https://wordpress.org/plugins/google-authenticator/
.. _WP Google Authenticator: https://wordpress.org/plugins/wp-google-authenticator/

Installing WPBiff
=================

The latest package is available on `PyPI`_ ::

  $ pip install wpbiff

.. _PyPI: https://pypi.python.org/pypi/wpbiff

Requirements
------------

This utility runs on Python 2.6 and 2.7

Usage Instructions
==================

In order to carry out successful attack against a two-factor protected Wordpress
blog, you must satisfy the following two pre-requisites.

Pre-requisites
--------------

The first requirement is that you must have the login username and password to
the Wordpress dashboard on ``/wp-admin``. The credentials can be acquired by
phishing, key logging or password reuse.

Secondly, you must be able to control the internal clock of the target server.
I recommend `Delorean`_ to fixate the server time to a certain point. You must
fixate an arbitrary date with the ``-d`` flag with Delorean and use the
very same time stamp with WPBiff in parallel.

For more information on remote clock tampering, please refer to this blog entry (coming soon).

.. _Delorean: https://github.com/PentesterES/Delorean

Options
-------

The following section explains the basic usage of WPBiff. You can also use
the ``-h`` switch any time to get help.

-d, --date DATE        Pinned date (Format: "YYYY-MM-DD hh:mm") [required]
-u, --username USER    Wordpress username  [required]
-p, --password PASS    Wordpress password  [required]
--plugin [ga|wpga]     Wordpress two-factor auth plugin type ("ga" or "wpga")
-a, --user-agent       HTTP User-Agent header (default: Firefox)
-t, --token TOKEN      Initial value of token (default: 000000)
-m, --max-token TOKEN  Maximum token value (default: 999999)
-h, --help             Show this message and exit.

Examples
--------

Assume you can intercept NTP traffic between your target and the NTP server it
uses. By tampering with this traffic, you can "pin" the target's clock to a
certain time and date.

Launch `Delorean`_ and fixate the target system to the current time and date ::

  $ ./delorean.py -d "2015-10-30 11:22"

.. _Delorean: https://github.com/PentesterES/Delorean

Now launch WPBiff as the following ::

  $ wpbiff -u admin -p admin -d "2015-10-30 11:22" --plugin ga "http://www.example.com"

This session will brute force Wordpress on ``www.example.com`` with the login username
``admin`` and password ``admin``.

Once the process finishes, WPBiff dumps the valid token and the session cookies
for accessing the Wordpress dashboard.

Links
=====

* Blog entry with detailed walkthrough (coming soon)
* `Source code on GitHub`_
* `Package on PyPI`_

.. _Source code on GitHub: https://github.com/gszathmari/wpbiff
.. _Package on PyPI: https://pypi.python.org/pypi/wpbiff

Contributors
============

* Gabor Szathmari - `@gszathmari`_

.. _@gszathmari: https://www.twitter.com/gszathmari

Credits
=======


* `Delorean`_ NTP Main-in-the-Middle tool

.. _Delorean: https://github.com/PentesterES/Delorean
