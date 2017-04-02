from demosys.effects import effect
from demosys.opengl import geometry
from OpenGL import GL
from pyrr import matrix44


class DefaultEffect(effect.Effect):
    """Generated default efffect"""
    def init(self):
        self.shader = self.get_shader("default.glsl")
        self.cube = geometry.cube(4.0, 4.0, 4.0)

    @effect.bind_target
    def draw(self, time, target):
        GL.glEnable(GL.GL_DEPTH_TEST)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -4.0))

        # Apply the rotation and translation from the system camera
        m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Draw the cube
        self.cube.bind(self.shader)
        self.shader.uniform_mat4("m_proj", self.sys_camera.projection)
        self.shader.uniform_mat4("m_mv", m_mv)
        self.shader.uniform_mat3("m_normal", m_normal)
        self.cube.draw()
