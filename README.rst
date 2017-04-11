Pypingdom
=====================================

Python library for interact with Pingdom services (REST API and maintenance windows).


Features
-------------------------------------


* Support for `Multi-User Authentication <https://www.pingdom.com/resources/api#multi-user+authentication>`_
* Check management: create, delete, update, list
* Maintenance windows: create, delete, list

.. warning::

    Since the Pingdom REST API don't support maintenance windows, we interact with the Website for it. Therefore this feature is hightly fragile and can *break* at any monment due to frontent changes on Pingdom website.


Requirements
-------------------------------------


* Pingdom account
* requests (0.10.8 or newer)


Installation
-------------------------------------

.. code-block:: python

    pip install pypingdom


Usage
-------------------------------------

The `client` object will allow you to interact both with the REST Api and the GUI (for manintenance windows)

.. code-block:: python

    >>> import pypingdom
    >>> client = pypingdom.Client(username="username@example.com",
                            password="your_password",
                            apikey="your_api_key",
                            email="your_email")

the `email` parameter is required for `Multi-User Authentication <https://www.pingdom.com/resources/api#multi-user+authentication>`_.

Checks
-------------------------------------


Since Pingdom do not treat the check name as identifier (as we probably want to do) the client object will retrieve the check list from the API and cache it as dict ( check_name => check_instance). You can access it through the `checks` atrribute:

.. code-block:: python

    >>> client.checks["my awsome check"]
    pingdom.Check <1895866>
      autoresolve: 0
      alert_policy: 2118909
      name: Diageo
      created: 1448565930
      lasterrortime: 1489325292
      resolution: 1
      lastresponsetime: 558
      lasttesttime: 1489847772
      alert_policy_name: Production Systems
      paused: False
      host: hostname.example.com
      acktimeout: 0
      ipv6: False
      use_legacy_notifications: False
      type: http
      tags: []

a better way to retrive a check would be:

.. code-block:: python

    >>> client.get_check("my awsom check")

that will return None if the check doesn't exists

List checks with `production` and `fromtend` tags:

.. code-block:: python

    >>> client.get_checks(filters={"tags": ["production", "frontend"]})

Create a check:

.. code-block:: python

    >>> check_definition = {
            "name": "My awsome check",
            "paused": True,
            "alert_policy": 201745,
            "type": "http",
            "host": "www.google.com",
            "url": "/",
            "requestheaders": {
                'XCustom': 'my header value'
            },
            "tags": ["pypingdom-test", "custom-tag"],
            "encryption": False
        }
    >>> client.update_check(check, check_definition)


Refers to `this page <https://www.pingdom.com/resources/api#MethodCreate+New+Check>`_ for the list of options.

`alert_policy`: can be set to the `id` of an existing alert policy or omitted to disable alerts. Once created the alert policy can be changed but not disabled (API restriction)

Update a check:

.. code-block:: python

    >>> client.update_check(check, {"paused": True})

this will retrun True if an effective change was sent to the API and False otherwise (userful for idempotency usage, like ansible modules)

Delete a check:

.. code-block:: python

    >>> client.delete_check(check)


Maintenance windows
-------------------------------------

Retrive maintenances windows for production websites in the last 7 days

.. code-block:: python

    >>> import datetime
    >>> checks = client.get_checks(filters={"tags": ["production": "frontend"]})
    >>> start = datetime.datetime.now() - datetime.timedelta(days=7)
    >>> client.get_maintenances(filters={"checks": checks, "after": start}):

Create a 1 hour maintenance window for production websites

.. code-block:: python

    >>> start = datetime.datetime.now() + datetime.timedelta(minutes=10)
    >>> end = start + datetime.timedelta(hours=1)

    >>> window = client.create_maintenance(filters={"checks": checks, "name": "pypyngdom test maintenance", "start": start, "stop": stop})

Delete futures maintenance windows

.. code-block:: python

    >>> windows = client.get_maintenances(filters={"checks": checks, "after": datetime.datetime.now()}):
    >>> for m in maintenances:
        client.delete_maintenance(m)
