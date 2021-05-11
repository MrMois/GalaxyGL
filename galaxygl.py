import glfw
import numpy as np
from shader import ShaderProgram
from camera import Camera
from OpenGL.GL import *


class Engine:

    def __init__(self, width=800, height=600, resizable=False):

        assert glfw.init()

        self.width = width
        self.height = height

        assert not resizable and 'TODO'
        self.resizable = resizable

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

        self.window = glfw.create_window(width, height, 'Window', None, None)

        if not self.window:
            glfw.terminate()
            raise Exception('Could not create glfw window.')

        glfw.make_context_current(self.window)

        self.camera = Camera(self.width / self.height)

    def run_main_loop(self, exit_msg=True):

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glDrawArrays(GL_TRIANGLES, 0, 3)

            glfw.swap_buffers(self.window)

        glfw.terminate()

        if exit_msg:
            print('Exiting main loop.')


if __name__ == '__main__':

    engine = Engine()

    vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                0.0, 0.5, 0.0, 0.0, 0.0, 1.0]

    vertices = np.array(vertices, dtype=np.float32)

    with open('shaders/base.vert.glsl', 'r') as f:
        vert_src = f.read()

    with open('shaders/base.frag.glsl', 'r') as f:
        frag_src = f.read()

    shader = ShaderProgram([(vert_src, GL_VERTEX_SHADER), (frag_src, GL_FRAGMENT_SHADER)])

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader.handle, "a_position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

    color = glGetAttribLocation(shader.handle, "a_color")
    glEnableVertexAttribArray(color)
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    shader.register_uniform('viewMat', 'mat4f')
    shader.register_uniform('projMat', 'mat4f')

    engine.camera.update_view(position=[1, 1, 1], target=[0, 0, 0])

    shader.set_uniform('viewMat', engine.camera.view)
    shader.set_uniform('projMat', engine.camera.proj)

    shader.use()
    engine.run_main_loop()
