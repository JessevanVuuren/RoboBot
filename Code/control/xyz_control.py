from dataclasses import dataclass
from pyray import *  # type: ignore
from utilz import *  # type: ignore
import math


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
    hidden_plane:Mesh
    position: Vector3 = vector3_zero()


def init_xyz() -> XYZControl:
    hidden_plane = gen_mesh_plane(10, 10, 1, 1)

    mesh_x = gen_mesh_cube(1.5, .15, .15)
    mesh_y = gen_mesh_cube(.15, 1.5, .15)
    mesh_z = gen_mesh_cube(.15, .15, 1.5)

    offset_x = Vector3(.75, 0, 0)
    offset_y = Vector3(0, .75, 0)
    offset_z = Vector3(0, 0, .75)

    material_x = load_material_default()
    material_x.maps[0].color = get_color(0xFF3352CC)

    material_y = load_material_default()
    material_y.maps[0].color = get_color(0x8BDC00CC)

    material_z = load_material_default()
    material_z.maps[0].color = get_color(0x2890FFCC)

    hit_box_x = AxisHitBox(mesh_x, offset_x,  material_x)
    hit_box_y = AxisHitBox(mesh_y, offset_y,  material_y)
    hit_box_z = AxisHitBox(mesh_z, offset_z,  material_z)

    axis_control_x = AxisControl(hit_box_x, Vector3(1, 0, 0), matrix_rotate_x(math.radians(0)))
    axis_control_y = AxisControl(hit_box_y, Vector3(0, 1, 0), matrix_rotate_x(math.radians(90)))
    axis_control_z = AxisControl(hit_box_z, Vector3(0, 0, 1), matrix_rotate_z(math.radians(-90)))

    return XYZControl(axis_control_x, axis_control_y, axis_control_z, hidden_plane)


def draw_xyz_control(target: Vector3, xyz: XYZControl, camera: Camera3D):
    end_pos_x_axis = vector3_add(target, Vector3(1.5, 0, 0))
    end_pos_y_axis = vector3_add(target, Vector3(0, 1.5, 0))
    end_pos_z_axis = vector3_add(target, Vector3(0, 0, 1.5))

    draw_cylinder_ex(end_pos_x_axis, Vector3(end_pos_x_axis.x + .5, end_pos_x_axis.y, end_pos_x_axis.z), .1, 0, 30, get_color(0xFF3352ff))
    draw_cylinder_ex(end_pos_y_axis, Vector3(end_pos_y_axis.x, end_pos_y_axis.y + .5, end_pos_y_axis.z), .1, 0, 30, get_color(0x8BDC00ff))
    draw_cylinder_ex(end_pos_z_axis, Vector3(end_pos_z_axis.x, end_pos_z_axis.y, end_pos_z_axis.z + .5), .1, 0, 30, get_color(0x2890FFff))

    draw_line_3d(target, end_pos_x_axis, get_color(0xFF3352ff))
    draw_line_3d(target, end_pos_y_axis, get_color(0x8BDC00ff))
    draw_line_3d(target, end_pos_z_axis, get_color(0x2890FFff))

    xyz.x.hit_box.matrix = vector3_to_matrix(vector3_add(xyz.x.hit_box.offset, target))
    draw_mesh(xyz.x.hit_box.mesh, xyz.x.hit_box.material, xyz.x.hit_box.matrix)

    xyz.y.hit_box.matrix = vector3_to_matrix(vector3_add(xyz.y.hit_box.offset, target))
    draw_mesh(xyz.y.hit_box.mesh, xyz.y.hit_box.material, xyz.y.hit_box.matrix)

    xyz.z.hit_box.matrix = vector3_to_matrix(vector3_add(xyz.z.hit_box.offset, target))
    draw_mesh(xyz.z.hit_box.mesh, xyz.z.hit_box.material, xyz.z.hit_box.matrix)


def move_point(point: Vector3, angle: float, ac: AxisControl, camera: Camera3D, xyz:XYZControl) -> Vector3:
    rotate_to_camera = matrix_rotate(ac.control_axis, angle)
    default_rotation = matrix_multiply(ac.hidden_plane_matrix, rotate_to_camera)
    translate_to_point = matrix_multiply(default_rotation, vector3_to_matrix(point))

    ray = get_screen_to_world_ray(get_mouse_position(), camera)
    ray = get_ray_collision_mesh(ray, xyz.hidden_plane, translate_to_point)

    offset = vector3_subtract(ac.ray.point, xyz.position)
    return vector3_subtract(ray.point, offset)



