Django RESTive
==============

``restive`` is a library for enabling easy setup of a RESTful service in
django, and provides code for both client and server-side setup.

In keeping with DRY, ``restive`` gets all of the boiler-plate out of the way,
allowing the intuitive creation of a rich ajax experience.

Some important points:

- all communication is in JSON (this could be configurable, I guess, but I
  don't see any reason for it ATM)

  - this means that callback **functions should return a dictionary**, which
    JSON then serializes.
  - the **serialization of django models** is also supported: if the
    returned dictionary has a "_models" key, it should be a list of ORM
    instances, and it gets serialized by Django's builtin json serializer.
  - javascript POSTing to the service should put all passed data (keyword
    arguments) as JSON text under the key ``data``.

- all communication is verified by a CSRF token, to prevent forgeries. (not
  yet implemented)
- ``restive_js`` is a **client-side component** to allow ease of interaction
  from the client side as well.

Here's restive's "Hello World"::

    from restive import Service

    service = Service()

    @service.add
    def greet(request, name='Jimmy'):
        return {'message': 'Hello %s!' % name}

    urlpatterns = service.urls()

To enable your restive service, just ``include()`` the file where you defined
the service in your ``urls.py``. For example, if the above code were in
``hello_app/rest.py``::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        ('^hello/', include('hello_app.rest')),
    )

The ``greet`` function would then be available at ``http://mysite.com/hello/greet``
