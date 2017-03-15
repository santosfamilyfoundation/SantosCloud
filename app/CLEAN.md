

# To clean the database

## Project Creation

### Using GUI

Create a project using the GUI. Go through every step through configuring the project (but don't run analysis!).

Go into `~/Documents/SantosGUI/project_dir/*your_project_name*` and open `config.cfg`. Look for identifier and write it down. It should look like `abae7d1a-d726-4171-807f-964c46e36f09`.

### Using script

Create a project using `test_cloud.py` in the `SantosGUI` repository. First, edit the file to not run any analysis or results functions on the projects. Note the identifier of the created project.

## Run object tracking

Run object tracking on the video. In a SantosGUI repository, go into the `application` folder, and run the following:

```
$ python
> import cloud_api as api
> remote = api.CloudWizard('localhost')
> remote.objectTracking('*your_identifier_here*','*your_email_here*')
```

Use an email to be notified when object tracking is done, or use None, and just watch when the server has finished.

## Create tracking video

On the server, cd into SantosCloud/app/traffic_cloud_utils. Run:

```
from video import create_tracking_video
from app_config import get_project_path
identifier = '*your_identifier_here'
project_path = get_project_path(identifier)
video_path = get_project_video_path(identifier)
create_tracking_video(project_path, video_path)
```

## Obtain tracking video

### Install vagrant-scp

To install, run:

```
vagrant plugin install vagrant-scp
```

### Get the file using scp

```
$ vagrant scp default-virtualbox:~/SantosCloud/project_dir/*your_identifier_here*/final_videos/tracking.mp4 .
```

This will copy the video to your current directory.

## Cleanup

Start the `clean.py` script on the server by navigating to `~/SantosCloud/app` and executing `python clean.py *your_identifier_here*`.

Open the video on your computer and begin watching it.

Once opened, press Enter on the server to begin cleaning.

Then, watch for three things:

### Deleting object tracked twice

Find the object id of one of the trajectories you would like to delete, and enter `D*object_id*` on the server. You can delete multiple tracked objects also, for example `D12,14,16`.

### Merging two objects

To merge two objects (i.e. if a pedestrian is tracked as a different object after walking behind an object), use the command `M*object_1*,*object_2*`, like `M12,15`.

### Changing object type

If an object is classified incorrectly, enter `C*object_id*,*object_type*`. For example, to change objects 14 and 16 to a car, run `C14,16,C`.


