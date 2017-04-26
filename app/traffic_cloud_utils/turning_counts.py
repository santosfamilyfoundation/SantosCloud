
import sqlite3
import math
from sklearn.cluster import k_means

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import numpy as np
from numpy.linalg.linalg import inv
from numpy import loadtxt
import matplotlib.pyplot as plt

from moving import Point

def get_objects_with_trajectory(obj_to_heading, turn=None, initial_heading=None, final_heading=None):
    '''
    Returns all objects matching the given parameters, i.e. with the headings or turning motion
    specified by the arguments. Takes a dictionary of objects to headings, such as:
    {1:('Right, 'Down'), 2:('Left','Left')}
    '''
    directions = ["right", "down", "left", "up"]

    objs = []
    for (i, headings) in obj_to_heading.iteritems():
        if initial_heading is not None and headings[0].lower() != initial_heading.lower():
            continue

        if final_heading is not None and headings[1].lower() != final_heading.lower():
            continue

        if turn is not None:
            initial_index = directions.index(headings[0].lower())
            final_index = directions.index(headings[1].lower())
            if turn.lower() == "left" and (final_index + 1) % len(directions) != initial_index:
                continue

            if turn.lower() == "right" and (initial_index + 1) % len(directions) != final_index:
                continue

            if turn.lower() == "straight" and initial_index != final_index:
                continue

        objs.append(i)

    return objs


def trajectory_headings(db_filename, homography_file):
    """
    Returns a dictionary from object id to a tuple representing the object's initial and final headings.
    For example, {1:('Left','Up')} means that object 1 was heading left initially, and then turned right
    and headed up.
    """
    homography = inv(loadtxt(homography_file))

    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    queryStatement = 'SELECT * FROM object_trajectories ORDER BY object_id, frame'
    cursor.execute(queryStatement)

    obj_id = 0
    obj_traj = []
    trajectories = []

    for row in cursor:
        if(row[0] != obj_id):
            trajectories.append(obj_traj)
            obj_id = row[0]
            obj_traj = []

        pos = Point(row[2], row[3])

        pos = pos.project(homography)
        obj_traj.append((pos.x[0], pos.y[0]))

    trajectories.append(obj_traj)

    geometry = intersection_geometry(trajectories)

    d = {}
    for i in range(len(trajectories)):
        d[i] = classify_trajectory(trajectories[i], geometry)

    return d

def categorize_trajectory(trajectory):
    num_categories = 10
    # Look at velocity in first and last second
    interval = 15
    stride = (len(trajectory) - interval) / (num_categories - 1)

    vels = []
    for i in range(num_categories):
        start = stride * i
        end = start + interval - 1
        if end > len(trajectory):
            end = len(trajectory) - 1

        startpoint = trajectory[end]
        endpoint = trajectory[start]
        x_vel = endpoint[0] - startpoint[0]
        y_vel = endpoint[1] - startpoint[1]
        speed = math.sqrt(x_vel**2 + y_vel**2)

        vels.append(x_vel / speed)
        vels.append(y_vel / speed)

    return vels

def cluster_trajectories(trajectories):
    vels = None

    for t in trajectories:
        v = np.array(categorize_trajectory(t)).reshape(-1, 1).T
        if vels is None:
            vels = v
        else:
            vels = np.concatenate((vels, v))

    res = k_means(vels, 10)
    # centroids, labels
    return (res[0], res[1])

def draw_clusters(trajectories, labels, centroids=None):
    alpha = 0.22
    colors = [(0, 0, 0, alpha), (0, 0, 1, alpha), (0, 1, 0, alpha), (1, 0, 0, alpha), (0, 1, 1, alpha), (1, 1, 0, alpha), (1, 0, 1, alpha), (.2,.2,.2,alpha), (.5,.5,.5,alpha), (.5,.5,0,alpha),(0,.5,.5,alpha),(.5,0,.5,alpha)]

    dpi = 100.0
    mpl_width, mpl_height = (10, 8)

    for j in range(12):
        # make figure without frame
        fig = plt.figure(frameon=False)
        fig.set_size_inches(mpl_width, mpl_height)
        ax = fig.add_subplot(111)

        for i in range(len(labels)):
            label = labels[i]
            if label == j:
                xs = []
                ys = []
                for t in trajectories[i]:
                    xs.append(t[0])
                    ys.append(t[1])
                ax.plot(xs, ys, ".", color=colors[label], linewidth=2, markersize=3)
            if centroids is not None:
                centroid = centroids[label]
                xs = []
                ys = []
                for i in range(len(centroid)):
                    if i % 2 == 0:
                        xs.append(centroid[i])
                    else:
                        ys.append(centroid[i])
                ax.plot(xs, ys, ".", color=(0,0,0,1), linewidth=2, markersize=3)

        fig.savefig('here'+str(j)+'.png', dpi=dpi, bbox_inches=0, pad_inches=0, format='png')
        plt.close()

def intersection_geometry(trajectories):
    '''
    Returns the geometry of the intersection as a 2-tuple. The tuple will contain the angle of the 'Right'
    direction in the intersection and the 'Down' angle in the intersection. Assumes that the intersection
    is the intersection of two straight roads.

    This function works by finding large clusters that contain objects traveling very straight (i.e. low
    variance among their angle heading), and finding the angles for those clusters.
    '''
    _, labels = cluster_trajectories(trajectories)

    num_samples = 5
    interval = 10
    clusters = []

    # diff_dict holds a dict of {cluster_id:[diff_from_start_angle]}
    # average_dict is a dict of {cluster_id:[average_object_angle]}
    diff_dict = {}
    average_dict = {}

    for i in range(len(trajectories)):
        label = labels[i]

        # If we haven't seen this label, create its arrays, and keep track of how many clusters there are
        if label not in clusters:
            diff_dict[label] = np.array([])
            average_dict[label] = np.array([])
            clusters.append(label)

        t = trajectories[i]

        # Sample the trajectory some number of times, constructing a list that contains the difference
        # in an object's heading, and a list of the angle at each moment
        diff_arr = []
        angle_arr = []
        samples = get_sample_tuples(len(t), num_samples, interval)
        for sample in samples:
            avg_vel = average_velocity(t, sample[0], sample[1])
            angle = math.atan2(avg_vel[1], avg_vel[0])
            angle_arr.append(angle)

            diff = angle_difference(angle_arr[0], angle)

            diff_arr.append(diff)

        # Add the heading diffs to the right list for the cluster, in order to find the straightest
        # trajectory later
        diff_dict[label] = np.concatenate((diff_dict[label], diff_arr))

        # Also keep track of what the angles for all the objects in the cluster were, to find
        # the average angle for the cluster later
        average_angle = normalize_angle(angle_arr[0] + sum(diff_arr) / len(diff_arr))
        average_dict[label] = np.append(average_dict[label], average_angle)

    # Iterate through clusters, finding the variance, number of objects, and average angle for each
    o = []
    for i in clusters:
        angles = average_dict[i]

        diff_arr = []
        for j in range(len(angles)):
            diff_arr.append(angle_difference(angles[0], angles[j]))

        average_angle = angles[0] + sum(diff_arr) / len(diff_arr)

        arr = diff_dict[i]
        o.append((i, np.var(arr), len(arr) / num_samples, average_angle))

    # Sort by variance to find the straightest trajectories
    o = sorted(o, key=lambda x: x[1])

    # Finds the two best objects, by iterating through the options with the least variance (i.e. straight
    # trajectories), ensuring that the cluster is large enough to be significant, and then ensuring that
    # the two angles are different
    best_guesses = []
    min_objects = 5
    for i in range(len(o)):
        cluster_info = o[i]
        if cluster_info[2] >= min_objects:
            angle = cluster_info[3]
            if len(best_guesses) == 0:
                best_guesses.append(angle)
            elif len(best_guesses) == 1:
                best = best_guesses[0]
                is_similar = similar_angles(best, angle) or similar_angles(best, opposite_angle(angle))
                if not is_similar:
                    best_guesses.append(angle)

    return get_correct_geometry(best_guesses)

def get_sample_tuples(length, samples, interval):
    '''
    Returns a list of tuples representing start and end indices to sample at. Will return the number of
    tuples specified by samples. The start and end index of the tuples will be separated by interval.
    '''
    out = []
    stride = (length - interval) / (samples - 1)
    for i in range(samples):
        start = stride * i
        end = start + interval
        out.append((start, end))
    return out

def get_correct_geometry(angles):
    '''
    Takes two angles of roads in the intersection and returns a tuple that contains the angle for the 'Right'
    direction and the angle for the 'Down' direction.
    '''
    a1 = angles[0]
    a2 = angles[1]
    min_a1 = min(abs(a1), abs(opposite_angle(a1)))
    min_a2 = min(abs(a2), abs(opposite_angle(a2)))

    out = []
    # Heuristic: the angle with the least magnitude is right. (In the coordinate space, an angle of 0
    # corresponds to right
    # Then, make sure that the second angle ('Down') is positive. Positive angles correspond to down in
    # the coordinate space
    if min_a1 < min_a2:
        if abs(a1) > math.pi / 2:
            out.append(opposite_angle(a1))
        else:
            out.append(a1)
        if a2 < 0:
            out.append(opposite_angle(a2))
        else:
            out.append(a2)
    else:
        if abs(a2) > math.pi / 2:
            out.append(opposite_angle(a2))
        else:
            out.append(a2)
        if a1 < 0:
            out.append(opposite_angle(a1))
        else:
            out.append(a1)

    return out

def classify_trajectory(trajectory, geometry):
    time_classification = classify_trajectory_vels(trajectory, geometry, get_velocity_time)
    distance_classification = classify_trajectory_vels(trajectory, geometry, get_velocity_distance)
    template_classification = classify_trajectory_template(trajectory, geometry)
    print("Timewise: ", time_classification)
    print("Distancewise: ", distance_classification)
    print("Templatewise: ", template_classification)
    return time_classification

def classify_trajectory_template(trajectory, geometry, num_samples = 10):
    samples = get_sample_tuples(len(trajectory), num_samples, 10)

    for i in range(0,1,.1):
        print('hi')
        print(angle_in_trajectory('left', 'down', i, (.4, 1.9)))

    angles = []
    for sample in samples:
        vel = average_velocity(trajectory, sample[0], sample[1])
        angles.append(math.atan2(vel[1], vel[0])))

    directions = ['right', 'down', 'left', 'up']
    l = [] # [('left','down',.2),...]

    sum_squares = 0
    for initial_direction in directions:
        for final_direction in directions:
            if initial_direction == final_direction:
                continue

            for i in range(len(samples)):
                angle = angles[i]
                predicted_angle = angle_in_trajectory(initial_direction, final_direction, float(i) / (num_samples - 1), geometry)
                sum_squares += angle_difference(angle, predicted_angle) ** 2

            rms = math.sqrt(sum_squares / num_samples)
            l.append((initial_direction, final_direction, rms))

    best = sorted(l, key=lambda x: x[2])[0]
    return (best[0], best[1])

def angle_in_trajectory(initial_direction, final_direction, percent_done, geometry):
    '''
    Returns the angle that an object turning in the given direction from the initial direction will
    have when it is some percent of the way through its trajectory specified by percent_done.
    '''
    directions = ['right', 'down', 'left', 'up']
    angles = [geometry[0], geometry[1], opposite_angle(geometry[0]), opposite_angle(geometry[1])]
    initial_index = directions.index(initial_direction.lower())
    final_index = directions.index(final_direction.lower())

    start_angle = angles[initial_index]
    final_angle = angles[final_index]

    diff = angle_difference(start_angle, final_angle)

    return normalize_angle(start_angle + percent_done * diff)

def classify_trajectory_vel(trajectory, geometry, vel_function):
    '''
    Returns a tuple of the initial and final heading of a trajectory. For example, ('Right', 'Down')
    '''
    vels = vel_function(trajectory)
    initial_vel = vels[0]
    initial_angle = math.atan2(initial_vel[1], initial_vel[0]))
    final_vel = vels[1]
    final_angle = math.atan2(final_vel[1], final_vel[0]))

    return (angle_to_direction(initial_angle, geometry), angle_to_direction(final_angle, geometry))

def get_velocity_time(trajectory):
    # Look at velocity in first and last second
    interval = 45
    samples = get_sample_tuples(len(trajectory), 2, interval)

    vels = []
    for sample in samples:
        vels.append(average_velocity(trajectory, sample[0], sample[1]))

    return vels

def get_velocity_distance(trajectory):
    # Look at velocity in first bit of distance traveled
    initial_vel = velocity_by_distance(trajectory, 0)
    final_vel = velocity_by_distance(trajectory, len(trajectory) - 1, forward=False)
    return [initial_vel, final_vel]

def velocity_by_distance(trajectory, start_frame, forward=True, threshold_distance=75):
    '''
    Returns the velocity of the object starting at start_frame until the object has traveled
    the distance (in pixels) specified by threshold_distance.

    Even if forward is False, the returned value will be the velocity of the object moving forward.

    If the object never travels a distance threshold_distance, it will return either the
    velocity in the first half of the trajectory or the velocity in the second half of the
    trajectory, depending on whether the start_frame is in the first or second half of the trajectory.
    (This behavior is intended to assist with classify_trajectory_distance)
    '''
    start_pos = trajectory[start_frame]:

    increment = 1
    if not forward:
        increment = -1
    frame = start_frame + increment
    while frame < len(trajectory) and frame >= 0:
        pos = trajectory[frame]
        distance = math.sqrt((pos[0] - start_pos[0])**2 + (pos[1] - start_pos[1])**2)
        if distance >= threshold_distance:
            if frame < start_frame:
                return average_velocity(trajectory, frame, start_frame)
            else:
                return average_velocity(trajectory, start_frame, frame)
        frame += increment

    # If we got past that, we didn't travel the threshold distance
    if start_frame <= len(trajectory) / 2:
        return average_velocity(trajectory, 0, len(trajectory) / 2)
    else:
        return average_velocity(trajectory, len(trajectory) / 2, len(trajectory))

def average_velocity(trajectory, start, end):
    '''
    Returns the velocity of an object from the start to the end index.
    '''
    if end >= len(trajectory):
        end = len(trajectory)

    startpoint = trajectory[start]
    endpoint = trajectory[end-1]
    return (endpoint[0] - startpoint[0], endpoint[1] - startpoint[1])

def angle_to_direction(angle, geometry):
    '''
    Returns a string representation of an angle for a given geometry. For example, could return 'Right'
    for an angle of .04 radians if the right in the geometry is .02.
    '''
    right = geometry[0]
    down = geometry[1]
    left = opposite_angle(right)
    up = opposite_angle(down)

    rightdown = midpoint(right, down)
    leftdown = midpoint(left, down)
    leftup = midpoint(left, up)
    rightup = midpoint(right, up)

    # In clockwise, angle should increase. Thus, angles is sorted, but offset.

    # The values in the directions array correspond to the angles array. For a given index in the
    # directions array, an object will have that value for its direction iff it has an angle between
    # the angle at that position and the next position in the angles array.
    # Example: Object a has an angle between leftup and rightup (indexes 2 and 3). Therefore, its
    # direction is "Up" (index 2).

    angles = [rightdown, leftdown, leftup, rightup]
    directions = ["Down", "Left", "Up", "Right"]

    least_index = find_discontinuity(angles)
    most_index = (least_index - 1) % 4

    if angle <= angles[least_index] or angle >= angles[most_index]:
        return directions[most_index]

    for j in range(3):
        curr = (least_index + j) % 4
        n = (curr + 1) % 4
        if angle >= angles[curr] and angle <= angles[n]:
            return directions[curr]

    print("Failed to find direction")
    raise Exception()

def opposite_angle(a):
    '''
    Returns the angle 180 degrees offset from a. Will output in the range -pi to pi.
    '''
    return normalize_angle(a + math.pi)

def normalize_angle(a):
    '''
    Takes an angle that may not be in the -pi to pi space, and converts it to a value between -pi and pi.
    '''
    while a > math.pi:
        a -= 2*math.pi
    while a < -math.pi:
        a += 2*math.pi
    return a

def similar_angles(a1, a2, max_diff=20):
    '''
    Returns True if the angles are within max_diff of each other. (max_diff is specified in degrees
    for human readability).
    '''
    max_radian_diff = max_diff * math.pi / 180
    if discontinuous_angles(a1, a2):
        # tot_angle will be near 2*pi iff they are near and discontinuous
        tot_angle = abs(a1 - a2)
        return abs(tot_angle - 2*math.pi) < max_radian_diff
    else:
        return abs(a1 - a2) < max_radian_diff

def angle_difference(a1, a2):
    '''
    Returns the minimum angle that a1 would have to swing through in order to reach a2.
    If the return value is positive, that means a1 would rotate counter-clockwise to reach a2,
    and if the return value is negative, a1 would rotate clockwise to reach a2.
    '''
    # a2 - a1 gives positive if a2 > a1, which is consistent with rotating counter-clockwise
    diff = a2 - a1
    return normalize_angle(diff)

def find_discontinuity(angles):
    '''
    Takes an array that is sorted but offset and returns the index of the least element
    '''
    for i in range(len(angles)):
        if angles[i] < angles[i-1]:
            return i
    return None

def discontinuous_angles(a1, a2):
    '''
    Returns True if the nearest path between the angles is through the discontinuity at pi/-pi.
    (i.e. we can't do simple arithmetic to find the closest difference between them)
    '''
    # Make a1 the larger, to fix later assumptions
    if a1 < a2:
        a1, a2 = a2, a1

    is_different = (a1 > 0 and a2 < 0)
    return is_different and (a1 - a2 > math.pi)

def midpoint(a1, a2):
    '''
    Returns the midpoint of the two objects between the smallest difference between them.
    '''
    if discontinuous_angles(a1, a2):
        angle = math.pi + (a1 + a2) / 2
        return normalize_angle(angle)
    else:
        return (a1 + a2) / 2


if __name__=="__main__":
    import os
    project_path = './../../project_dir/8871ad0e-d75b-4f6f-a95a-07b98a911bc9'
    db = os.path.join(project_path, 'run', 'results.sqlite')
    homography = os.path.join(project_path, 'homography', 'homography.txt')
    obj_to_heading = trajectory_headings(db, homography)
    objs = get_objects_with_trajectory(obj_to_heading, turn='left')
    print(objs)

    from video import save_video_frame
    video_path = os.path.join(project_path, 'stmarc_video.avi')
    image_path = os.path.join(project_path, 'frame.png')
    save_path = os.path.join(project_path, 'out.png')
    save_video_frame(video_path, image_path)

    from plotting.visualization import road_user_traj, turn_icon_counts
    road_user_traj(db, homography, image_path, save_path, objs_to_plot=objs, plot_cars=True)


    out = {}

    for turn in ['left', 'straight', 'right']:
        for direction in ['right', 'down', 'left', 'up']:
            if direction not in out:
                out[direction] = {}

            objs = get_objects_with_trajectory(obj_to_heading, turn=turn, initial_heading=direction)
            out[direction][turn] = len(objs)

    save_path = os.path.join(project_path, 'turns.png')
    turn_icon_counts(out, save_path)

