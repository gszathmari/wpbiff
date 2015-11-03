######
WPBiff
######

Wordpress Two-Factor Authentication Brute-forcer

.. image:: https://img.shields.io/travis/gszathmari/wpbiff.svg
    :target: https://travis-ci.org/gszathmari/wpbiff
    :alt: Travis CI

.. image:: https://img.shields.io/requires/github/gszathmari/wpbiff.svg
   :target: https://requires.io/github/gszathmari/wpbiff/requirements/?branch=master
   :alt: Requirements Status

Features
========

This utility brute-forces two-factor protected Wordpress dashboards by iterating
through every possible 6-digit Google Authenticator TOTP token.

WPBiff is meant to be used together with Main-in-the-Middle based attacks against NTP.

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

For more information on remote clock tampering, please refer to this blog entry *(coming soon)*.

.. _Delorean: https://github.com/PentesterES/Delorean

Options
-------

The following section explains the basic usage of WPBiff. You can also use
the ``-h`` switch any time to get help.

-d, --date DATE        Pinned date (Format: "YYYY-MM-DD hh:mm")  [required]
-u, --username USER    Wordpress username  [required]
-p, --password PASS    Wordpress password  [required]
-a, --user-agent       HTTP User-Agent header (default: Firefox)
-t, --token TOKEN      Initial value of token (default: 000000)
-m, --max-token TOKEN  Maximum token value (default: 999999)

Use the ``--plugin`` switch to choose between the Wordpress plugin type providing
two-factor authentication for the target. Choose ``ga`` for
`Google Authenticator`_ and ``wpga`` for `WP Google Authenticator`_.

.. _Google Authenticator: https://wordpress.org/plugins/google-authenticator/
.. _WP Google Authenticator: https://wordpress.org/plugins/wp-google-authenticator/

Examples
--------

Assume NTP traffic can be intercepted between your target and the upstream NTP
server. By tampering with this traffic, you can "pin" the target's clock to a
certain time and date.

Launch `Delorean`_ NTP server to serve a fixed time and date ::

  $ ./delorean.py -d "2015-10-30 11:22"

.. _Delorean: https://github.com/PentesterES/Delorean

Redirect NTP traffic from your target to the fake NTP server.

Finally launch WPBiff as the following ::

  $ wpbiff -u admin -p admin -d "2015-10-30 11:22" --plugin ga "http://www.example.com"

This session will brute force Wordpress on ``www.example.com`` with the login username
``admin`` and password ``admin``.

Once the process finishes, WPBiff dumps the valid token and the session cookies
for accessing the Wordpress dashboard.

Speed
=====

If the clock on the target Wordpress site reverts to the same time and date
every minute (e.g. ntpdate runs minutely), three parallel instances of WBiff is
capable to find the TOTP token in about an hour.

Synthetic Test Results
----------------------

========= ======== ======== ========
Test      WPBiff 1 WPBiff 2 WPBiff 3
========= ======== ======== ========
Session 1 57m      141m     n.a.
Session 2 51m      46m      n.a.
Session 3 102m     83m      n.a.
========= ======== ======== ========

Where **WPBiff 1**, **2** and **3** were covering different ranges within
all possible combinations of 6-digit tokens ::

  ubuntu@wpbiff1:~$ wpbiff -t 000000 -m 333333 ...

  ubuntu@wpbiff2:~$ wpbiff -t 333334 -m 666666 ...

  ubuntu@wpbiff3:~$ wpbiff -t 666667 -m 999999 ...


Links
=====

* Blog entry with detailed walkthrough *(coming soon)*
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

* `Delorean`_: NTP Main-in-the-Middle tool

.. _Delorean: https://github.com/PentesterES/Delorean
