from pyray import *  # type: ignore

class RenderLayer:
    def __init__(self, width: int, height: int, clear_color: Color):
        self.texture = load_render_texture(width, height)
        self.clear_color = clear_color

    def __enter__(self):
        begin_texture_mode(self.texture)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_texture_mode()

    def draw(self):
        draw_texture_rec(
            self.texture.texture,
            Rectangle(0, 0, self.texture.texture.width, -self.texture.texture.height),
            Vector2(0, 0),
            WHITE
        )

class ShaderManager:
    def __init__(self, vs_path: str, fs_path: str):
        self.shader = load_shader(vs_path, fs_path)
        self._set_shader_locations()
        self.light_position = Vector3(-1.0, -1.0, -1.0)
        self.light_color = Vector3(1.0, 1.0, 1.0)
        self._configure_lighting()

    def _set_shader_locations(self):
        locs = [
            (ShaderLocationIndex.SHADER_LOC_MATRIX_MODEL, "model"),
            (ShaderLocationIndex.SHADER_LOC_MATRIX_VIEW, "view"),
            (ShaderLocationIndex.SHADER_LOC_MATRIX_PROJECTION, "projection"),
        ]
        for idx, name in locs:
            self.shader.locs[idx] = get_shader_location(self.shader, name)

    def _configure_lighting(self):
        set_shader_value(self.shader, get_shader_location(self.shader, "lightPosition"),
                        self.light_position, ShaderUniformDataType.SHADER_UNIFORM_VEC3)
        set_shader_value(self.shader, get_shader_location(self.shader, "lightColor"),
                        self.light_color, ShaderUniformDataType.SHADER_UNIFORM_VEC3)

    def __enter__(self):
        begin_shader_mode(self.shader)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_shader_mode()

class RobotArm:
    def __init__(self, link1, link2):
        self.link1 = link1
        self.link2 = link2

    def render(self):
        self.link1.render_link()
        self.link2.render_link()

class UIRenderer:
    def __init__(self, connection_status):
        self.connection_status = connection_status

    def render(self):
        draw_fps(10, 30)
        text = "ServoBot connected" if self.connection_status.is_connected else "ServoBot disconnected"
        color = get_color(0x14f06fff) if self.connection_status.is_connected else get_color(0xf0a727ff)
        draw_text(text, 10, 10, 20, color)

class RenderSystem:
    def __init__(self, width: int, height: int, camera: Camera3D, arm: RobotArm, sc):
        self.layers = {
            "world": RenderLayer(width, height, get_color(0x181818FF)),
            "xyz": RenderLayer(width, height, get_color(0x00000000)),
            "ui": RenderLayer(width, height, get_color(0x00000000)),
        }
        self.shader = ShaderManager("shaders/lighting.vs", "shaders/lighting.fs")
        self.camera = camera
        self.arm = arm
        self.ui_renderer = UIRenderer(sc)

    def _render_world_layer(self, point_to_follow: Vector3):
        with self.layers["world"]:
            clear_background(self.layers["world"].clear_color)
            with begin_mode_3d(self.camera):
                draw_grid()
                draw_sphere(point_to_follow, 0.13, get_color(0xffdd33FF))
                draw_line_3d(vector3_zero(), point_to_follow, WHITE)
                self.arm.render()
                with self.shader:
                    draw_cube(vector3_zero(), 1, 1, 1, get_color(0xFF0000FF))

    def _render_xyz_layer(self, point_to_follow: Vector3, xyz):
        with self.layers["xyz"]:
            clear_background(self.layers["xyz"].clear_color)
            with begin_mode_3d(self.camera):
                draw_xyz_control(point_to_follow, xyz, self.camera)

    def _render_ui_layer(self):
        with self.layers["ui"]:
            clear_background(self.layers["ui"].clear_color)
            self.ui_renderer.render()

    def render_frame(self, point_to_follow: Vector3, xyz):
        self._render_world_layer(point_to_follow)
        self._render_xyz_layer(point_to_follow, xyz)
        self._render_ui_layer()

        begin_drawing()
        clear_background(BLACK)
        for layer in self.layers.values():
            layer.draw()
        end_drawing()

# Usage example
if __name__ == "__main__":
    # Initialize components
    camera = Camera3D()
    arm = RobotArm(Link(), Link())  # Assume Link class exists
    sc = ConnectionStatus()         # Assume ConnectionStatus exists

    # Create render system
    renderer = RenderSystem(WIDTH, HEIGHT, camera, arm, sc)
    
    # In main loop
    while not window_should_close():
        # Update logic here
        renderer.render_frame(point_to_follow, xyz_controller)