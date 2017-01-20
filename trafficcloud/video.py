import os
from app_config import AppConfig as ac
import subprocess

tracking_filename = "tracking.mp4"
highlight_filename = "highlight.mp4"

def create_tracking_video():
    videos_folder = os.path.join(ac.CURRENT_PROJECT_PATH, "final_videos")
    temp_video_prefix = "temp_tracking_video-"

    count = 0
    num_frames_per_vid = 60
    num_frames = get_number_of_frames(ac.CURRENT_PROJECT_VIDEO_PATH)

    # Make the videos folder if it doesn't exists 
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)

    delete_files(videos_folder, excluded_files=[highlight_filename])

    # Create a bunch of short videos ("snippets")
    while num_frames_per_vid * count < num_frames:
        create_video_snippet(videos_folder, temp_video_prefix, count, count*num_frames_per_vid, (count + 1)*num_frames_per_vid - 1)
        count += 1

    combine_videos(videos_folder, temp_video_prefix, tracking_filename)
    delete_files(videos_folder, temp_video_prefix, ["mpg", "mp4"], excluded_files=[tracking_filename, highlight_filename])

def create_highlight_video(list_of_near_misses):
    videos_folder = os.path.join(ac.CURRENT_PROJECT_PATH, "final_videos")
    temp_video_prefix = "temp_highlight_video-"

    # Make the videos folder if it doesn't exists 
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)

    delete_files(videos_folder, excluded_files=[tracking_filename])

    # Create a bunch of short videos ("snippets")
    for i, near_miss in enumerate(list_of_near_misses):
        create_video_snippet(videos_folder, temp_video_prefix, i, near_miss[0], near_miss[1])

    combine_videos(videos_folder, temp_video_prefix, highlight_filename)
    delete_files(videos_folder, temp_video_prefix, ["mpg", "mp4"], excluded_files=[tracking_filename, highlight_filename])

## Helpers -- Internal use

def move_files_to_folder(from_folder, to_folder, prefix, extensions):
    if not os.path.exists(to_folder):
        os.makedirs(to_folder)
    for file in os.listdir(from_folder):
        if file.startswith(prefix):
            s = file.split('.')
            if len(s) == 2:
                e = s[1]
                # Then check extension is correct
                if e in extensions:
                    os.rename(os.path.join(from_folder, file), os.path.join(to_folder, file))

def delete_files(folder, prefix="", extensions=[], excluded_files=[]):
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.startswith(prefix):
                s = file.split('.')
                if len(s) == 2:
                    e = s[1]
                    # Then check extension is correct
                    if len(extensions) == 0 or e in extensions:
                        if not file in excluded_files:
                            os.remove(os.path.join(folder, file))

def get_list_of_files(folder, prefix, extension):
    count = 0
    files = []

    while os.path.exists(os.path.join(folder, prefix+str(count)+"."+extension)):
        files.append(os.path.join(folder, prefix+str(count)+"."+extension))
        count += 1

    return files

### Video Helpers

#### Video Metadata

def get_number_of_frames(videopath):
    num = int(subprocess.check_output(["ffprobe",
        "-v", "error",
        "-count_frames",
        "-select_streams", "v:0", 
        "-show_entries", "stream=nb_read_frames", 
        "-of", "default=nokey=1:noprint_wrappers=1", 
        videopath]))
    return num

def get_framerate(videopath):
    list_o = str(subprocess.check_output(["ffprobe",
        "-v", "error", 
        "-select_streams", "v:0", 
        "-show_entries", "stream=avg_frame_rate", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        videopath]))
    return str(int(list_o.strip().split('/')[0])/float(list_o.strip().split('/')[1]))

#### Video Creation

def create_video_snippet(videos_folder, file_prefix, video_number, start_frame, end_frame):
    images_folder = os.path.join(ac.CURRENT_PROJECT_PATH, "temp_images")
    db_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")
    temp_image_prefix = "image-"

    # Make the images folder if it doesn't exists 
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Delete old images, and recreate them in the right place
    delete_files(images_folder, temp_image_prefix, ["png"], excluded_files=[tracking_filename, highlight_filename])
    subprocess.call(["display-trajectories.py", "-i", ac.CURRENT_PROJECT_VIDEO_PATH,"-d", db_path, "-o", ac.CURRENT_PROJECT_PATH + "/homography/homography.txt", "-t", "object", "--save-images", "-f", str(start_frame), "--last-frame", str(end_frame)])
    move_files_to_folder(os.getcwd(), images_folder, temp_image_prefix, ["png"])

    # Get the frames, and create a short video out of them
    renumber_frames(images_folder, start_frame, temp_image_prefix, "png")
    convert_frames_to_video(images_folder, videos_folder, temp_image_prefix, file_prefix + str(video_number) + ".mpg")

def combine_videos(videos_folder, temp_video_prefix, filename):
    # The only way I could find to join videos was to convert the videos to .mpg format, and then join them.
    # This seems to be the only way to keep ffmpeg happy.

    # Using Popen seems to be necessary in order to pipe the output of one into the other
    p1 = subprocess.Popen(['cat']+get_list_of_files(videos_folder, temp_video_prefix, "mpg"), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['ffmpeg', 
        '-f', 'mpeg', 
        '-i', '-', 
        '-qscale', '0', 
        '-vcodec', 'mpeg4', 
        os.path.join(videos_folder, filename)], stdin=p1.stdout, stdout=subprocess.PIPE)

    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    p2.wait()

### Images Helpers

def renumber_frames(folder, start_frame, prefix, extension):
    temp_folder = os.path.join(folder, "temp")
    # Make the temp folder if it doesn't exists 
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Rename them all to 'new-image-x' in order to not interfere with the current 'image-x'
    for file in os.listdir(folder):
        if file.startswith(prefix):
            rest = file[len(prefix):]
            s = rest.split('.')
            if len(s) == 2:
                e = s[1]
                if e == extension:
                    number = rest.split('.')[0]
                    try:
                        num = int(number) - start_frame
                    except:
                        print("Couldn't parse to int: "+file+" from prefix: "+prefix)
                    if num < 0:
                        raise Error()
                    new_file = prefix+str(num)+'.'+extension
                    os.rename(os.path.join(folder, file), os.path.join(temp_folder, new_file))

    # Rename the 'new-image-x' to 'image-x'
    for file in os.listdir(temp_folder):
        os.rename(os.path.join(temp_folder, file), os.path.join(folder, file))

    os.removedirs(temp_folder)

def convert_frames_to_video(images_folder, videos_folder, images_prefix, filename):
    subprocess.call(["ffmpeg", 
        "-framerate", get_framerate(ac.CURRENT_PROJECT_VIDEO_PATH), 
        "-i", os.path.join(images_folder, images_prefix+"%d.png"), 
        "-c:v", "libx264", 
        "-pix_fmt", "yuv420p", 
        os.path.join(videos_folder, filename)])


