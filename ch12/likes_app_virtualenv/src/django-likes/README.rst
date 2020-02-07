=============================
django-likes
=============================

.. image:: https://badge.fury.io/py/django-likes.svg
    :target: https://badge.fury.io/py/django-likes

.. image:: https://travis-ci.org/archatas/django-likes.svg?branch=master
    :target: https://travis-ci.org/archatas/django-likes

.. image:: https://codecov.io/gh/archatas/django-likes/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/archatas/django-likes

A Django app for liking anything on your website.

Documentation
-------------

The full documentation is at https://django-likes.readthedocs.io.

Quickstart
----------

Install django-likes::

    pip install django-likes

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'likes.apps.LikesConfig',
        ...
    )

Add django-likes's URL patterns:

.. code-block:: python

    from likes import urls as likes_urls


    urlpatterns = [
        ...
        url(r'^', include(likes_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
