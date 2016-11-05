import os
from app_config import AppConfig as ac
import subprocess

def create_video():
    count = 0
    num_frames_per_vid = 60
    images_folder = os.path.join(ac.CURRENT_PROJECT_PATH, "final_images")
    print(images_folder)
    videos_folder = os.path.join(ac.CURRENT_PROJECT_PATH, "final_videos")

    # Make the videos folder if it doesn't exists 
    # (images_folder will be created by move_images_to_project_dir_folder)
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)
    db_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")
    delete_videos("final_videos")

    while True:
        # Delete old images, and recreate them in the right place
        delete_images(images_folder)
        subprocess.call(["display-trajectories.py", "-i", ac.CURRENT_PROJECT_VIDEO_PATH,"-d", db_path, "-o", ac.CURRENT_PROJECT_PATH + "/homography/homography.txt", "-t", "object", "--save-images", "-f", str(count*num_frames_per_vid), "--last-frame", str((count + 1)*num_frames_per_vid - 1)])
        move_images_to_project_dir_folder(images_folder)
        
        # If we got to the end of the video, break
        if not images_exist(images_folder):
            print 'No more images'
            break

        # Get the frames, and create a short video out of them
        renumber_frames(images_folder, count*num_frames_per_vid)
        convert_frames_to_video(images_folder, videos_folder, "video-"+str(count)+".mp4")

        count += 1

    combine_videos(videos_folder, "final_videos")

def move_images_to_project_dir_folder(folder):
    images_folder = folder
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    for file in os.listdir(os.getcwd()):
        if file[0:6] == 'image-' and file[-4:] == '.png':
            os.rename(file, os.path.join(images_folder, file))


def convert_frames_to_video(images_folder, videos_folder, filename):
    subprocess.call(["ffmpeg", "-framerate", "30", "-i", os.path.join(images_folder, "image-%d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", os.path.join(videos_folder, filename)])

def delete_videos(folder):
    videos_folder = folder
    file_extensions = ['.mp4', '.mpg']

    for extension in file_extensions:
        if os.path.exists(videos_folder):
            for file in os.listdir(videos_folder):
                if file[0:6] == 'video-' and file[-4:] == extension:
                    os.remove(os.path.join(videos_folder, file))
                if file == 'output' + extension:
                    os.remove(os.path.join(videos_folder, file))
        for file in os.listdir(os.getcwd()):
            if file[0:6] == 'video-' and file[-4:] == extension:
                os.remove(os.path.join(os.getcwd(), file))
            if file == 'output' + extension:
                os.remove(os.path.join(videos_folder, file))

def delete_images(folder):
    images_folder = folder
    if os.path.exists(images_folder):
        for file in os.listdir(images_folder):
            if file[0:6] == 'image-' and file[-4:] == '.png':
                os.remove(os.path.join(images_folder, file))
    for file in os.listdir(os.getcwd()):
        if file[0:6] == 'image-' and file[-4:] == '.png':
            os.remove(os.path.join(os.getcwd(), file))

def move_videos_to_folder(folder):
    videos_folder = folder
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)
    for file in os.listdir(os.getcwd()):
        if file[0:6] == 'video-' and file[-4:] == '.mp4':
            os.rename(file, os.path.join(videos_folder, file))

def images_exist(folder):
    images_folder = folder
    if os.path.exists(images_folder):
        for file in os.listdir(images_folder):
            if file[0:6] == 'image-' and file[-4:] == '.png':
                return True
    return False

def combine_videos(folder, filename):
    # The only way I could find to join videos was to convert the videos to .mpg format, and then join them.
    # This seems to be the only way to keep ffmpeg happy.
    videos_folder = folder
    convert_to_mpeg(videos_folder)

    # Using Popen seems to be necessary in order to pipe the output of one into the other
    p1 = subprocess.Popen(['cat']+get_videos(videos_folder), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['ffmpeg', '-f', 'mpeg', '-i', '-', '-qscale', '0', '-vcodec', 'mpeg4', os.path.join(videos_folder, 'output.mp4')], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.

def convert_to_mpeg(folder):
    videos_folder = folder
    count = 0

    while os.path.exists(os.path.join(videos_folder, "video-"+str(count)+".mp4")):
        subprocess.call(['ffmpeg', '-i', os.path.join(videos_folder, 'video-'+str(count)+'.mp4'), '-qscale', '0', os.path.join(folder, "video-"+str(count)+".mpg")])
        count += 1

def get_videos(folder):
    videos_folder = folder
    count = 0
    videos = []

    while os.path.exists(os.path.join(videos_folder, "video-"+str(count)+".mpg")):
        videos.append(os.path.join(videos_folder, "video-"+str(count)+".mpg"))
        count += 1
    return videos


def renumber_frames(folder, frame):
    images_folder = folder
    print(images_folder)

    # Rename them all to 'new-image-x' in order to not interfere with the current 'image-x'
    for file in os.listdir(images_folder):
        if file[0:6] == 'image-' and file[-4:] == '.png':
            number = file[6:-4]
            new_number = int(number) - frame
            new_file = 'new-image-'+str(new_number)+'.png'
            os.rename(os.path.join(images_folder, file), os.path.join(images_folder, new_file))

    # Rename the 'new-image-x' to 'image-x'
    for file in os.listdir(images_folder):
        if file[0:10] == 'new-image-' and file[-4:] == '.png':
            new_file = file[4:]
            os.rename(os.path.join(images_folder, file), os.path.join(images_folder, new_file))


