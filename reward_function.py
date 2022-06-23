import math

def reward_function(params):
    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * params['track_width']
    marker_2 = 0.25 * params['track_width']
    marker_3 = 0.5 * params['track_width']

    reward = 1.0
    speed_threshold_1 = 1.8
    speed_threshold_2 = 1.3
    direction_threshold = 3.0

    speed = params['speed']
    steps = params['steps']
    is_offtrack = params['is_offtrack']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    benchmark_time = 11.7
    benchmark_steps = 173
    straight_waypoints = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 43, 44, 45, 46,
                          47, 48, 49, 50, 56, 57, 58, 59, 60, 61, 62, 63, 64, 71, 72, 73, 74, 75, 76, 77, 78, 89, 90,
                          91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 112, 113, 114, 115, 116, 117]

    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx),
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])

    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)

    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    if direction_diff > direction_threshold:
        reward *= 0.5

        # Get reward if completes the lap and more reward if it is faster than benchmark_time
        if progress == 100:
            if round(steps / 15, 1) < benchmark_time:
                reward += 100 * round(steps / 15, 1) / benchmark_time
            else:
                reward += 100
        elif is_offtrack:
            reward -= 50

        if direction_diff > direction_threshold or not all_wheels_on_track:

            direction_bonus = 1 - (direction_diff / 15)
            if direction_bonus < 0 or direction_bonus > 1:
                direction_bonus = 0
            reward *= direction_bonus
        else:
            if next_point in straight_waypoints:
                if speed >= speed_threshold_1:
                    reward += max(speed, speed_threshold_1)
                else:
                    reward += 1e-3
            else:
                if speed <= speed_threshold_2:
                    reward += max(speed, speed_threshold_2)
                else:
                    reward += 1e-3

        # Give additional reward if the car pass every 50 steps faster than expected
        if (steps % 50) == 0 and progress >= (steps / benchmark_steps) * 100:
            reward += 10.0
        # Penalize if the car cannot finish the track in less than benchmark_steps
        elif (steps % 50) == 0 and progress < (steps / benchmark_steps) * 100:
            reward -= 5.0

    # Give higher reward if the car is closer to center line and vice versa
    if params['distance_from_center'] <= marker_1:
        reward = 1
    elif params['distance_from_center'] <= marker_2:
        reward = 0.5
    elif params['distance_from_center'] <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # Steering penalty threshold, change the number based on your action space setting
    abs_steering_threshold = 15

    # Penalize reward if the car is steering too much
    if abs(params['steering_angle']) > abs_steering_threshold:  # Only need the absolute steering angle
        reward *= 0.5

    # penalize reward for the car taking slow actions
    # speed is in m/s
    # we penalize any speed less than 0.5m/s
    speed_threshold = 0.5
    if params['speed'] < speed_threshold:
        reward *= 0.5

    if params['speed'] > speed_threshold:
        reward *= 1.5

    if params['all_wheels_on_track']:
        reward += 1.0
    else:
        reward -= 1.0  # penalize if the car is off track
    if params['is_left_of_center']:
        reward += 1.0
    if params['is_reversed']:
        reward -= 1.0

    if params['steps'] > 200:
        reward -= 1.0  # penalize if the car is stuck
    else:
        reward += 1.0

    if params['closest_waypoints'][0] == 0:
        reward += 1.0  # reward if the car is on the first waypoint

    if params['closest_objects'][0] == 0:
        reward += 1.0
    else:
        reward -= 1.0
    if params['heading'] < 0:
        reward += 1.0  # reward if the car is heading towards the center
    else:
        reward -= 1.0
    if params['is_crashed']:
        reward -= 1.0  # penalize if the car is crashed
    if params['is_offtrack']:
        reward -= 1.0  # penalize if the car is off track

    if params['progress'] == 100:
        reward = 10000.0

    return float(reward)
