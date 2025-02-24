from dataclasses import dataclass
from typing import Optional
from link import Link
from pyray import *  # type: ignore


@dataclass
class AxisHitBox:
    mesh: Mesh
    offset: Vector3
    material: Material
    matrix = matrix_identity()


@dataclass
class AxisControl:
    hit_box: AxisHitBox
    control_axis: Vector3
    hidden_plane_matrix: Matrix
    ray: RayCollision = RayCollision()


@dataclass
class XYZControl:
    x: AxisControl
    y: AxisControl
    z: AxisControl
    hidden_plane: Mesh
    position: Vector3 = vector3_zero()

@dataclass
class RobotPart:
    name: str
    body: Mesh
    material: Material
    link_index:int
    lock_rotation: Vector3 = Vector3(1, 1, 1)
    lock_position: Vector3 = Vector3(1, 1, 1)
    offset: Matrix = matrix_identity()
    position: Matrix = matrix_identity()
    link: Optional[Link] = None


@dataclass
class Robot():
    name: str
    arm_length: float
    origin: Vector3
    parts: list[RobotPart]