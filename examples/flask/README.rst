Flask application example
=========================

`Flask <http://flask.pocoo.org/>`_ works great with μMongo !

This application show a simple API usecase. It uses:

- PyMongo as MongoDB driver to use with μMongo
- Flask as web framework
- Babel for error messages localization


Some examples using `http command <http://httpie.org>`_:

Displaying a user:

.. code-block::

    $ http  http://localhost:5000/users/572723781d41c8223255705e
    HTTP/1.0 200 OK
    Content-Length: 145
    Content-Type: application/json
    Date: Mon, 02 May 2016 10:07:35 GMT
    Server: Werkzeug/0.14.1 Python/3.5.3

    {
        "birthday": "1953-06-15T00:00:00+00:00", 
        "firstname": "Jinping", 
        "id": "572723781d41c8223255705e", 
        "lastname": "Xi", 
        "nick": "xiji"
    }

Bad payload while trying to create user:

.. code-block::

    $ http POST http://localhost:5000/users bad=field birthday=42 
    HTTP/1.0 400 BAD REQUEST
    Content-Length: 132
    Content-Type: application/json
    Date: Mon, 02 May 2016 10:06:12 GMT
    Server: Werkzeug/0.14.1 Python/3.5.3

    {
        "message": {
            "_schema": [
                "Unknown field name bad."
            ], 
            "birthday": [
                "Not a valid datetime."
            ]
        }
    }

Same thing but with a ``accept-language`` header to specify French as prefered language:

.. code-block::

    $ http POST http://localhost:5000/users "Accept-Language:fr; q=1.0, en; q=0.5" bad=field birthday=42
    HTTP/1.0 400 BAD REQUEST
    Content-Length: 130
    Content-Type: application/json
    Date: Mon, 02 May 2016 10:05:20 GMT
    Server: Werkzeug/0.14.1 Python/3.5.3

    {
        "message": {
            "_schema": [
                "Champ bad unconnu."
            ], 
            "birthday": [
                "Pas une datetime valide."
            ]
        }
    }
