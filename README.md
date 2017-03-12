# Pypingdom

Python library for interact with Pingdom services (REST API and maintenance windows).

# Features:

- Check: create, delete, modify, pause, unpause, maintenance window 
- Global: maintenance window

# Requirements

- Pingdom account
- requests (0.10.8 or newer)

# Usage

## Installation

```sh
pip install pypingdom
```

## The `client` object: 

```sh
import pypingdom

client = pypingdom.Client(username="username@example.com",
                        password="your_password",
                        apikey="your_api_key",
                        email="your_email")
```

`email` is required for [Multi-User Authentication](https://www.pingdom.com/resources/api#multi-user+authentication)

## Create a new check:

```sh

c = pypingdom.Check(client, "My Awsome check")
c.host = "example.com"
c.type = "http"
c.paused = "true"
c.url = "/status"
c.resolution = 3
c.contactids = [154325, 465231, 765871]
c.alert_policies = [34857, 74234, 3w9485]
c.tags = ["test", "webservers"]
c.encryption: True
c.alert_policy: 0
c.create()
```

Refers to [this page] for the [list of options](https://www.pingdom.com/resources/api#MethodCreate+New+Check).

`alert_policy`: can be set to the `id` of an existing alert policy or to `0`for disabling alerts  

## Check operations

```sh

c = client.check("Ansible integration test")
c.pause()
c.unpause()
c.delete()
# modify
c.resolution = 5
c.modify()
```

# Maintenance windows

Since Pingdom don't allow to create maintenance windows through the REST Api, we interact with the Website for it. Therefore you this feature is hightly fragile and can break at any monment due to frontent changes on Pingdom 
website.

## Check maintenance:

```sh
from datetime import datetime

c = client.check("Ansible integration test")
c.create_maintenance("Deploy hotfix 12.10.2017", datetime(2017,10,12,22,0), datetime(2017,10,12,23,30)):
```

## Global maintenance:

```sh
from datetime import datetime

client.create_maintenance("Global maintenance", datetime(2017,10,12,22,0), datetime(2017,10,12,23,30), ["check1", "check2", "check3"]):
```


