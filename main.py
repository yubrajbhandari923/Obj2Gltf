import pygltflib
import numpy as np
import trimesh
import os
class Obj2Gltf:
    def __init__(self, obj_path, gltf_path):
        self.obj_path = obj_path
        self.gltf_path = gltf_path
        self.gltf = pygltflib.GLTF2()
        self.scene = pygltflib.Scene()
        self.gltf.scenes.append(self.scene)
        self.gltf.scene = 0

        self.byteLength = 0

        # Check if obj_path is a file or folder
        if obj_path.endswith('.obj'):
            self.obj2gltf()
        else:
            self.obj_folder2gltf()

        self.add_buffer()


    def load_obj(self):
        self.obj = trimesh.load(self.obj_path)
        self.vertices = np.array(self.obj.vertices, dtype=np.float32)
        self.faces = np.array(self.obj.faces, dtype=np.uint32)

    def add_buffer(self):
        self.gltf.set_binary_blob(self.gltf.binary_blob() + self.vertices.tobytes() + self.faces.tobytes())
        self.byteLength += self.vertices.nbytes + self.faces.nbytes

    
    def add_buffer_view(self):
        self.gltf.bufferViews.append(pygltflib.BufferView(
            buffer=0,
            byteOffset=self.byteLength,
            byteLength=self.vertices.nbytes,
            target=pygltflib.TARGET_ARRAY_BUFFER,
        ))
        self.gltf.bufferViews.append(pygltflib.BufferView(
            buffer=0,
            byteOffset=self.byteLength + self.vertices.nbytes,
            byteLength=self.faces.nbytes,
            target=pygltflib.TARGET_ELEMENT_ARRAY_BUFFER,
        ))

    def add_accessor(self):
        self.gltf.accessors.append(pygltflib.Accessor(
            bufferView=len(self.gltf.bufferViews) - 2,
            byteOffset=self.byteLength,
            componentType=pygltflib.FLOAT,
            count=len(self.vertices),
            type=pygltflib.VEC3,
        ))
        self.gltf.accessors.append(pygltflib.Accessor(
            bufferView=len(self.gltf.bufferViews) - 1,
            byteOffset=self.byteLength +self.vertices.nbytes,
            componentType=pygltflib.UNSIGNED_INT,
            count=len(self.faces) * 3,
            type=pygltflib.SCALAR,
        ))
    
    def add_material(self):
        material = pygltflib.Material(
            pbrMetallicRoughness=pygltflib.PbrMetallicRoughness(
                baseColorFactor=[1.0, 0.0, 0.0, 1.0],
            ),
        )
        self.gltf.materials.append(material)
    
    def add_node(self):
        node = pygltflib.Node(
            mesh=len(self.gltf.meshes) - 1,
        )
        self.scene.nodes.append(node)
        self.gltf.nodes.append(node)
    
    def add_mesh(self):
        mesh = pygltflib.Mesh()
        mesh.primitives.append(pygltflib.Primitive(
            attributes=pygltflib.Attributes(
                POSITION=len(self.gltf.accessors) - 2,
            ),
            indices=len(self.gltf.accessors) - 1,
            material=0,
        ))
        self.gltf.meshes.append(mesh)
    
    def __del__(self):
        buffer = pygltflib.Buffer(
            byteLength=self.byteLength,
        )
        self.gltf.buffers.append(buffer)
        self.gltf.save(self.gltf_path)
    
        

Obj2Gltf('test.obj', 'test.gltf')