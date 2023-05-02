# HPE OneView SDK for Python

## Build Status 

| OV Version | 8.30 | 8.20 | 8.10 | 8.00 | 7.20 | 7.10 | 7.00                                                                                                                                                                                    | 6.60                                                                                                                                                                                    | 6.50                                                                                                                                                                                    |                                                                                      6.40                                                                                       |                                                                                      6.30                                                                                       |                                                                                          6.20                                                                                          |                                                                                          6.10                                                                                          |                                                                                          6.00                                                                                          |                                                                                            5.60                                                                                            |
| ------------- |  ------------- |  ------------- |  ------------- |  ------------- |   --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |----------------------------------------------------------------------------: |
| SDK Version/Tag |[v8.3.0](https://github.com/HewlettPackard/oneview-python/releases/tag/8.3.0)|[v8.2.0](https://github.com/HewlettPackard/oneview-python/releases/tag/8.2.0)|[v8.1.0](https://github.com/HewlettPackard/oneview-python/releases/tag/8.1.0)|[v8.0.0](https://github.com/HewlettPackard/oneview-python/releases/tag/8.0.0)|[v7.2.0](https://github.com/HewlettPackard/oneview-python/releases/tag/7.2.0)|[v7.1.0](https://github.com/HewlettPackard/oneview-python/releases/tag/7.1.0)| [v7.0.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v7.0.0)                                                                                                          | [v6.6.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v6.6.0)                                                                                                          | [v6.5.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v6.5.0)                                                                                                          |                                                 [v6.4.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v6.4.0)                                                  |                                                 [v6.3.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v6.3.0)                                                  |                                                     [v6.2.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v6.2.0)                                                     |                                                     [v6.1.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v6.1.0)                                                     |                                                     [v6.0.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v6.0.0)                                                     |                                                       [v5.6.0](https://github.com/HewlettPackard/oneview-python/releases/tag/v5.6.0)                                                       |
| Build Status    | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/4800354967) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/4371621558) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/3626826357)| [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/3006374044) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/2675986741) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/2376290875) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/1967921808) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/1658469670) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/runs/4236699714) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/runs/3524286157) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/986745563) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/726148134) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/HewlettPackard/oneview-python/actions/runs/623585124) | [![Build status](https://github.com/HewlettPackard/oneview-python/actions/workflows/run_tests.yml/badge.svg)](https://travis-ci.com/github/HewlettPackard/oneview-python/builds/214352373) |

## Introduction

HPE OneView makes it simple to deploy and manage today’s complex hybrid cloud infrastructure. HPE OneView can help you transform your data center to software-defined, and it supports HPE’s broad portfolio of servers, storage, and networking solutions, ensuring the simple and automated management of your hybrid infrastructure. Software-defined intelligence enables a template-driven approach for deploying, provisioning, updating, and integrating compute, storage, and networking infrastructure.

The HPE OneView Python library provides a pure Python interface to the HPE OneView REST APIs. It depends on the [Python-Future](http://python-future.org/index.html) library to provide Python 2/3 compatibility.

You can find the latest supported HPE OneView Python SDK [here](https://github.com/HewlettPackard/oneview-python/releases/latest)

Refer to

Supported HPE OneView Python [APIs Implementation](https://github.com/HewlettPackard/oneview-python/blob/master/endpoints-support.md) and
Latest version of the OneView Python [SDK Documentation](https://hewlettpackard.github.io/oneview-python/index.html)

## What's New

HPE OneView Python library extends support of the SDK to OneView REST API version 5200 (OneView v8.30)
### Migration script
Perform migration from HPE OneView 6.x to HPE OneView 7.0 for non-Synergy appliance using below script.
```bash
   $ git clone https://github.com/HewlettPackard/oneview-python.git
   $ cd oneview-python/examples/migration/
   $ python migrate.py [<list of server hardwware names to be migrated>] 
```

Please refer to [notes](https://github.com/HewlettPackard/oneview-python/blob/master/CHANGELOG.md) for more information on the changes , features supported and issues fixed in this version

## Getting Started 

HPE OneView SDK for Python can be installed from Source,Pypi and Docker container installation methods.

   ## From Source
   ```bash
   $ git clone https://github.com/HewlettPackard/oneview-python.git
   $ cd oneview-python 
   ```
   ```python
   $ python setup.py install --user  # to install in the user directory (~/.local)
   ```
   ```bash
   $ sudo python setup.py install    # to install globally
   ```
   
   ## Or using PIP:
   ```bash
   $ git clone https://github.com/HewlettPackard/oneview-python.git 
   $ cd oneview-python 
   ```
   ```python
   $ pip install . 
   ```   
   
   ## From Pypi
   ```bash
   $ git clone https://github.com/HewlettPackard/oneview-python.git
   $ cd oneview-python 
   ```
   ```python
   $ pip install hpeOneView 
   ```
   
   ## From Docker Image / Container
   
   Clone this repo and cd into it:
   ```bash
   $ git clone https://github.com/HewlettPackard/oneview-python.git
   $ cd oneview-python
   ```
   
   # Build the docker image:
   ```bash
   $ docker build -t oneview-python . 
   ```
   Now you can run any of the example in this directory:
   Run the container, passing in your credentials to OneView and specifying which example recipe to run. <br />
   `-v`: The volume on which repo code is mounted <br />
   Replace `connection_templates` with the name of the example you'd like to run <br />
   Replace `pwd` with the path of the example file you'd like to run. <br />
   ```bash
   $ docker run -it --rm \ -v $(pwd)/:/root/oneview/ python examples/connection_templates.py
   ```
   
   ## Running Examples with published docker image
   We also provide a lightweight and easy way to test and run oneview-python. The hewlettpackardenterprise/hpe-oneview-sdk-for-python:<tag> docker image 
   contains an installation of oneview-python installation you can use by just pulling down the Docker Image:

   The Docker Store image tag consist of two sections: <sdk_version-OV_version>

   Download and store a local copy of hpe-oneview-sdk-for-python and use it as a Docker image. <br />
   ```bash

   $ docker pull hewlettpackardenterprise/hpe-oneview-sdk-for-python:v8.3.0-OV8.3
   ```

   Run docker commands and this will in turn create sh session where you can create files, issue commands and execute the tests <br />
   ```bash

   $ docker run -it hewlettpackardenterprise/hpe-oneview-sdk-for-python:v8.3.0-OV8.3 /bin/sh

   ```
   
## Configuration

  ### JSON: 
  Connection properties for accessing the OneView appliance can be set in a JSON file.
  Before running the samples or your own scripts, you must create the JSON file. An example can be found at: OneView configuration sample.

  Note: If you have an active and valid login session and want to use it, define the sessionID in the Credentials. When sessionID is defined, you can remove username 
  and password from your JSON (they will be disregarded anyway).

  Once you have created the JSON file, you can initialize the OneViewClient:

   ```python 
   from hpeOneView.oneview_client import OneViewClient
   oneview_client = OneViewClient.from_json_file('/path/config.json')
   ``` 
   
  :lock: Tip: Check the file permissions because the password is stored in clear-text.

  ### Environment Variables:
  Configuration can also be defined through environment variables:

  ### Required
  ```bash
  export ONEVIEWSDK_IP='172.16.102.82'
  export ONEVIEWSDK_USERNAME='Administrator'
  export ONEVIEWSDK_PASSWORD='secret123'
  ```
  Or sessionID 
  ```bash
   export ONEVIEWSDK_SESSIONID='123'
   ```
    
  Once you have defined the environment variables, you can initialize the OneViewClient using the following code snippet:

  ```python 
   from hpeOneView.oneview_client import OneViewClient
   oneview_client = OneViewClient.from_environment_variables()
   ```
  :lock: Tip: Make sure no unauthorized person has access to the environment variables, since the password is stored in clear-text.

  Note: If you have an active and valid login session and want to use it, define the ```ONEVIEWSDK_SESSIONID```. When a sessionID is defined, it will be used for 
  authentication (username and password will be ignored in this case).

  ### Dictionary:
  ```python
  # You can also set the configuration using a dictionary. As described above, for authentication you can use username/password:
  config = { 
    "ip": "172.16.102.82", 
    "credentials": { 
        "userName": "Administrator",
        "password": "secret123"
    }
  }
  ```
  
  ```python 
  #Or if you have an active and valid login session and want to use it, define the sessionID in the Credentials:
  config = {
    "ip": "172.16.102.82",
    "credentials": { 
        "sessionID": "123" 
    } 
  }
  ```

  ```python
  # If you need to use a proxy server, You can add the same in config dictionary as below:
  config = { 
    "ip": "172.16.102.82",
    "proxy": "1.2.3.4:8080",
    "credentials": {
        "userName": "Administrator",
        "password": "secret123"
    }
  }
  ```

  ```python 
   from hpeOneView.oneview_client import OneViewClient
   oneview_client = OneViewClient(config) 
   ```
  :lock: Tip: Check the file permissions because the password is stored in clear-text.


For more details on the Installation , Configuration , Logging , Troubleshooting refer to [WIKI# Installation & Configuration section](https://github.com/HewlettPackard/oneview-python/wiki#installation).

### HPE Synergy Image Streamer

From Release 8.1, Image streamer is no longer supported.

## Getting Help 

Are you running into a road block? Have an issue with unexpected bahriov? Feel free to open a new issue on the [issue tracker](https://github.com/HewlettPackard/oneview-python/issues)

For more information on how to open a new issue refer to [How can I get help & support](https://github.com/HewlettPackard/oneview-python/wiki#getting-help---how-can-i-get-help—support)

## License 

This project is licensed under the Apache license. Please see [LICENSE](https://github.com/HewlettPackard/oneview-python/blob/master/LICENSE) for more information.

## Additional Resources 

**HPE OneView Documentation**

[HPE OneView Release Notes](http://hpe.com/info/OneView/docs)

[HPE OneView Support Matrix](http://hpe.com/info/OneView/docs)

[HPE OneView Installation Guide](http://hpe.com/info/OneView/docs)

[HPE OneView User Guide](http://hpe.com/info/OneView/docs)

[HPE OneView Online Help](http://hpe.com/info/OneView/docs)

[HPE OneView REST API Reference](http://hpe.com/info/OneView/docs)

[HPE OneView Firmware Management White Paper](http://hpe.com/info/OneView/docs)

[HPE OneView Deployment and Management White Paper](http://hpe.com/info/OneView/docs)


**HPE OneView Community**

[HPE OneView Community Forums](http://hpe.com/info/oneviewcommunity)

Learn more about HPE OneView at [hpe.com/info/oneview](https://hpe.com/info/oneview)


