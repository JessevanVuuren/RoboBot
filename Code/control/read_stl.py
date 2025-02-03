from pathlib import Path
from models import *  # type: ignore
from pyray import *  # type: ignore
from cffi import FFI
import struct
import os


def hex32_to_int(data):
    return int.from_bytes(data, byteorder="little")


def load_stl_mesh(file_path) -> RobotBody:

    file = open(file_path + ".stl", 'rb')

    header = file.read(80)
    num_of_tri = hex32_to_int(file.read(4))

    print(f"File: {header}")
    print(f"Triangles: {num_of_tri}")

    mesh = Mesh()
    mesh.vertexCount = num_of_tri * 3
    mesh.triangleCount = num_of_tri

    vertices = []
    for i in range(num_of_tri):
        triangle1 = file.read(50)
        # normal = struct.unpack("<3f", triangle1[0:12])

        vertex1 = struct.unpack("<3f", triangle1[12:24])
        vertex2 = struct.unpack("<3f", triangle1[24:36])
        vertex3 = struct.unpack("<3f", triangle1[36:48])
        vertices.extend((*vertex1, *vertex2, *vertex3))


    float_pointer = ffi.new(f"float[{len(vertices)}]")
    for i in range(len(vertices)):
        float_pointer[i] = vertices[i]

    mesh.vertices = float_pointer

    default_material = load_material_default()
    default_material.maps[0].color = get_color(0xA2A4A4FF)

    upload_mesh(mesh, False)


    return RobotBody(mesh, Path(file_path).stem, default_material)
