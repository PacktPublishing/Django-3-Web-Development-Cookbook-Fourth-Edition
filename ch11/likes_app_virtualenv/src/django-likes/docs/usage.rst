=====
Usage
=====

To use django-likes in a project, add it to your `INSTALLED_APPS`:

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
