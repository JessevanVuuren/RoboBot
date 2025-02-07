from pyray import *  # type: ignore
from render import ShaderManager
from read_robot import Robot
from typing import Optional
from link import Link
from models import *
from utilz import *

import math


class RobotArm2Link:
    def __init__(self, robot:Robot):
        self.robot = robot
        self.link_length = robot.arm_length
        
        link1 = Link(robot.origin, robot.arm_length, robot.origin)
        link2 = Link(link1.end_pos, robot.arm_length, robot.origin)
        
        self.links = [link1, link2]

        self.yaw = 0
        self.angle1 = 0
        self.angle2 = 0

    def compute_ik(self, point_to_follow: Vector3):
        end_effector_xz = Vector2(point_to_follow.x, point_to_follow.z)
        origin_point_xz = Vector2(self.links[0].start_pos.x, self.links[0].start_pos.z)

        xz_distance = vector2_distance(end_effector_xz, origin_point_xz)
        vertical_offset = point_to_follow.y - self.links[0].start_pos.y
        base_angle = math.atan2(vertical_offset, xz_distance)

        distance = math.sqrt(xz_distance**2 + vertical_offset**2)
        distance = min(distance, self.link_length * 2)

        alpha = math.acos((distance**2 + self.link_length**2 - self.link_length**2) / (2 * distance * self.link_length))
        beta = math.acos((self.link_length**2 + self.link_length**2 - distance**2) / (2 * self.link_length * self.link_length))
        theta = math.atan2(point_to_follow.x, point_to_follow.z)

        self.angle1 = base_angle + alpha
        self.angle2 = math.pi - beta
        self.yaw = theta

        self.links[0].set_angle_x(self.angle1)
        self.links[0].set_angle_y(-theta)
        self.links[1].set_start_point(self.links[0].end_pos)
        self.links[1].set_angle_x(self.angle1 - self.angle2)
        self.links[1].set_angle_y(-theta)


    def render_bones(self):
        self.links[0].render_link()
        self.links[1].render_link()

    def compute_body(self):
        for part in self.robot.parts:
            link = self.links[part.link_index]

            link_point = link.get_body_position()

            link_with_yaw = matrix_multiply(matrix_rotate_y(self.yaw), link_point)

            position_lock = lock_matrix_position(link_with_yaw, part.lock_position)
            rotation_lock = lock_matrix_rotation(position_lock, part.lock_rotation)

            origin = vector3_to_matrix(link.start_pos)
            part_offset = matrix_multiply(part.offset, rotation_lock)
            final_position = matrix_multiply(part_offset, origin)

            part.position = final_position

    def render_body(self, shader: Optional[ShaderManager] = None):
        for part in self.robot.parts:

            if (shader):
                with shader:
                    draw_mesh(part.body, part.material, part.position)
            else:
                draw_mesh(part.body, part.material, part.position)
