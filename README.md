# TrafficCloud
Our API wrapper around TrafficIntelligence. It's video analysis, *in the cloud*.

### Setup

To use the project, you must add the TrafficCloud folder to your PYTHONPATH environment variable. On Ubuntu, this means adding the following line to your `.bashrc`:

```
export PYTHONPATH="${PYTHONPATH}:/home/$USER/Documents/TrafficCloud"
```

(This example is if your TrafficCloud repo lives in `~/Documents/`)

A simple way to do this is by using `vim ~/.bashrc` or `nano ~/.bashrc` and then running `source ~/.bashrc` or restarting your terminal.

You must also set environment variables for the secret key, email, and the password for the email. Run the following commands to set these environment variables:

```
export TRAFFICCLOUD_SECRET_KEY="ExampleSecretKey"
export TRAFFICCLOUD_EMAIL="santostrafficcloud@gmail.com"
export TRAFFICCLOUD_PASSWORD="ExamplePassword"
```

You can generate a secret key by running the following python commands:

```
import os
os.urandom(24).encode('hex')
```

### Running

Running `python main.py <project_name>` from the TrafficCloud folder will run the analysis on the project. `<project_name>` can either be the folder name or the relative or absolute path to the folder from the TrafficCloud folder (i.e. for a project with id of 'id', this can be `python main.py id`, `python main.py project_dir/id/` or `python main.py /home/username/TrafficCloud/project_dir/id/`). This assumes that the project folder exists in `TrafficCloud/project_dir/` and contains all of the necessary config and video files.

To run the server, either 1) run `python app/app.py` from the TrafficCloud folder, or 2) `cd` into the `app/` folder and run `python app.py`. These will start the server and tell you what port it is running on.

### Generate API Documentation

#### Install `apidoc`

To install `apidoc` in order to update the documentation, you must install npm. To install npm on Ubuntu/Debian systems, follow these steps:

1. Run `curl -sL https://deb.nodesource.com/setup_4.x | sudo bash -` (install curl with `sudo apt-get install curl` if needed)
2. Run `sudo apt-get install -y nodejs` and `sudo apt-get install -y build-essential`.
3. Run `node -v` and `npm -v` in a shell and ensure that node's version is greater than 0.10.35 and npm's version is greater than 2.1.17.
4. If npm is out of date run `sudo npm install -g npm`
5. Run `sudo npm install apidoc -g`.

#### Regenerating the Documentation

To regenerate the API Documentation, please run the following command from the SantosCloud folder:

```
apidoc -f ".*\\.py$" apidoc -i app/handlers/ -o app/static/apidoc
```

#### Viewing the Documentation

Navigate to the IP (localhost:8888 for local installation) and the path `/static/apidoc/index.html`. (For example, `localhost:8888/static/apidoc/index.html`).

