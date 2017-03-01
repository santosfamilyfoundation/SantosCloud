# SantosCloud

SantosCloud is an API that allows users to perform analysis on videos of traffic intersections in order to produce safety statistics to enable infrastructure change that could save lives. SantosCloud provides an API that enables users to upload their videos, analyze it, and retrieve a safety report outlining the details of the intersection.

SantosCloud's analysis is performed by the excellent [TrafficIntelligence project](https://bitbucket.org/Nicolas/trafficintelligence/wiki/Home). Many thanks to Dr. Nicolas Saunier for his work on that project and collaboration with us on this project.

All of the instructions in this README apply to Ubuntu operating systems. This is the only currently supported OS for running SantosCloud.

## Table of Contents

- [Setup](#setup)
- [Running](#running)
- [API Documentation](#api-documentation)

## Setup

### Installation

There are two options:

#### Vagrant Installation

For installation of the complete environment that you will need to run SantosCloud, see the instructions in the [README of the SantosInstallation repository](https://github.com/santosfamilyfoundation/SantosInstallation). Once you do this, 

#### Local Installation

As of now, instructions for local installation are still a work-in-progress. Basically, you will need to clone this repository onto your computer and install TrafficIntelligence. We are in the process of providing clean installation instructions for TrafficIntelligence.

### Environment Setup

Either way that you install SantosCloud and TrafficIntelligence, you will have to perform some steps to set up the environment for running the server.

To use the project, you must add the SantosCloud folder to your PYTHONPATH environment variable. On Ubuntu, this means adding the following line to your `.bashrc`:

```
export PYTHONPATH="${PYTHONPATH}:/home/$USER/Documents/SantosCloud"
```

(This example is if your SantosCloud repo lives in `~/Documents/`)

A simple way to do this is by using `vim ~/.bashrc` or `nano ~/.bashrc` and then running `source ~/.bashrc` or restarting your terminal.

You need also set environment variables for the secret key, and you can optionally set environment variables for the server to email users on long-running analysis tasks. 

You can generate a secret key by running the following python commands:

```
import os
os.urandom(24).encode('hex')
```

Run the following commands to set the secret key (this is required). Paste the secret key from the step above.

```
export SANTOSCLOUD_SECRET_KEY="ExampleSecretKey"
```

Run the following commands to set the variables the server needs for email capabilities (this is optional):

```
export SANTOSCLOUD_EMAIL="santostrafficcloud@gmail.com"
export SANTOSCLOUD_EMAIL_PASSWORD="ExamplePassword"
```

The email feature has only been tested with Gmail emails. If you install this locally, you can create a Gmail or use yours to send emails from when the analysis completes.

You can add the commands to your `.bashrc` file in order to have these environment variables set for every shell that you open. Again, you can use `vim ~/.bashrc` or `nano ~/.bashrc` and then run `source ~/.bashrc` or restart your terminal to set these variables.

## Running

To run the server, either 1) run `python app/app.py` from the SantosCloud folder, or 2) `cd` into the `app/` folder and run `python app.py`. This will start the server.

## API Documentation

### Install `npm` and `apidoc`

To install `apidoc` in order to update the documentation, you must install npm. To install npm on Ubuntu/Debian systems, follow these steps:

1. Run `curl -sL https://deb.nodesource.com/setup_4.x | sudo bash -` (install curl with `sudo apt-get install curl` if needed)
2. Run `sudo apt-get install -y nodejs` and `sudo apt-get install -y build-essential`.
3. Run `node -v` and `npm -v` in a shell and ensure that node's version is greater than 0.10.35 and npm's version is greater than 2.1.17.
4. If npm is out of date run `sudo npm install -g npm`
5. Run `sudo npm install apidoc -g`.

### Regenerating the Documentation

To regenerate the API Documentation, please run the following command from the SantosCloud folder:

```
apidoc -f ".*\\.py$" apidoc -i app/handlers/ -o app/static/apidoc
```

### Viewing the Documentation

Navigate to the IP of the server and the path `/static/apidoc/index.html`. (For example, `localhost:8888/static/apidoc/index.html`).

