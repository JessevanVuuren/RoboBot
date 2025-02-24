
from pyray import *  # type: ignore
from utilz import *
import math


class Link:
    def __init__(self, pos: Vector3, length, base_pos):
        self.start_pos = pos
        self.end_pos = Vector3(pos.x, pos.y + length, pos.z)
        self.length = length
        self.color = get_color(0xffffff44)
        self.base_pos = base_pos

    def render_link(self):
        scale = self.length * .1

        direction = vector3_subtract(self.end_pos, self.start_pos)
        norm = vector3_normalize(direction)
        midway = vector3_scale(norm, self.length * .2)
        midway = vector3_add(midway, self.start_pos)

        draw_cylinder_ex(self.start_pos, midway, 0, scale, 4, self.color)
        draw_cylinder_ex(midway, self.end_pos, scale, 0, 4, self.color)

        draw_cylinder_wires_ex(self.start_pos, midway, 0, scale, 4, self.color)
        draw_cylinder_wires_ex(midway, self.end_pos, scale, 0, 4, self.color)

    def set_end_point(self, point: Vector3):
        direction = vector3_normalize(vector3_subtract(point, self.start_pos))
        final_pos = vector3_scale(direction, self.length)

        self.end_pos = final_pos

    def set_start_point(self, point: Vector3):
        self.start_pos = point

    def get_angle(self):
        return math.atan2(self.end_pos.y - self.base_pos.y, self.end_pos.z)

    def set_angle_x(self, angle):
        y = self.start_pos.y + self.length * math.sin(angle)
        z = self.start_pos.z + self.length * math.cos(angle)

        self.end_pos = Vector3(self.start_pos.x, y, z)

    def set_angle_y(self, angle):
        rel = vector3_subtract(self.end_pos, self.start_pos)

        rotated_x = rel.x * math.cos(angle) - rel.z * math.sin(angle)
        rotated_z = rel.x * math.sin(angle) + rel.z * math.cos(angle)
        rotated = Vector3(rotated_x, rel.y, rotated_z)

        self.end_pos = vector3_add(self.start_pos, rotated)

    def get_body_position(self) -> Matrix:
        midpoint = get_midpoint(self.start_pos, self.end_pos)
        rotation = get_rotation_between_points(self.start_pos, self.end_pos)

        quat_to_matrix = quaternion_to_matrix(rotation)
        vec_to_matrix = vector3_to_matrix(midpoint)

        return matrix_multiply(quat_to_matrix, vec_to_matrix)
