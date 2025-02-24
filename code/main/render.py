from typing import Any
from pyray import *  # type: ignore


class RenderLayer:
    def __init__(self, width: int, height: int, is_3D:bool, camera, background_color=get_color(0x00000000)):
        self.texture = load_render_texture(width, height)
        self.background_color = background_color
        self.camera = camera
        self.is_3D = is_3D
        
    def __enter__(self):
        begin_texture_mode(self.texture)
        clear_background(self.background_color)
        if (self.is_3D):
            begin_mode_3d(self.camera)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (self.is_3D):
            end_mode_3d()
        end_texture_mode()

    def draw(self):
        rect = Rectangle(0, 0, self.texture.texture.width, -self.texture.texture.height)
        draw_texture_rec(self.texture.texture, rect, Vector2(0, 0), get_color(0xFFFFFFFF))


class ShaderManager:
    def __init__(self, vs: str, fs: str):
        self.shader = load_shader(vs, fs)

    def __enter__(self):
        begin_shader_mode(self.shader)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_shader_mode()

    def set_locs(self, index:int, uniform:str):
        self.shader.locs[index] = get_shader_location(self.shader, uniform)

    def set_vector3_value(self, value:Vector3, uniform:str):
        type = ShaderUniformDataType.SHADER_UNIFORM_VEC3
        set_shader_value(self.shader, get_shader_location(self.shader, uniform), value, type)


