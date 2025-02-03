from pyray import *
import serial
import math
import time

HEIGHT = 720
WIDTH = 1280


arduino = serial.Serial(port='COM8', baudrate=1000000, timeout=1)
time.sleep(1)


def write_read(x):
    arduino.write((x + '\n').encode())
    response = arduino.read_until(b'\n').decode().strip()
    return response


set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
init_window(WIDTH, HEIGHT, "RoBoBot")
set_target_fps(60)

x = WIDTH//2
y = HEIGHT//2

l_arm = 50
max_distance = 100

origin = Vector2(x, y)

while not window_should_close():

    begin_drawing()
    clear_background(get_color(0x181818FF))

    mouse_x = get_mouse_x()
    mouse_y = get_mouse_y()

    mouse = Vector2(mouse_x, mouse_y)

    distance = min(max_distance, vector2_distance(origin, mouse))

    alpha = math.acos((distance**2 + l_arm**2 - l_arm**2) / (2 * distance * l_arm))
    beta = math.acos((l_arm**2 + l_arm**2 - distance**2) / (2 * l_arm * l_arm))
    base_angle = math.atan2(mouse_y - origin.y, mouse_x - origin.x)

    angle1 = base_angle + alpha
    angle2 = math.pi - beta

    vector2 = Vector2(
        origin.x + l_arm * math.cos(angle1),
        origin.y + l_arm * math.sin(angle1)
    )
    vector3 = Vector2(
        vector2.x + l_arm * math.cos(angle1 - angle2),
        vector2.y + l_arm * math.sin(angle1 - angle2)
    )

    value = write_read(str(180 - (math.pi + angle1) * 57.2957795) + "|" + str(angle2 * 57.2957795) + "|")

    draw_line_ex(origin, vector2, 1, get_color(0xffffffFF))
    draw_line_ex(vector2, vector3, 1, get_color(0xffffffFF))

    draw_fps(10, 10)
    end_drawing()

close_window()
