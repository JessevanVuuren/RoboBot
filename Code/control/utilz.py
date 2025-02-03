from pyray import *  # type: ignore


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
