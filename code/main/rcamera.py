from pyray import * # type: ignore


def camera_yaw(camera: Camera3D, angle, rotate_around_target):
    up = vector3_normalize(camera.up)

    target_position = vector3_subtract(camera.target, camera.position)
    
    target_position = vector3_rotate_by_axis_angle(target_position, up, angle)

    if (rotate_around_target):
        camera.position = vector3_subtract(camera.target, target_position)
    else:
        camera.target = vector3_add(camera.position, target_position)


def get_camera_right(camera: Camera3D):

    forward = vector3_normalize(vector3_subtract(camera.target, camera.position))
    up = vector3_normalize(camera.up)

    return vector3_cross_product(forward, up)

def get_camera_forward(camera):
    return vector3_normalize(vector3_subtract(camera.target, camera.position));


def camera_pitch(camera: Camera3D, angle, lock_view, rotate_around_target, rotate_up):
    up = vector3_normalize(camera.up)

    target_position = vector3_subtract(camera.target, camera.position)

    if (lock_view):
        max_angle_up = vector3_angle(up, target_position)
        max_angle_up -= 0.001

        if (angle > max_angle_up):
            angle = max_angle_up

        maxAngleDown = vector3_angle(vector3_negate(up), target_position)
        maxAngleDown *= -1.0
        maxAngleDown += 0.001
        if (angle < maxAngleDown):
            angle = maxAngleDown

    right = get_camera_right(camera)

    target_position = vector3_rotate_by_axis_angle(target_position, right, angle)

    if (rotate_around_target):
        camera.position = vector3_subtract(camera.target, target_position)
    else:
        camera.target = vector3_add(camera.position, target_position)

    if (rotate_up):
        camera.up = vector3_rotate_by_axis_angle(camera.up, right, angle)

def camera_move_to_target(camera, delta):

    distance = vector3_distance(camera.position, camera.target)

    distance += delta

    if (distance <= 0):
        distance = 0.001

    forward = get_camera_forward(camera);
    camera.position = vector3_add(camera.target, vector3_scale(forward, -distance));
