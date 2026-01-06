from pathlib import Path
from typing import Optional
# from cffi import FFI
from models import *  # type: ignore
from pyray import *  # type: ignore
from utilz import *
import struct
import yaml


def load_part(path: str, origin: Vector3, part_config, shader, boom_length: int) -> RobotPart:

    mesh = load_stl_mesh(path + "/" + part_config["name"])

    material = load_material_default()
    material.maps[0].color = RED
    material.shader = shader

    part = RobotPart(part_config["name"], mesh, material, part_config["link"])

    rotation = yaml_to_vector3(part_config["rotation"])
    position = yaml_to_vector3(part_config["position"])

    matrix_rotation = matrix_rotate_xyz(vector3_to_radians(rotation))

    matrix_position = Matrix()
    if (part_config["type"] == "body"):
        matrix_position = vector3_to_matrix(vector3_subtract(position, origin))

    if (part_config["type"] == "boom"):
        pos = Vector3(position.x, -(boom_length / 2) + position.y, position.z)
        matrix_position = vector3_to_matrix(pos)

    lock_rotation = yaml_to_vector3(part_config["lock_rotation"])
    lock_position = yaml_to_vector3(part_config["lock_position"])

    part.lock_position = vector3_bitwise(lock_position)
    part.lock_rotation = vector3_bitwise(lock_rotation)

    part.offset = matrix_multiply(matrix_rotation, matrix_position)

    return part


def load_stl_mesh(file_path: str) -> Mesh:
    file = open(file_path + ".stl", 'rb')

    header = file.read(80)
    num_of_tri = int.from_bytes(file.read(4), byteorder="little")

    mesh = Mesh()
    mesh.vertexCount = num_of_tri * 3
    mesh.triangleCount = num_of_tri

    normals = []
    vertices = []
    for i in range(num_of_tri):
        triangle1 = file.read(50)

        normal = struct.unpack("<3f", triangle1[0:12])
        vertex1 = struct.unpack("<3f", triangle1[12:24])
        vertex2 = struct.unpack("<3f", triangle1[24:36])
        vertex3 = struct.unpack("<3f", triangle1[36:48])

        vertices.extend((*vertex1, *vertex2, *vertex3))
        normals.extend((*normal, *normal, *normal))

    vertices_pointer = ffi.new(f"float[{len(vertices)}]", vertices)
    normals_pointer = ffi.new(f"float[{len(normals)}]", normals)

    mesh.vertices = vertices_pointer
    mesh.normals = normals_pointer

    upload_mesh(mesh, True)
    file.close()

    return mesh


def load_robot(path, shader) -> Robot:
    file = open(path + "/config.yml")
    config = yaml.safe_load(file)
    file.close()

    origin = yaml_to_vector3(config["origin_point"])

    robot = Robot(
        name=config["name"],
        arm_length=config["arm_length"],
        origin=origin,
        parts=[]
    )

    for part in config["parts"]:
        robot.parts.append(load_part(path, origin, part, shader, config["arm_length"]))

    return robot
