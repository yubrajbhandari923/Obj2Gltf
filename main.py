import pygltflib
import numpy as np
import trimesh

class Obj2Gltf:
    def __init__(self, obj_path, gltf_path):
        self.obj_path = obj_path
        self.gltf_path = gltf_path
        self.gltf = pygltflib.GLTF2()
        self.scene = pygltflib.Scene()
        self.gltf.scenes.append(self.scene)
        self.gltf.scene = 0

        self.obj = trimesh.load(self.obj_path)
        self.vertices = np.array(self.obj.vertices, dtype=np.float32)
        self.faces = np.array(self.obj.faces, dtype=np.uint32)

    def 
    
    
        

Obj2Gltf('test.obj', 'test.gltf')