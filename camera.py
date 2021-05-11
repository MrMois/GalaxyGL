import numpy as np
from pyrr.matrix44 import create_look_at, create_perspective_projection


class Camera:

    def __init__(self,
                 aspect,
                 y_fov=60.0,
                 z_near=0.01,
                 z_far=1000.0,
                 position=np.array([0, 0, 1]),
                 target=np.array([0, 0, -1]),
                 up_dir=np.array([0, 1, 0]),):

        self.aspect = aspect
        self.y_fov = y_fov
        self.z_near = z_near
        self.z_far = z_far
        self.position = position
        self.target = target
        self.up_dir = up_dir

        self.view = self.update_view()
        self.proj = self.update_proj()

    def update_view(self, position=None, target=None, up_dir=None):

        if position:
            self.position = position
        if target:
            self.target = target
        if up_dir:
            self.up_dir = up_dir

        self.view = create_look_at(self.position, self.target, self.up_dir)

        return self.view

    def update_proj(self):

        self.proj = create_perspective_projection(self.y_fov, self.aspect, self.z_near, self.z_far)

        return self.proj





    
