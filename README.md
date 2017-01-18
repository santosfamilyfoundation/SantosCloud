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

The email feature has only been tested with Gmail emails. If you install this locally, you can create a Gmail or use yours to send emails from when the analysis completes.

You can generate a secret key by running the following python commands:

```
import os
os.urandom(24).encode('hex')
```

### Running

Running `python main.py <project_name>` from the TrafficCloud folder will run the analysis on the project. `<project_name>` can either be the folder name or the relative or absolute path to the folder from the TrafficCloud folder (i.e. for a project with id of 'id', this can be `python main.py id`, `python main.py project_dir/id/` or `python main.py /home/username/TrafficCloud/project_dir/id/`). This assumes that the project folder exists in `TrafficCloud/project_dir/` and contains all of the necessary config and video files.

To run the server, either 1) run `python app/app.py` from the TrafficCloud folder, or 2) `cd` into the `app/` folder and run `python app.py`. These will start the server and tell you what port it is running on.

