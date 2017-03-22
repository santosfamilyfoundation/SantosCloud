import os
import subprocess
import json
import matplotlib.pyplot as plt

import cv2
from numpy.linalg.linalg import inv
from numpy import loadtxt

from moving import userTypeNames
from storage import loadTrajectoriesFromSqlite
from cvutils import cvPlot, cvColors, cvGreen, imageBox

tracking_filename = "tracking.mp4"
highlight_filename = "highlight.mp4"

def create_tracking_video(project_path, video_path):
    db_filename = os.path.join(project_path, 'run', 'results.sqlite')
    homography_path = os.path.join(project_path, 'homography', 'homography.txt')
    output_path = os.path.join(project_path, 'final_videos', tracking_filename)

    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)

    create_trajectory_video(video_path, db_filename, homography_path, output_path)

def create_highlight_video(project_path, video_path, list_of_near_misses):
    videos_folder = os.path.join(project_path, "final_videos")
    temp_video_prefix = "temp_highlight_video-"

    # Make the videos folder if it doesn't exists
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)

    delete_files(videos_folder, excluded_files=[tracking_filename])

    # Slow down by 3x for highlight video
    output_framerate = get_framerate(video_path) / 3.0
    upper_frame_limit = get_number_of_frames(video_path)

    for i, near_miss in enumerate(list_of_near_misses):
        start_frame, end_frame, object_id1, object_id2 = near_miss

        # Create a short video snippet of the near miss interaction
        snippet_number = 2*i + 1
        print [object_id1, object_id2]

        # Create a short tracking video
        create_trajectory_video(video_path, db_filename, homography_path, output_path, first_frame=max(0, start_frame-30), last_frame=min(upper_frame_limit, end_frame+30), objects_to_label=[object_id1, object_id2], framerate=output_framerate)

        # Get resolution of video
        snippet_path = os.path.join(videos_folder, temp_video_prefix + str(snippet_number) + ".mpg")
        width, height = get_resolution(snippet_path)

        # create title slide image
        slide_number = 2*i
        slide_name = temp_video_prefix + str(slide_number)
        slide_path = os.path.join(videos_folder, slide_name+'.png')
        create_title_slide(width, height, slide_path, object_id1, object_id2)

        # create title slide video
        create_video_from_image(videos_folder, slide_name+'.png', slide_name+'.mp4', output_framerate, 5)

    files = get_list_of_files(videos_folder, temp_video_prefix, 'mp4')
    combine_videos(files, highlight_filename)
    delete_files(videos_folder, temp_video_prefix, ["mpg", "mp4", "png"], excluded_files=[tracking_filename, highlight_filename])

## Helpers -- Internal use

def get_video_writer(output_path, framerate, width, height):
    video_extension = output_path.split('.')[-1]
    if video_extension == 'mp4':
        codec = 'MP4V'
    else:
        codec = 'DIVX'

    fourcc = cv2.cv.CV_FOURCC(*codec)
    writer = cv2.VideoWriter(output_path, fourcc, framerate, (width, height), True)

    return writer

def create_trajectory_video(video_path, db_filename, homography_path, output_path, first_frame=0, last_frame=None, video_type='object', objects_to_label=None, bounding_boxes=False, framerate=None):
    '''
    Creates a video of tracked trajectories.

    video_path: a path to the video on which to overlay
    db_filename: path to the database of tracked objects and features
    homography_path: the path to the homography.txt of the project
    output_path: The path of the video to be created. Please be sure that the output video format works on your system! (mp4 doesn't work on Windows AFAIK)
    first_frame: frame to start at
    last_frame: frame to end at
    video_type: either 'object' or 'feature'
    bounding_boxes: boolean indicating whether to show bounding boxes for objects
    '''
    capture = cv2.VideoCapture(video_path)
    width = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, first_frame)
    frame_num = first_frame

    if framerate is None:
        framerate = get_framerate(video_path)

    print('Loading objects, please wait...')
    objects = loadTrajectoriesFromSqlite(db_filename, video_type, withFeatures=bounding_boxes)
    homography = inv(loadtxt(homography_path))

    ret = True
    objectToDeleteIds = []

    out = get_video_writer(output_path, framerate, width, height)

    while ret:
        if last_frame is not None and frame_num > last_frame:
            break

        ret, img = capture.read()
        if ret:
            if frame_num % 100 == 0:
                print('frame {0}'.format(frame_num))

            if len(objectToDeleteIds) > 0:
                objects = [o for o in objects if o.getNum() not in objectToDeleteIds]
                objectToDeleteIds = []

            # plot objects
            for obj in objects:
                if obj.existsAtInstant(frame_num):
                    # Only draw for objects that should be labeled, if passed in
                    if objects_to_label is not None and obj not in objects_to_label:
                        continue

                    if obj.getLastInstant() == frame_num:
                        objectToDeleteIds.append(obj.getNum())

                    # Project the positions with homography
                    if not hasattr(obj, 'projectedPositions'):
                        obj.projectedPositions = obj.positions.project(homography)

                    # Plot it's trajectory until now
                    cvPlot(img, obj.projectedPositions, cvColors[obj.getNum()], frame_num-obj.getFirstInstant())

                    # Plot the object's bounds if it has features
                    if obj.hasFeatures():
                        imgcrop, yCropMin, yCropMax, xCropMin, xCropMax = imageBox(img, obj, frame_num, homography, width, height)
                        cv2.rectangle(img, (xCropMin, yCropMin), (xCropMax, yCropMax), cvGreen, 1)

                    # Put object id and type if it's an object video
                    # If it's a feature video, there's too many numbers, let's ignore it.
                    if video_type == 'object':
                        objDescription = '{} '.format(obj.num)
                        if userTypeNames[obj.userType] != 'unknown':
                            objDescription += userTypeNames[obj.userType][0].upper()
                        cv2.putText(img, objDescription, obj.projectedPositions[frame_num-obj.getFirstInstant()].asint().astuple(), cv2.FONT_HERSHEY_PLAIN, 3, cvColors[obj.getNum()], thickness=4)

            # Write image
            out.write(img)

            frame_num += 1

    capture.release()
    out.release()
    cv2.destroyAllWindows()

def combine_videos(videos_list, output_path):
    video_index = 0
    capture = cv2.VideoCapture(videos_list[video_index])
    width = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    output_path = os.path.join(videos_folder, filename)
    out = get_video_writer(output_path, framerate, width, height)

    ret = True
    while ret:
        ret, frame = cap.read()
        if ret:
            print "end of video " + str(video_index) + " .. next one now"
            video_index += 1
            if video_index >= len(videos_list):
                break
            cap = cv2.VideoCapture(videos_list[video_index])
            ret, frame = cap.read()

        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def create_video_from_image(folder, image_filename, video_filename, framerate, duration):
    print('Creating video from image')
    input_path = os.path.join(folder, image_filename)
    output_path = os.path.join(folder, video_filename)

    video_index = 0
    capture = cv2.VideoCapture(videos_list[video_index])
    width = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    image = cv2.imread(input_path)
    out = get_video_writer(output_path, framerate, width, height)

    for i in range(framerate * duration):
        out.write(image)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

## File helpers

def delete_files(folder, prefix="", extensions=[], excluded_files=[]):
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.startswith(prefix):
                s = file.split('.')
                has_extension = len(s) == 2
                extension_included = True

                # If it has an extension, don't delete it if it doesn't have an extension provided
                if has_extension:
                    e = s[1]
                    if len(extensions) > 0 and e not in extensions:
                        extension_included = False

                # If it has an extension that should be deleted (or extensions don't exist), and not in excluded files, delete it
                if extension_included:
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
    """ fast cmdline way to get # of frames taken from
    http://stackoverflow.com/questions/2017843/fetch-frame-count-with-ffmpeg#comment-72336543
    """
    if os.path.exists(videopath):
        cmd = "ffmpeg -i %s -vcodec copy -acodec copy -f null /dev/null 2>&1 | grep -Eo 'frame= *[0-9]+ *' | grep -Eo '[0-9]+' | tail -1" % videopath
        num = subprocess.check_output(cmd, shell=True)
        return num

def get_framerate(videopath):
    list_o = str(subprocess.check_output(["ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=avg_frame_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        videopath]))
    return float(list_o.strip().split('/')[0])/float(list_o.strip().split('/')[1])

def get_resolution(videopath):
    """
    Returns
    -------

    (width, height) in number of pixels
    """
    capture = cv2.VideoCapture(videopath)
    width = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    return (width, height)

#### Video Creation

def create_title_slide(width, height, save_path, object_id1, object_id2, fontsize=None, textcolor='#FFFFFF', facecolor='#000000'):
    """
    width: int, width in pixels of desired output
    height: int, pixel height of desired output

    Note: fontsize varies with the resolution of the video in a very dumb manner right now.
    If you want to control fontsize, provide it as a parameter
    """
    # heights and widths in matplotlib are units of inches, not pixels
    dpi = 100.0
    mpl_width = width / dpi
    mpl_height = height / dpi

    # make figure without frame
    fig = plt.figure(frameon=False)
    fig.set_size_inches(mpl_width, mpl_height)
    ax = fig.add_subplot(111)

    # hide axis
    ax.set_axis_off()

    # set your axis size
    ax.axis([0, mpl_width, 0, mpl_height])

    # 20 is a good font size for a 400 height image...
    # 40 is a good font size for a 800 height image
    if not fontsize:
        fontsize = height / 20

    ax.text(0.2*mpl_width, 0.75*mpl_height, 'Near Miss between', style='italic', fontsize=fontsize, color=textcolor)
    ax.text(0.2*mpl_width, 0.6*mpl_height, 'Object {}'.format(object_id1), fontsize=fontsize, color=textcolor)
    ax.text(0.2*mpl_width, 0.4*mpl_height, 'Object {}'.format(object_id2), fontsize=fontsize, color=textcolor)

    fig.savefig(save_path, dpi=dpi, bbox_inches=0, pad_inches=0, facecolor=facecolor)
