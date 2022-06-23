def reward_function(params):
    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * params['track_width']
    marker_2 = 0.25 * params['track_width']
    marker_3 = 0.5 * params['track_width']

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
    if params['closest_waypoint'] == 0:
        reward += 1.0
    if params['crashed']:
        reward = -1.0
    if params['is_left_of_center']:
        reward += 1.0
    # if params['offtrack']:
    #     reward -= 1.0
    if params['is_reversed']:
        reward -= 1.0
    if params['progress'] == 100:
        reward = 10000.0

    return float(reward)
