from pathlib import Path
from typing import Optional
from cffi import FFI
from models import *  # type: ignore
from pyray import *  # type: ignore
import struct


def hex32_to_int(data):
    return int.from_bytes(data, byteorder="little")


def load_stl_mesh(file_path:str, color:int=0xFFFFFFFF, shader:Optional[Shader] = None) -> RobotPart:
    file = open(file_path + ".stl", 'rb')

    header = file.read(80)
    num_of_tri = hex32_to_int(file.read(4))

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

    default_material = load_material_default()

    if (shader):
        default_material.shader = shader

    default_material.maps[0].color = RED

    upload_mesh(mesh, True)
    return RobotPart(Path(file_path).stem, mesh, default_material)