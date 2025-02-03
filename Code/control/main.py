from serialCom import SerialCommunicator
from robot_arm import RobotArm2Link
from link import Link

from xyz_control import *  # type: ignore
from rcamera import *  # type: ignore
from utilz import *  # type: ignore
from pyray import *  # type: ignore

import math

HEIGHT = 720
WIDTH = 1280
ZOOM_SPEED = 1
GRID_AMOUNT = 20
CAMERA_DISTANCE = 20

set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
init_window(WIDTH, HEIGHT, "RoBoBot")
set_target_fps(60)

target = vector3_zero()
camera_start_pos = Vector3(CAMERA_DISTANCE, CAMERA_DISTANCE, CAMERA_DISTANCE)
camera_start_up = Vector3(0, 1, 0)

camera = Camera3D(camera_start_pos, target, camera_start_up, 30.0, CameraProjection.CAMERA_PERSPECTIVE)

xyz_layer = load_render_texture(WIDTH, HEIGHT)
world_layer = load_render_texture(WIDTH, HEIGHT)
ui_layer = load_render_texture(WIDTH, HEIGHT)


def draw_grid():
    for x in range(0, GRID_AMOUNT):
        for z in range(0, GRID_AMOUNT):
            if (x == 0 or z == 0):
                continue
            start = Vector3(x - GRID_AMOUNT / 2, 0, -GRID_AMOUNT / 2)
            end = Vector3(x - GRID_AMOUNT / 2, 0, GRID_AMOUNT / 2)

            draw_line_3d(start, end, Color(100, 100, 100, 255))

            start = Vector3(- GRID_AMOUNT / 2, 0, z - GRID_AMOUNT / 2)
            end = Vector3(GRID_AMOUNT / 2, 0, z - GRID_AMOUNT / 2)

            draw_line_3d(start, end, Color(100, 100, 100, 255))


def render():
    # render 3d world
    begin_texture_mode(world_layer)
    clear_background(get_color(0x181818FF))
    begin_mode_3d(camera)

    draw_sphere(point_to_follow, .13, get_color(0xffdd33FF))
    draw_line_3d(vector3_zero(), point_to_follow, get_color(0xFFFFFFFF))
    draw_grid()

    
    arm.link1.render_link()
    arm.link2.render_link()

    end_mode_3d()
    end_texture_mode()
    ##

    # render xyz control
    begin_texture_mode(xyz_layer)
    begin_mode_3d(camera)
    clear_background(get_color(0x00000000))
    draw_xyz_control(point_to_follow, xyz, camera)
    end_mode_3d()
    end_texture_mode()
    ##

    # render ui layer
    begin_texture_mode(ui_layer)
    clear_background(get_color(0x00000000))
    draw_fps(10, 30)
    if (SC.is_connected):
        draw_text("ServoBot connected", 10, 10, 20, get_color(0x14f06fff))
    else:
        draw_text("ServoBot disconnected", 10, 10, 20, get_color(0xf0a727ff))
    end_texture_mode()
    ##

    begin_drawing()
    draw_texture_rec(world_layer.texture, Rectangle(0, 0, world_layer.texture.width, -world_layer.texture.height), Vector2(0, 0), get_color(0xFFFFFFFF))
    draw_texture_rec(xyz_layer.texture, Rectangle(0, 0, xyz_layer.texture.width, -xyz_layer.texture.height), Vector2(0, 0), get_color(0xFFFFFFFF))
    draw_texture_rec(ui_layer.texture, Rectangle(0, 0, ui_layer.texture.width, -ui_layer.texture.height), Vector2(0, 0), get_color(0xFFFFFFFF))
    end_drawing()



SC = SerialCommunicator("COM8", 1000000, 1, ["INFO"])
SC.start()



point_to_follow = Vector3(0, 3, 5)

arm_length = 5
origin_point = vector3_zero()
arm = RobotArm2Link(origin_point, arm_length)

xyz = init_xyz()

while not window_should_close():

    dist = get_mouse_wheel_move()
    camera_move_to_target(camera, -dist * ZOOM_SPEED)

    if (is_mouse_button_down(MouseButton.MOUSE_BUTTON_RIGHT)):
        mouseDelta = get_mouse_delta()
        camera_yaw(camera, -mouseDelta.x * .01, True)
        camera_pitch(camera, -mouseDelta.y * .01, True, True, False)

    if (is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)):
        ray = get_screen_to_world_ray(get_mouse_position(), camera)

        xyz.x.ray = get_ray_collision_mesh(ray, xyz.x.hit_box.mesh, xyz.x.hit_box.matrix)
        xyz.y.ray = get_ray_collision_mesh(ray, xyz.y.hit_box.mesh, xyz.y.hit_box.matrix)
        xyz.z.ray = get_ray_collision_mesh(ray, xyz.z.hit_box.mesh, xyz.z.hit_box.matrix)
        xyz.position = deref_vector3(point_to_follow)

    if (is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT)):
        xyz.x.ray.hit = False
        xyz.y.ray.hit = False
        xyz.z.ray.hit = False

    if (xyz.x.ray.hit):
        angle = math.atan2(camera.position.z, camera.position.y)
        new_position = move_point(point_to_follow, angle, xyz.x, camera, xyz)
        point_to_follow.x = new_position.x

    if (xyz.y.ray.hit):
        angle = math.atan2(camera.position.x, camera.position.z)
        new_position = move_point(point_to_follow, angle, xyz.y, camera, xyz)
        point_to_follow.y = new_position.y

    if (xyz.z.ray.hit):
        angle = math.atan2(camera.position.y, camera.position.x)
        new_position = move_point(point_to_follow, angle, xyz.z, camera, xyz)
        point_to_follow.z = new_position.z


    arm.compute_ik(point_to_follow)

    angle1 = math.degrees(arm.link1.get_angle())
    angle2 = math.degrees(arm.link2.get_angle())

    data_to_write = str(180 - angle1) + "|" + str((angle1 - angle2) * 2) + "|"
    
    SC.write(data_to_write)



    render()


SC.stop()
close_window()
