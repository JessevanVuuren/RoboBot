from serial_com import SerialCommunicator
from robot_arm import RobotArm2Link
from link import Link

from xyz_control import *  # type: ignore
from read_robot import *  # type: ignore
from rcamera import *  # type: ignore
from render import *  # type: ignore
from utilz import *  # type: ignore
from pyray import *  # type: ignore

HEIGHT = 720
WIDTH = 1280
ZOOM_SPEED = 10
GRID_SIZE = 15
GRID_AMOUNT = 20
CAMERA_DISTANCE = 300

set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
init_window(WIDTH, HEIGHT, "RoBoBot")
set_target_fps(60)

camera_start_pos = Vector3(CAMERA_DISTANCE, CAMERA_DISTANCE, CAMERA_DISTANCE)
camera = Camera3D(camera_start_pos, Vector3(0, 50, 0), Vector3(0, 1, 0), 30.0, CameraProjection.CAMERA_PERSPECTIVE)

SC = SerialCommunicator("COM8", 1000000, 1, ["INFO"])
SC.start()

xyz = init_xyz()


def draw_grid():
    for x in range(0, GRID_AMOUNT):
        for z in range(0, GRID_AMOUNT):
            if (x == 0 or z == 0):
                continue

            x_delta = (x - GRID_AMOUNT / 2) * GRID_SIZE
            z_delta = (z - GRID_AMOUNT / 2) * GRID_SIZE
            end_effector = GRID_AMOUNT / 2 * GRID_SIZE

            start = Vector3(x_delta, 0, -end_effector)
            end = Vector3(x_delta, 0, end_effector)

            draw_line_3d(start, end, Color(100, 100, 100, 255))

            start = Vector3(-end_effector, 0, z_delta)
            end = Vector3(end_effector, 0, z_delta)

            draw_line_3d(start, end, Color(100, 100, 100, 255))


def render():
    with world_layer:
        draw_grid()
        draw_sphere(point_to_follow, .13, get_color(0xffdd33FF))
        draw_line_3d(vector3_zero(), point_to_follow, get_color(0xFFFFFFFF))

        arm.render_bones()
        arm.render_body()

    with xyz_layer:
        draw_xyz_control(point_to_follow, xyz, camera)

    with ui_layer:
        draw_fps(10, 30)
        if (SC.is_connected):
            draw_text("ServoBot connected", 10, 10, 20, get_color(0x14f06fff))
        else:
            draw_text("ServoBot disconnected", 10, 10, 20, get_color(0xf0a727ff))

    begin_drawing()
    world_layer.draw()
    xyz_layer.draw()
    ui_layer.draw()
    end_drawing()


world_layer = RenderLayer(WIDTH, HEIGHT, True, camera, get_color(0x181818FF))
xyz_layer = RenderLayer(WIDTH, HEIGHT, True, camera)
ui_layer = RenderLayer(WIDTH, HEIGHT, False, camera)

shader = ShaderManager("shaders/lighting.vs", "shaders/lighting.fs")
shader.set_locs(ShaderLocationIndex.SHADER_LOC_MATRIX_MODEL, "model")
shader.set_locs(ShaderLocationIndex.SHADER_LOC_MATRIX_VIEW, "view")
shader.set_locs(ShaderLocationIndex.SHADER_LOC_MATRIX_PROJECTION, "projection")
shader.set_vector3_value(vector3_zero(), "lightPosition")
shader.set_vector3_value(vector3_one(), "lightColor")

point_to_follow = Vector3(0, 30, 50)
# point_to_follow = Vector3(0, 300, 0)

robot = load_robot("../../robots/ServoBot", shader.shader)
arm = RobotArm2Link(robot)


while not window_should_close():

    dist = get_mouse_wheel_move()
    camera_move_to_target(camera, -dist * ZOOM_SPEED)
    shader.set_vector3_value(camera.position, "lightPosition")

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
    arm.compute_body()

    yaw = round(math.degrees(arm.yaw))
    angle1 = round(math.degrees(arm.angle1))
    angle2 = round(math.degrees(arm.angle2))

    data_to_write = str(yaw + 90) + "|" + str(180 - angle1) + "|" + str(angle2) + "|"

    SC.write(data_to_write)

    render()


SC.stop()
close_window()
