from pyray import *  # type: ignore


class RenderLayer:
    def __init__(self, width: int, height: int):
        self.texture = load_render_texture(width, height)

    def __enter__(self):
        begin_texture_mode(self.texture)
        return self

    def __exit__(self):
        end_texture_mode()
