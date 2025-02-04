from pyray import *  # type: ignore
from render import ShaderManager
from typing import Optional
from link import Link
from models import *
from utilz import *

import math


class RobotArm2Link:
    def __init__(self, base_pos: Vector3, link_length: float):
        self.link_length = link_length
        self.link1 = Link(base_pos, link_length)
        self.link2 = Link(self.link1.end_pos, link_length)
        self.body_parts: list[RobotPart] = []

        self.yaw = 0

    def compute_ik(self, point_to_follow: Vector3):
        end_effector_xz = Vector2(point_to_follow.x, point_to_follow.z)
        origin_point_xz = Vector2(self.link1.start_pos.x, self.link1.start_pos.z)

        xz_distance = vector2_distance(end_effector_xz, origin_point_xz)
        vertical_offset = point_to_follow.y - self.link1.start_pos.y
        base_angle = math.atan2(vertical_offset, xz_distance)

        distance = math.sqrt(xz_distance**2 + vertical_offset**2)
        arm_reach = self.link1.length + self.link2.length
        distance = min(distance, arm_reach)

        alpha = math.acos((distance**2 + self.link_length**2 - self.link_length**2) / (2 * distance * self.link_length))
        beta = math.acos((self.link_length**2 + self.link_length**2 - distance**2) / (2 * self.link_length * self.link_length))
        self.yaw = math.atan2(point_to_follow.x, point_to_follow.z)

        angle1 = base_angle + alpha
        angle2 = math.pi - beta

        
        self.link1.set_angle_x(angle1)
        self.link1.set_angle_y(-self.yaw)
        self.link2.set_start_point(self.link1.end_pos)
        self.link2.set_angle_x(angle1 - angle2)
        self.link2.set_angle_y(-self.yaw)

    def render_bones(self):
        self.link1.render_link()
        self.link2.render_link()

    def compute_body(self):
        for part in self.body_parts:
            if (not part.link):
                continue

            link_point = part.link.get_body_position()

            link_with_yaw = matrix_multiply(matrix_rotate_y(self.yaw), link_point)

            position_lock = lock_matrix_position(link_with_yaw, part.lock_position)
            rotation_lock = lock_matrix_rotation(position_lock, part.lock_rotation)

            origin = vector3_to_matrix(part.link.start_pos)
            part_offset = matrix_multiply(part.offset, rotation_lock)
            final_position = matrix_multiply(part_offset, origin)

            part.position = final_position



    def render_body(self, shader: Optional[ShaderManager] = None):
        for part in self.body_parts:

            if (shader):
                with shader:
                    draw_mesh(part.body, part.material, part.position)
            else:
                draw_mesh(part.body, part.material, part.position)
