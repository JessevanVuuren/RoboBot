from pyray import *  # type: ignore
from link import Link
import math


class RobotArm2Link:
    def __init__(self, base_pos: Vector3, link_length: float):
        self.link_length = link_length
        self.link1 = Link(base_pos, link_length)
        self.link2 = Link(self.link1.end_pos, link_length)

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
        yaw = math.atan2(point_to_follow.x, point_to_follow.z)

        angle1 = base_angle + alpha
        angle2 = math.pi - beta

        self.link1.set_angle_x(angle1)
        self.link1.set_angle_y(-yaw)
        self.link2.set_start_point(self.link1.end_pos)
        self.link2.set_angle_x(angle1 - angle2)
        self.link2.set_angle_y(-yaw)
