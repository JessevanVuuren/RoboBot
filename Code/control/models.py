from dataclasses import dataclass
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
class RobotBody:
    body: Mesh
    name: str
    material: Material
