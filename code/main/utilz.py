from pyray import *  # type: ignore
import math

DEGREES_TO_RADIANS = 0.0174532925

def print_vec(v):
    print(v.x, v.y, v.z)


def print_q(v):
    print(v.x, v.y, v.z, v.w)


def deref_vector3(v: Vector3) -> Vector3:
    return Vector3(v.x, v.y, v.z)


def vector3_to_matrix(v: Vector3) -> Matrix:
    return matrix_translate(v.x, v.y, v.z)


def matrix_to_vector(m: Matrix) -> Vector3:
    return Vector3(m.m12, m.m13, m.m14)


def get_midpoint(start, end):
    return vector3_scale(vector3_subtract(end, start), .5)


def get_rotation_between_points(start,  end):
    up = Vector3(0, 1, 0)
    direction = vector3_normalize(vector3_subtract(end, start))
    axis = vector3_cross_product(up, direction)
    dot = vector3_dot_product(up, direction)
    angle = math.acos(dot)

    return quaternion_from_axis_angle(axis, angle)


def lock_matrix_position(final_position: Matrix, lock: Vector3) -> Matrix:
    final_position.m12 *= lock.x
    final_position.m13 *= lock.y
    final_position.m14 *= lock.z

    return final_position


def lock_matrix_rotation(final_position, lock):
    position = matrix_to_vector(final_position)
    rotation = quaternion_from_matrix(final_position)

    rotation.x *= lock.x
    rotation.y *= lock.y
    rotation.z *= lock.z

    return matrix_multiply(quaternion_to_matrix(rotation), vector3_to_matrix(position))
    

def yaml_to_vector3(v) -> Vector3:
    return Vector3(v[0], v[1], v[2])


def vector3_to_radians(v: Vector3) -> Vector3:
    return vector3_scale(v, DEGREES_TO_RADIANS)


def vector3_bitwise(v:Vector3):
    return Vector3(int(v.x) ^ 1, int(v.y) ^ 1, int(v.x) ^ 1)