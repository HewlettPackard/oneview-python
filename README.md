[![PyPI version](https://badge.fury.io/py/hpeOneView.svg)](https://badge.fury.io/py/hpeOneView)
[![Build Status](https://travis-ci.com/HewlettPackard/oneview-python.svg?branch=master)](https://travis-ci.com/HewlettPackard/oneview-python)
[![Coverage Status](https://coveralls.io/repos/github/HewlettPackard/oneview-python/badge.svg?branch=master)](https://coveralls.io/github/HewlettPackard/oneview-python?branch=master)

# HPE OneView SDK for Python

This library provides a pure Python interface to the HPE OneView REST APIs.

HPE OneView is a fresh approach to converged infrastructure management, inspired
by the way you expect to work, with a single integrated view of your IT
infrastructure.

The HPE OneView Python library depends on the
[Python-Future](http://python-future.org/index.html) library to provide Python
2/3 compatibility. This will be installed automatically if you use the installation
methods described below.

### Running Examples with local docker container
If you'd rather run the examples in a Docker container, you can use the Dockerfile at the top level of this repo.
All you need is Docker and git (optional).

1. Clone this repo and cd into it:
   ```bash
   $ git clone https://github.com/HewlettPackard/oneview-python.git
   $ cd oneview-python
   ```

   Note: You can navigate to the repo url and download the repo as a zip file if you don't want to use git.

2. Build the docker image: `$ docker build -t oneview-python .`

   Note: If you're behind a proxy, please edit the Dockerfile before building, uncommenting/adding the necessary ENV directives for your environment.

3. Now you can run any of the example in this directory:
   ```bash
   # Run the container, passing in your credentials to OneView and specifying which example recipe to run.
   # -v : The volume on which repo code is mounted
   # Replace "connection_templates" with the name of the example you'd like to run
   # Replace "pwd" with the path of the example file you'd like to run.

   $ docker run -it --rm \
     -v $(pwd)/:/root/oneview/
     python examples/connection_templates.py
   ```

That's it! If you'd like to modify a example, simply modify the example file (on the host), then re-run the image.

### Running Examples with published docker image
We also provide a lightweight and easy way to test and run `oneview-python`. The `hewlettpackardenterprise/hpe-oneview-sdk-for-python:<tag>` docker image contains an installation of oneview-python installation you can use by just pulling down the Docker Image:

The Docker Store image `tag` consist of two sections: `<sdk_version-OV_version>`

```bash
# Download and store a local copy of hpe-oneview-sdk-for-python and
# use it as a Docker image.
$ docker pull hewlettpackardenterprise/hpe-oneview-sdk-for-python:v5.2.0-OV5.2

# Run docker commands and this will in turn create
# a sh session where you can create files, issue commands and execute the tests
$ docker run -it hewlettpackardenterprise/hpe-oneview-sdk-for-python:v5.2.0-OV5.2 /bin/sh
```


## Installation

### From source

Either:

```bash
$ git clone https://github.com/HewlettPackard/oneview-python.git
$ cd oneview-python
$ python setup.py install --user  # to install in the user directory (~/.local)
$ sudo python setup.py install    # to install globally
```

Or if using PIP:

```bash
$ git clone https://github.com/HewlettPackard/oneview-python.git
$ cd oneview-python
$ pip install .
```

Both installation methods work if you are using virtualenv, which you should be!

### From Pypi

```bash
$ pip install hpeOneView
```


## API Implementation

A status of the HPE OneView REST interfaces that have been implemented in this Python library can be found in the [Wiki section](https://github.com/HewlettPackard/oneview-python/blob/master/endpoints-support.md).


## SDK Documentation

The latest version of the SDK documentation can be found in the [SDK Documentation section](https://hewlettpackard.github.io/oneview-python/index.html).

## Logging

This module uses Python’s Standard Library logging module. An example of how to configure logging is provided on [```/examples/logger.py```](/examples/logger.py).

More information about the logging configuration can be found in the Python Documentation.

## Configuration

### JSON

Connection properties for accessing the OneView appliance can be set in a JSON file.

Before running the samples or your own scripts, you must create the JSON file.
An example can be found at: [OneView configuration sample](examples/config-rename.json).

Note: If you have an active and valid login session and want to use it, define the sessionID in the Credentials. When sessionID is defined, you can remove username and password from your JSON (they will be disregarded anyway).

Once you have created the JSON file, you can initialize the OneViewClient:

```python
oneview_client = OneViewClient.from_json_file('/path/config.json')
```

:lock: Tip: Check the file permissions because the password is stored in clear-text.

### Environment Variables

Configuration can also be stored in environment variables:

```bash
# Required
export ONEVIEWSDK_IP='172.16.102.82'

export ONEVIEWSDK_USERNAME='Administrator'
export ONEVIEWSDK_PASSWORD='secret123'
# Or sessionID
export ONEVIEWSDK_SESSIONID='123'


# Optional
export ONEVIEWSDK_API_VERSION='800'
export ONEVIEWSDK_AUTH_LOGIN_DOMAIN='authdomain'
export ONEVIEWSDK_SSL_CERTIFICATE='<path_to_cert.crt_file>'
export ONEVIEWSDK_PROXY='<proxy_host>:<proxy_port>'
export ONEVIEWSDK_CONNECTION_TIMEOUT='<connection time-out in seconds>'
```

:lock: Tip: Make sure no unauthorized person has access to the environment variables, since the password is stored in clear-text.

Note: If you have an active and valid login session and want to use it, define the ONEVIEWSDK_SESSIONID. When a sessionID is defined, it will be used for authentication (username and password will be ignored in this case).

Once you have defined the environment variables, you can initialize the OneViewClient using the following code snippet:

```python
oneview_client = OneViewClient.from_environment_variables()
```

### Dictionary

You can also set the configuration using a dictionary. As described above, for authentication you can use username/password:


```python
config = {
    "ip": "172.16.102.82",
    "credentials": {
        "userName": "Administrator",
        "password": "secret123"
    }
}
```

 or if you have an active and valid login session and want to use it, define the sessionID in the Credentials:


```python
config = {
    "ip": "172.16.102.82",
    "credentials": {
        "sessionID": "123"
    }
}

oneview_client = OneViewClient(config)
```

:lock: Tip: Check the file permissions because the password is stored in clear-text.

### SSL Server Certificate

To enable the SDK to establish a SSL connection to the HPE OneView server, it is necessary to generate a CA Cert file containing the server credentials.

1. Fetch the HPE OneView Appliance CA certificate.
```bash
$ openssl s_client -showcerts -host <host> -port 443
```

2. Copy the server certificate wrapped with a header line and a footer line into a `<file_name>.crt` file.
```
-----BEGIN CERTIFICATE-----
... (HPE OneView Appliance certificate in base64 PEM encoding) ...
-----END CERTIFICATE-----
```
When using HPE Image Streamer, the server certificate for the HPE Image Streamer should also be added to the certificates file. Example:
```
-----BEGIN CERTIFICATE-----
... (HPE OneView Appliance certificate in base64 PEM encoding) ...
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
... (HPE Image Streamer Appliance certificate in base64 PEM encoding) ...
-----END CERTIFICATE-----
```

3. Declare the CA Certificate location when creating a `config` dictionary.
```python
config = {
    "ip": "172.16.102.82",
    "credentials": {
        "userName": "Administrator",
        "password": "secret123"
    },
    "ssl_certificate": "/home/oneview-python/my_ov_certificate.crt"
}
```

### Proxy

If your environment requires a proxy, define the proxy properties in the JSON file using the following syntax:

```json
  "proxy": "<proxy_host>:<proxy_port>"
```
OR export the `ONEVIEWSDK_PROXY` environment variable:
```bash
export ONEVIEWSDK_PROXY='<proxy_host>:<proxy_port>'
```

### Setting your OneView version

The OneView Python SDK supports the API endpoints for HPE OneView 4.10, 4.20, 5.00, 5.20, 5.30.

The current `default` HPE OneView version used by the Python SDK is `4.10`, API `800`.

To use a different API, you must set the API version on the OneViewClient configuration, either using the JSON configuration:

```json
"api_version": 800
```
OR using the Environment variable:

```bash
export ONEVIEWSDK_API_VERSION='800'
```

If this property is not specified, it will fall back to the ```800``` default value.

The API list is as follows:

- HPE OneView 4.10 API version: `800`
- HPE OneView 4.20 API version: `1000`
- HPE OneView 5.00 API version: `1200`
- HPE OneView 5.20 API version: `1600`
- HPE OneView 5.30 API version: `1800`

### HPE Synergy Image Streamer

The OneView Python SDK also supports the API endpoints for HPE Synergy Image Streamer.
To configure the SDK, you must set the Image Streamer IP on the OneViewClient configuration,
either using the JSON configuration:

```json
"image_streamer_ip": "100.100.100.100"
```

OR using the Environment variable:

```bash
export ONEVIEWSDK_IMAGE_STREAMER_IP='100.100.100.100'
```

To create the ImageStreamerClient, you must call the `create_image_streamer_client`
method from the pre-existent OneViewClient instance. Through the created
ImageStreamerClient, you are able to access the API Clients of the
Image Streamer resources:

```python
image_streamer_client = oneview_client.create_image_streamer_client()

build_plans = image_streamer_client.build_plans.get_all()
```

You can find more usage examples in the folder ```/examples/image_streamer```

### OneView Connection Timeout
By default the system timeout is used when connecting to OneView.  If you want to change this,
then the timeout can be set by either:

1. Setting the appropriate environment variable:
```bash
export ONEVIEWSDK_CONNECTION_TIMEOUT='<connection time-out in seconds>'
```

2. Setting the time-out in the JSON configuration file using the following syntax:
```json
"timeout": <timeout in seconds>
```

## Exception handling

All exceptions raised by the OneView Python SDK inherit from HPEOneViewException.

**HPEOneViewException** has the following properties:
- **msg** - a string containing the error message sent by the OneView REST API;
- **oneview_response** - contains the entire JSON data dictionary with error details that are returned by the OneView Python SDK. It can be: ```None```.

##### Exception Handling example:

```python
try:
    fc_network_client = oneview_client.fc_networks
    fc_network = fc_network_client.get_by_name(name)
except HPEOneViewException as e:
    print(e.msg)
    if e.oneview_response:
    	pprint(e.oneview_response)
```

For compatibility purposes, the Exception args property is defined with the error arguments. For example:

```python
except Exception as e:
	print(arg[0]) # e.msg equivalent
    print(arg[1]) # e.oneview_reponse equivalent
```

## Contributing and feature requests

**Contributing:** You know the drill. Fork it, branch it, change it, commit it, and pull-request it. We are passionate about improving this project, and glad to accept help to make it better.

**NOTE:** We reserve the right to reject changes that we feel do not fit the scope of this project. For feature additions, please open an issue to discuss your ideas before doing the work.

**Feature Requests:** If you have needs not being met by the current implementation, please let us know (via a new issue). This feedback is crucial for us to deliver a useful product. Do not assume we have already thought of everything, because we assure you that is not the case.

#### Naming Convention for OneView Resources

The following summarizes code structure and naming conventions for the OneView resources.

- **Packages:** The package is named according to the **HPE OneView API Reference** group, with all characters in lowercase, replacing spaces with underscores.
- **Modules:** The module is named according to the **HPE OneView API Reference** endpoint title, with all characters in lowercase, replacing spaces with underscores.
    For example: In the documentation we have **FC Networks**, so the module name will be **fc_networks**.
- **Classes:** We are using camel case to define the class name, for example: **FcNetworks**.
- **OneViewClient properties:** In the **oneview_client**, the property name follows exactly the module name, for example: **fc_networks**.
- **Examples:** The example is named with the same name of the resource module: **fc_networks**.
- **Tests:**  The unit test folders follow the same structure of the resources. The name of the test modules should start with "test," for example: **test_fc_networks**.

#### Testing

When contributing code to this project, we require tests to accompany the code being delivered.
That ensures a higher standing of quality, and also helps to avoid minor mistakes and future regressions.

When writing the unit tests, the standard approach we follow is to use the python library [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) to patch all calls that would be made to a OneView appliance and return mocked values.

We have packaged everything required to verify if the code is passing the tests in a tox file.
The tox call runs all unit tests against Python 2 and 3, runs a flake8 validation, and generates the test coverage report.

To run it, use the following command:

```
$ tox
```

You can also check out examples of tests for different resources in the [tests](tests) folder.

## License

This project is licensed under the Apache license. Please see [LICENSE](LICENSE) for more information.

## Version and changes

To view history and notes for this version, view the [Changelog](CHANGELOG.md).
