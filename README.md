# Thycotic SDK Python Package

A Python package to facilitate the connection to the Thycotic Secret Server

## Prerequisites

Python 2.7* and Python 3.*

Knowledge of Secret Server's SDK Client Accounts to set up the rules

## Downloading the package

You can download the package here or through the pip command:

``` commandline
python pip install secret-server-sdk-client
```

or

```commandline
python -m pip install secret-server-sdk-client
```

## Initial Setup

Import the SDK Client and instantiate it

```python
from secret_server.sdk_client import SdkClient
client = SdkClient

```

Configure the connection to your Secret Server instance by using the

```
configure(<url>, <rule>, <key>)
```

**parameters:**

- ```url``` - the Url to your Secret Server instance
- ```rule``` - the name of an onboarding rule you have created
- ```key``` - the onboarding key for that rule, if applicable

```python
from secret_server.sdk_client import  SdkClient
client = SdkClient()
client.configure(url='https://myserver/SecretServer',rule='OnboardingRule', key='oB0arD1ngKey')

# Or

creds = {
  "url" :"https://myserver/SecretServer",
  "rule" : "OnboardingRuleName",
  "key" : "oB0arD1ngKey"
}
client.configure(**creds)
# Alternatively, you can define environment variables and the client will automatically use them
client.configure()

```
Once the configuration and initialization are complete, they do not need to be run again.
Encrypted configuration files created in the current directory will be used to establish the
connection to Secret Server instance.

## Usage

Fetch a secret by ID

```python
# retrieve the full representation of a secret
from secret_server.sdk_client import  SdkClient
client = SdkClient()
secret = client.get_secret(1)

# retrieve only a single secret field value by slug
password = client.get_secret_field(1, 'password')
```

To remove the connection to Secret Server and delete all configuration:

``` python
from secret_server.sdk_client import  SdkClient
client = SdkClient()
client.remove()
# OR
client.remove(True)
# True will revoke the client in Secret Server as well. Proper permissions by the API account are required

```

## Cache Settings

By default, no secret values are stored on the local machine. As such, every call to

```get_secret``` will result in a round-trip to the server. If the server is unavailable,
the call will fail.

To change this behavior, set the cache strategy using the

```set_cache(<cache_strategy>, <cache_age>)``` with the required parameters:

- ```cache_strategy``` - the numeric representation of the cache strategy for the secrets
- ```cache_age``` - cache age (the maximum time, in minutes, that a cached value will be usable)

Examples of setting cache:

```python
from secret_server.sdk_client import  SdkClient
client = SdkClient()
# The default (never cache secrets). Cache age is optional for this choice
client.set_cache(0)

# Check the server first; if unavailable, return the last retrieved value, if present.
# Use this strategy for improved fault tolerance.
# Server Then Cache for 5 minutes
client.set_cache(1, 5)

# Check the cache first; if no value is present, retrieve it from the server.
# Use this strategy for improved performance.
# Cache Then Server for 10 minutes
client.set_cache(2, 10)

# Same as the above mode, but allow an expired cached value to be used if the server 
# is unavailable.
# Cache Then Server Fallback on Expired Cache for 15 minutes
client.set_cache(3, 15)

# Clear all cached values immediately
client.commands.clear_cache()
```

## Authors

Paulo Dorado
Ali Falahi - Rewrote the package to remove reliance on the CLI

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thycotic SDK