import pygltflib
import numpy as np
import trimesh

class Obj2Gltf:
    def __init__(self, obj_path, gltf_path):
        self.obj_path = obj_path
        self.gltf_path = gltf_path
        self.gltf = pygltflib.GLTF2()
        self.gltf.scene = 0
        self.gltf.scenes.append(pygltflib.Scene())

        self.obj = trimesh.load(self.obj_path)
        self.vertices = self.obj.vertices
        self.faces = self.obj.faces
        

Obj2Gltf('test.obj', 'test.gltf')