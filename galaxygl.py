import glfw
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

    def run_main_loop(self):

        while not glfw.window_should_close(self.window):
            glfw.poll_events()


if __name__ == '__main__':

    engine = Engine()
    engine.run_main_loop()
