from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


class ShaderProgram:

    @staticmethod
    def set_uniform_wrap(func, loc, is_matrix):
        # Wraps OpenGL uniform setters into consistent interface
        # The returned function only has value as parameter
        def wrapped(value):
            if is_matrix:
                return func(loc, 1, GL_FALSE, value)
            else:
                return func(loc, *value)

        return wrapped

    def __init__(self, shaders):
        # Compile shaders
        shaders = [compileShader(source, shader_type) for source, shader_type in shaders]
        # Compile program
        self.handle = compileProgram(*shaders)
        # Uniform references are stored in a dict, see register_uniform
        self.uniforms = {}

    def register_uniform(self, uniform_name, uniform_type):
        self.use()

        loc = glGetUniformLocation(self.handle, uniform_name)

        set_func = {
            '1f': ShaderProgram.set_uniform_wrap(glUniform1f, loc, False),
            '2f': ShaderProgram.set_uniform_wrap(glUniform2f, loc, False),
            '3f': ShaderProgram.set_uniform_wrap(glUniform3f, loc, False),
            '4f': ShaderProgram.set_uniform_wrap(glUniform4f, loc, False),
            'mat3f': ShaderProgram.set_uniform_wrap(glUniformMatrix3fv, loc, True),
            'mat4f': ShaderProgram.set_uniform_wrap(glUniformMatrix4fv, loc, True),
        }[uniform_type]

        self.uniforms[uniform_name] = (loc, uniform_type, set_func)
        self.unuse()
    
    def set_uniform(self, uniform_name, value):
        self.use()
        # Get according set function and upload value
        _, _, set_func = self.uniforms[uniform_name]
        set_func(value)
        self.unuse()

    def use(self):
        glUseProgram(self.handle)

    def unuse(self):
        glUseProgram(0)











