# Thycotic SDK Python Package

A Python package to facilitate the connection to the Thycotic Secret Server

## Prerequisites

Python 2.7* and Python 3.*

## Downloading the package

You can download the package here or through the pip command:

``` python
python pip install secret-server-sdk-client
```

or

```python
python -m pip install secret-server-sdk-client
```

## Initial Setup

Import the SDK Client

``` python
from secret_server.sdk_client import SDK_Client
```

Instantiate the ```SDK_Client``` object

```python
client = SDK_Client()
```

Configure the connection to your Secret Server instance by using the

``` python
configure(<sdk_path>, <url>, <rule>, <key>)
```

**required parameters:**

- ```sdk_path``` - the path to the directory containing the SDK client
- ```url``` - theURL to your Secret Server instance
- ```rule``` - the name of an onboarding rule you have created
- ```key``` - the onboarding key for that rule, if applicable

```python
client.configure(os.environ.get('HOME') + '\\tss\\', 'https://myserver/SecretServer',
                 'OnboardingRule', 'oB0arD1ngKey')
```

Another way to configure the connection to your Secret Server instance:

```python
client.config.SDK_CONFIG['path'] = os.environ.get('HOME') + '\\tss\\'
client.config.SDK_CONFIG['url'] = 'https://myserver/SecretServer'
client.config.SDK_CONFIG['rule'] = 'OnboardingRule'
client.config.SDK_CONFIG['key'] = 'oB0arD1ngKey'
```

Alternatively, you can also pull configuration from the current environment using the
os.environ object:

```python
client.configure_from_env()
```

The methods sets the config using the following variables

```python
os.environ.get('SDK_CLIENT_PATH')
os.environ.get('SECRET_SERVER_URL')
os.environ.get('SDK_CLIENT_RULE')
os.environ.get('SDK_CLIENT_KEY')
```

Initialize the connection to the Secret Server:

```python
client.commands.initialize()
```

Once the configuration and initialization are complete, they do not need to be run again.
Encrypted configuration files created in the current directory will be used to establish the
connection to Secret Server instance.

## Usage

Fetch a secret by ID 

```python
# retrieve the full representation of a secret
secret = client.commands.get_secret(1)

# retrieve only the secret fields
secret = client.commands.get_secret(1, field = 'all')

# retrieve only a single secret field value by slug
password = client.commands.get_secret(1, field = 'password')
```

To remove the connection to Secret Server and delete all configuration:

```python
client.commands.remove()
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

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thycotic SDK