import pygltflib
import numpy as np
import trimesh
import os
class Obj2Gltf:
    def __init__(self, obj_path, gltf_path=None, exclude_list=[]):
        self.obj_path = obj_path
        self.gltf_path = gltf_path
        self.gltf = pygltflib.GLTF2()
        self.scene = pygltflib.Scene()
        self.gltf.scenes.append(self.scene)
        self.gltf.scene = 0
        self.byteLength = 0
        self.path_is_file = True
        self.exclude_list = exclude_list
        self.folder_name = ""

        self.gltf.set_binary_blob(b'')
        self.gltf.asset = pygltflib.Asset(version='2.0')

        # Check if obj_path is a file or folder
        if obj_path.endswith('.obj'):
            self.obj_file()
        else:
            self.obj_folder2gltf()

        self.add_buffer()
    
    def obj_file(self):
        self.load_obj()
        self.add_buffer_view()
        self.add_accessor()
        # self.add_material()
        self.add_mesh()
        self.add_node()
        self.add_buffer()

    def obj_folder2gltf(self):
        self.path_is_file = False
        self.folder_name = self.obj_path
        for file in os.listdir(self.obj_path):
            if file.endswith('.obj') and file not in self.exclude_list:
                self.obj_path = os.path.join(self.folder_name, file)
                self.obj_file()

    def load_obj(self):
        print(f'Loading {self.obj_path}')
        self.obj = trimesh.load(self.obj_path)
        self.vertices = np.array(self.obj.vertices, dtype="float32")
        self.faces = np.array(self.obj.faces, dtype="uint32")

        self.vertices_blob = self.vertices.tobytes()
        self.faces_blob = self.faces.flatten().tobytes()

    def add_buffer(self):
        self.gltf.set_binary_blob( self.vertices.tobytes() + self.faces.flatten().tobytes())
        self.byteLength += self.vertices.nbytes + self.faces.nbytes
    
    def add_buffer_view(self):
        """ Caution: This function should be called before add_buffer() to get the correct byteOffset"""
        self.gltf.bufferViews.append(pygltflib.BufferView(
            buffer=0,
            byteOffset=self.byteLength, 
            byteLength=len(self.vertices.tobytes()),
            # target=pygltflib.ARRAY_BUFFER,
        ))
        self.gltf.bufferViews.append(pygltflib.BufferView(
            buffer=0,
            byteOffset=self.byteLength + len(self.vertices.tobytes()),
            byteLength=len(self.faces.tobytes()),
            # target=pygltflib.ELEMENT_ARRAY_BUFFER,
        ))

    def add_accessor(self):
        """ Caution: This function should be called before add_buffer() to get the correct byteOffset"""
        self.gltf.accessors.append(pygltflib.Accessor(
            bufferView=len(self.gltf.bufferViews) - 2,
            # byteOffset=self.byteLength,
            componentType=pygltflib.FLOAT,
            count=len(self.vertices),
            type=pygltflib.VEC3,
            max=self.vertices.max(axis=0).tolist(),
            min=self.vertices.min(axis=0).tolist(),

        ))
        self.gltf.accessors.append(pygltflib.Accessor(
            bufferView=len(self.gltf.bufferViews) - 1,
            # byteOffset=self.byteLength +lenself.vertices.nbytes,
            componentType=pygltflib.UNSIGNED_INT,
            count=self.faces.size,
            type=pygltflib.SCALAR,
            # max=[int(self.faces.max())],
            # min=[int(self.faces.min())],

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
        self.gltf.nodes.append(node)
        self.scene.nodes.append(len(self.gltf.nodes) - 1)
    
    def add_mesh(self):
        mesh = pygltflib.Mesh()
        mesh.primitives.append(pygltflib.Primitive(
            attributes=pygltflib.Attributes(
                POSITION=len(self.gltf.accessors) - 2,
            ),
            indices=len(self.gltf.accessors) - 1,
            # material=0,
        ))
        if not self.path_is_file:
            mesh.name = self.obj_path.split('/')[-1].replace('.obj', '')
        else:
            mesh.name = self.obj_path.replace('.obj', '')
        self.gltf.meshes.append(mesh)
    
    def __del__(self):
        buffer = pygltflib.Buffer(
            byteLength=self.vertices.nbytes + self.faces.nbytes,
        )
        self.gltf.buffers.append(buffer)
        if not self.gltf_path is None:
            self.gltf.save(self.gltf_path)
        else:
            if self.is_path_file:
                self.gltf.save(self.obj_path.replace('.obj', '.gltf'))
            else:
                self.gltf.save(os.path.join(self.folder_name, '_model.gltf'))
        # pygltflib.validator.validate(self.gltf)
        # pygltflib.validator.summary(self.gltf)

    
        

Obj2Gltf('Patient_obj/liver.obj', 'test.gltf', exclude_list=["Body_Filled.obj", "Skin.obj", "Visceral_fat.obj", "Subcutaneous_fat.obj", "Muscles.obj"])