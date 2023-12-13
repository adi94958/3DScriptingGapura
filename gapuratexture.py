import bpy
import math
from math import radians

def clear_scene():
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)

        for mtr in bpy.data.materials:
            bpy.data.materials.remove(mtr)

class Object3D:
    def __init__(self):
        self.objects = []  # Menyimpan referensi objek-objek yang dibuat

    def clear_scene(self):
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)

        for mtr in bpy.data.materials:
            bpy.data.materials.remove(mtr)

    def create_mesh_object(self, name, verts, faces, location=(0, 0, 0)):
        mesh_data = bpy.data.meshes.new(name)
        mesh_data.from_pydata(verts, [], faces)
        obj = bpy.data.objects.new(name, mesh_data)
        bpy.context.collection.objects.link(obj)
        obj.location = location
        self.objects.append(obj)  # Tambahkan objek ke dalam list objects
        return obj

    def translate_object(self, obj, translasi_x, translasi_y, translasi_z):
        obj.location.x = translasi_x
        obj.location.y = translasi_y
        obj.location.z = translasi_z

    def rotation_object(self, obj, rotation_x, rotation_y, rotation_z):
        sudut_rotasi_x = math.radians(rotation_x)
        sudut_rotasi_y = math.radians(rotation_y)
        sudut_rotasi_z = math.radians(rotation_z)
        obj.rotation_euler = (sudut_rotasi_x, sudut_rotasi_y, sudut_rotasi_z)

    def scale_object(self, obj, scale_x, scale_y, scale_z):
        obj.scale.x = scale_x
        obj.scale.y = scale_y
        obj.scale.z = scale_z
        

class Square(Object3D):
    def __init__(self, name, width, length, height, location=(0, 0, 0)):
        super().__init__()
        self.name = name
        self.width = width
        self.length = length
        self.height = height
        self.location = location
        self.create()

    def generate_square_verts(self):
        return [
            (0, 0, 0),
            (self.width, 0, 0),
            (self.width, self.length, 0),
            (0, self.length, 0),
            (0, 0, self.height),
            (self.width, 0, self.height),
            (self.width, self.length, self.height),
            (0, self.length, self.height),
        ]

    def generate_square_faces(self):
        return [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 3, 7, 4),
            (1, 2, 6, 5),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
        ]

    def create(self):
        square_verts = self.generate_square_verts()
        square_faces = self.generate_square_faces()
        self.obj = self.create_mesh_object(self.name, square_verts, square_faces, self.location)


class Triangle(Object3D):
    def __init__(self, name, width, length, height, location=(0, 0, 0)):
        super().__init__()
        self.name = name
        self.width = width
        self.length = length
        self.height = height
        self.location = location
        self.create()
                
    def generate_triangle_verts(self):
        return [
            (0, 0, 0),
            (self.width, 0, 0),
            (self.width, self.length, 0),
            (0, self.length, 0),
            (self.width, 0, self.height),
            (self.width, self.length, self.height),
        ]

    def generate_triangle_faces(self):
        return [
            (0, 1, 2, 3),
            (0, 4, 1),
            (3, 5, 2),
            (3, 0, 4, 5),
            (1, 2, 5, 4),
        ]

    def create(self):
        triangle_verts = self.generate_triangle_verts()
        triangle_faces = self.generate_triangle_faces()
        self.obj = self.create_mesh_object(self.name, triangle_verts, triangle_faces, self.location)


class Cylinder(Object3D):
    def __init__(self, name, radius, height, num_segments=32, location=(0, 0, 0)):
        super().__init__()
        self.name = name
        self.radius = radius
        self.height = height
        self.num_segments = num_segments
        self.location = location
        self.create()

    def generate_cylinder_verts(self):
        verts = []

        # Menambahkan verteks untuk lingkaran bagian bawah
        for i in range(self.num_segments):
            angle = 2 * math.pi * i / self.num_segments
            x = self.radius * math.cos(angle) + self.location[0]
            y = self.radius * math.sin(angle) + self.location[1]
            verts.append((x, y, self.location[2]))

        # Menambahkan verteks untuk lingkaran bagian atas
        for i in range(self.num_segments):
            angle = 2 * math.pi * i / self.num_segments
            x = self.radius * math.cos(angle) + self.location[0]
            y = self.radius * math.sin(angle) + self.location[1]
            verts.append((x, y, self.location[2] + self.height))

        return verts, self.generate_cylinder_faces()

    def generate_cylinder_faces(self):
        faces = []

        # Menambahkan wajah-wajah untuk bagian samping
        for i in range(self.num_segments):
            next_i = (i + 1) % self.num_segments
            # Wajah untuk bagian bawah
            faces.append((i, next_i, i + self.num_segments))
            # Wajah untuk bagian atas
            faces.append((i + self.num_segments, next_i + self.num_segments, next_i))
        
        # Menambahkan wajah untuk alas
        bottom_face = list(range(self.num_segments))
        faces.append(bottom_face)
        
        # Menambahkan wajah untuk alas atas
        top_face = list(range(self.num_segments, 2 * self.num_segments))
        faces.append(top_face)

        return faces
    
    def create(self):
        cylinder_verts, cylinder_faces = self.generate_cylinder_verts()
        self.obj = self.create_mesh_object(self.name, cylinder_verts, cylinder_faces, self.location)



class Sphere(Object3D):
    def __init__(self, name, radius, num_segments=32, num_rings=16, location=(0, 0, 0)):
        super().__init__()
        self.name = name
        self.radius = radius
        self.num_segments = num_segments
        self.num_rings = num_rings
        self.location = location
        self.create()

    def generate_sphere_verts(self):
        verts = []

        # Menambahkan verteks untuk bola
        for i in range(self.num_rings + 1):
            ring_angle = math.pi * i / self.num_rings
            y = self.radius * math.cos(ring_angle) + self.location[1]
            ring_radius = self.radius * math.sin(ring_angle)

            for j in range(self.num_segments):
                segment_angle = 2 * math.pi * j / self.num_segments
                x = ring_radius * math.cos(segment_angle) + self.location[0]
                z = ring_radius * math.sin(segment_angle) + self.location[2]
                verts.append((x, y, z))

        return verts, self.generate_sphere_faces()

    def generate_sphere_faces(self):
        faces = []

        # Menambahkan wajah untuk bola
        for i in range(self.num_rings):
            for j in range(self.num_segments):
                next_j = (j + 1) % self.num_segments
                next_i = i + 1

                current_index = i * self.num_segments + j
                next_index = i * self.num_segments + next_j
                next_ring_index = next_i * self.num_segments + j
                next_ring_next_index = next_i * self.num_segments + next_j

                faces.append((current_index, next_index, next_ring_next_index, next_ring_index))

        return faces

    def create(self):
        sphere_verts, sphere_faces = self.generate_sphere_verts()
        self.obj = self.create_mesh_object(self.name, sphere_verts, sphere_faces, self.location)
        
class Fence(Object3D):
    def __init__(self, name, width, length, heigth, size, cuts, thickness, location=(0, 0, 0)):
        super().__init__()
        self.name = name
        self.size = size
        self.cuts = cuts
        self.thickness = thickness
        self.location = location
        self.width = width
        self.length = length
        self.height = heigth
        self.obj = None
        self.create()

    def create_dynamic_plane(self):
        # Tambahkan plane
        bpy.ops.mesh.primitive_plane_add(size=self.size, location=self.location)

        # Resize dan rotasi plane
        bpy.ops.transform.resize(value=(self.width, self.length, self.height))
        bpy.ops.transform.rotate(value=radians(90), orient_axis='X')

        # Mode Edit
        bpy.ops.object.mode_set(mode='EDIT')

        # Subdivide plane dan poke face
        bpy.ops.mesh.subdivide(number_cuts=self.cuts)
        # bpy.ops.mesh.poke()

        # Konversi tris ke quads
        # bpy.ops.mesh.quads_convert_to_tris()
        # bpy.ops.mesh.tris_convert_to_quads()
        
        # Ubah nama
        bpy.context.active_object.name = self.name

        # Mode Object
        bpy.ops.object.mode_set(mode='OBJECT')

        # Tambahkan modifier wireframe
        bpy.ops.object.modifier_add(type='WIREFRAME')
        wireframe_modifier = bpy.context.object.modifiers["Wireframe"]
        wireframe_modifier.thickness = self.thickness
        wireframe_modifier.use_boundary = True
        bpy.ops.object.select_all(action='DESELECT')
        
    def translate_object(self, translasi_x, translasi_y, translasi_z):
        if self.obj is not None:
            super().translate_object(self.obj, translasi_x, translasi_y, translasi_z)
        else:
            print("Error: Fence object not created before translation.")

    def create(self):
        self.create_dynamic_plane()
        # Dapatkan referensi objek berdasarkan nama
        self.obj = bpy.data.objects.get(self.name)

        # Jika objek belum dibuat, berikan pesan kesalahan
        if self.obj is None:
            print(f"Error: Object with name '{self.name}' not found.")
        else:
            self.objects.append(self.obj)
            
def assign_texture_to_object(obj_name, texture_path):
    # Menggunakan objek yang sudah ada dengan nama yang diberikan
    obj = bpy.data.objects.get(obj_name)

    if obj:
        # Membuat Material untuk Objek
        material_obj = bpy.data.materials.new(name=f"{obj_name}_Material")
        obj.data.materials.append(material_obj)

        # Mengatur Texture Image untuk Material Objek
        image_texture = bpy.data.textures.new(name=f"{obj_name}_Texture", type='IMAGE')
        image_texture.image = bpy.data.images.load(texture_path)

        # Membuat Node Material
        material_obj.use_nodes = True
        nodes = material_obj.node_tree.nodes
        links = material_obj.node_tree.links

        # Hapus semua node yang ada
        for node in nodes:
            nodes.remove(node)

        # Tambahkan principled shader
        shader_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        shader_node.location = (0, 0)

        # Tambahkan image texture node
        texture_node = nodes.new(type='ShaderNodeTexImage')
        texture_node.location = (shader_node.location.x - 200, shader_node.location.y + 100)
        texture_node.image = image_texture.image

        # Tambahkan material output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (shader_node.location.x + 200, shader_node.location.y)

        # Hubungkan node-node
        links.new(shader_node.outputs["BSDF"], output_node.inputs["Surface"])
        links.new(texture_node.outputs["Color"], shader_node.inputs["Base Color"])

        # Menetapkan material pada objek
        obj.data.materials[0] = material_obj

        # Atur koordinat UV mapping
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Aktifkan Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Menampilkan hasil
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        # Mengembalikan objek yang telah diperbarui sebagai instance UpdatedObject
        return obj
    else:
        print(f"Objek dengan nama '{obj_name}' tidak ditemukan.")
        return None

import bpy

def join_objects_and_set_material(object_names, new_object_name, material_color):
    bpy.ops.object.select_all(action='DESELECT')
    
    for obj_name in object_names:
        bpy.data.objects[obj_name].select_set(True)
    
    bpy.context.view_layer.objects.active = bpy.data.objects[object_names[0]]
    bpy.ops.object.join()
    
    joined_object = bpy.context.active_object
    joined_object.name = new_object_name
    
    material = bpy.data.materials.new(name="Material")
    joined_object.data.materials.append(material)
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = material_color

def main():
    object3D = Object3D()
    object3D.clear_scene()

    ## Membuat instance dari kelas-kelas objek geometri
    plane = Square("plane.001", 50, 60, 0.1, location=(-7, -8, 0))
    
    for i in range(7):
        x_offset = i * 1
        tiangSquareKiri = Square("tiangSquareKiri.001", 0.8, 0.5, 5, location=(0,0, 0))
        tiangSquareKiri.translate_object(tiangSquareKiri.obj, 5 + x_offset, 10, 0)
        
#    Join Objek
    bpy.ops.object.select_all(action='DESELECT')
    objects_to_join = []
    for obj in bpy.context.scene.objects:
        if obj.name not in ['Camera','plane.001']:
            objects_to_join.append(obj)
            obj.select_set(True)

    bpy.context.view_layer.objects.active = objects_to_join[0]
    bpy.ops.object.join()   
    joined_object = bpy.context.active_object
    joined_object.name = "pagar kiri"
        
    for i in range(5):
        y_offset = i * 1.2
        tiangCylinder = Cylinder("tiangCylinder", 0.3, 6, num_segments=64, location=(0, 0, 0))
        tiangCylinder.translate_object(tiangCylinder.obj, 10.3, 11 + y_offset, 0)
    
    #    Join Objek
    bpy.ops.object.select_all(action='DESELECT')
    objects_to_join = []
    for obj in bpy.context.scene.objects:
        if obj.name not in ['Camera','plane.001','pagar kiri']:
            objects_to_join.append(obj)
            obj.select_set(True)

    bpy.context.view_layer.objects.active = objects_to_join[0]
    bpy.ops.object.join()   
    joined_object = bpy.context.active_object
    joined_object.name = "tiang kiri"
    
    for i in range(7):
        x_offset = i * 0.7
        tiangSquareKanan = Square("tiangSquareKanan.001", 0.3, 2, 10, location=(0,0, 0))
        tiangSquareKanan.translate_object(tiangSquareKanan.obj, 22.6 + x_offset, 10, 0)
        
    #    Join Objek
    bpy.ops.object.select_all(action='DESELECT')
    objects_to_join = []
    for obj in bpy.context.scene.objects:
        if obj.name not in ['Camera','plane.001','pagar kiri', 'tiang kiri']:
            objects_to_join.append(obj)
            obj.select_set(True)

    bpy.context.view_layer.objects.active = objects_to_join[0]
    bpy.ops.object.join()   
    joined_object = bpy.context.active_object
    joined_object.name = "pagar kanan"
        
    for i in range(7):
        x_offset = i * 0.83
        tiangSquareKanan = Square("tiangSquareKanan.001", 0.3, 2, 3, location=(0,0, 0))
        tiangSquareKanan.translate_object(tiangSquareKanan.obj, 26.8 + x_offset, 9.5, 0)
        
    #    Join Objek
    bpy.ops.object.select_all(action='DESELECT')
    objects_to_join = []
    for obj in bpy.context.scene.objects:
        if obj.name not in ['Camera','plane.001','pagar kiri', 'tiang kiri', 'pagar kanan']:
            objects_to_join.append(obj)
            obj.select_set(True)

    bpy.context.view_layer.objects.active = objects_to_join[0]
    bpy.ops.object.join()   
    joined_object = bpy.context.active_object
    joined_object.name = "pagar kanan2"
    
    for i in range(2):
        y_offset = i * 5
        ruangan = Square("ruangan.002", 6.8, 0.8, 6, location=(0, 0, 0))
        ruangan.translate_object(ruangan.obj, 22.6, 11.3 + y_offset, 0)
        
    ruangan = Square("ruangan.003", 0.3, 6.38, 6, location=(29.3, 10.72, 0))
    ruangan = Square("ruangan.004", 0.8, 2.78, 6, location=(22.6, 11.3, 0))
    ruangan = Square("ruangan.005", 0.8, 2.78, 2.9, location=(22.6, 13.8, 3.5))
    
    #    Join Objek
    bpy.ops.object.select_all(action='DESELECT')
    objects_to_join = []
    for obj in bpy.context.scene.objects:
        if obj.name not in ['Camera','plane.001','pagar kiri', 'tiang kiri', 'pagar kanan', 'pagar kanan2']:
            objects_to_join.append(obj)
            obj.select_set(True)

    bpy.context.view_layer.objects.active = objects_to_join[0]
    bpy.ops.object.join()   
    joined_object = bpy.context.active_object
    joined_object.name = "ruangan"
    
    
    planeAtap = Square("planeAtap.001", 13, 7.22, 0.5, location=(9.8, 10, 6))
    planeAtapRuangan = Square("planeAtapRuangan.001", 7, 6.5, 0.5, location=(22.6, 10.72, 6))
    
    #    Join Objek
    bpy.ops.object.select_all(action='DESELECT')
    objects_to_join = []
    for obj in bpy.context.scene.objects:
        if obj.name not in ['Camera','plane.001','pagar kiri', 'tiang kiri', 'pagar kanan', 'pagar kanan2', 'ruangan']:
            objects_to_join.append(obj)
            obj.select_set(True)

    bpy.context.view_layer.objects.active = objects_to_join[0]
    bpy.ops.object.join()   
    joined_object = bpy.context.active_object
    joined_object.name = "atap"
    
    bpy.ops.object.select_all(action='DESELECT')
#   BIKIN PAGER
    size_fence = 3.5
    fence_instance = Fence(name="PagarBesi", width=3, length=1, heigth=1.2, size=size_fence, cuts=10, thickness=0.1, location=(0, 0, 0))
    fence_instance.translate_object(17.2, 10.7, size_fence/2)
    
    size_fence = 4
    PagarBesiKiri = Fence(name="PagarBesiKiri", width=2.8, length=1, heigth=1.2, size=size_fence, cuts=10, thickness=0.4, location=(0, 0, 0))
    PagarBesiKiri.translate_object(-0.8, 10.25, size_fence/2)
    PagarBesiKanan = Fence(name="PagarBesiKanan", width=3.1, length=1, heigth=1.2, size=size_fence, cuts=10, thickness=0.4, location=(0, 0, 0))
    PagarBesiKanan.translate_object(36, 11.7, size_fence/2)
    
    
    #taman
    balok1 = Square("balok.001", 0.6, 3.6, 0.8, location=(0.8, 1, 0))
    balok2 = Square("balok.002", 0.6, 3.6, 0.8, location=(3.8, 1, 0)) 
    balok3 = Square("balok.003", 0.6, 3.6, 0.8, location=(0.8, 1.6, 0))
    balok3.rotation_object(balok3.obj, 0, 0, -90)
    balok4 = Square("balok.004", 0.6, 3.6, 0.8, location=(0.8, 4.6, 0))
    balok4.rotation_object(balok4.obj, 0, 0, -90)
    kubus = Square("kubus", 0.9, 0.9, 1.4, location=(2.2, 2.35, 0))
    meja = Square("meja", 2, 2, 0.05, location=(1.6, 1.75, 1.4))
    tiang = Square("tiang", 0.4, 0.4, 3.5, location=(2.45, 2.55, 1.4))
    bunga1 = Square("bunga.001", 0.15, 0.15, 2.5, location=(2.6, 2.85, 2.3))
    bunga1.rotation_object(bunga1.obj, 45, 0, 0)
    bunga2 = Square("bunga.002", 0.15, 0.15, 2.2, location=(2.6, 2.85, 1.4))
    bunga2.rotation_object(bunga2.obj, 28, 0, 0)
    bunga3 = Square("bunga.003", 0.15, 0.15, 0.8, location=(2.6, 1.65, 3.7))
    bunga3.rotation_object(bunga3.obj, -45, 0, 0)
    bunga4 = Square("bunga.004", 0.15, 0.15, 0.8, location=(2.6, 2.4, 2.3))
    bunga4.rotation_object(bunga4.obj, 65, 0, 0)
    bunga5 = Square("bunga.005", 0.15, 0.15, 0.6, location=(2.6, 1.7, 2.62))
    bunga5.rotation_object(bunga5.obj, 45, 0, 0)
    
    # meja duduk
    bpy.ops.object.select_all(action='DESELECT')
    for i in range(1, 5):
        bpy.data.objects[f'balok.{str(i).zfill(3)}'].select_set(True)

    bpy.context.view_layer.objects.active = bpy.data.objects['balok.001']

    bpy.ops.object.join()
    bpy.ops.object.duplicate(linked=False)
    balok = bpy.context.view_layer.objects.active

    # Use the Object3D methods directly on the balok instance
    object3D.scale_object(balok, 0.5, 0.5, 0.5)
    object3D.translate_object(balok, 1.75, 1.9, 4.5)

    bpy.ops.object.select_all(action='DESELECT')
    for i in range(1, 6):
        bpy.data.objects[f'bunga.{str(i).zfill(3)}'].select_set(True)

    bpy.context.view_layer.objects.active = bpy.data.objects['bunga.001']

    bpy.ops.object.join()
    bpy.ops.object.duplicate(linked=False)
    bunga = bpy.context.view_layer.objects.active

    object3D.translate_object(bunga, 2.7, 2.9, 3.3)
    object3D.rotation_object(bunga, 45, 0, 180)

    bpy.ops.object.select_all(action='DESELECT')
    for i in range(1, 3):
        bpy.data.objects[f'bunga.{str(i).zfill(3)}'].select_set(True)
    bpy.data.objects[f'balok.002'].select_set(True)
    bpy.data.objects[f'tiang'].select_set(True)
    bpy.data.objects[f'meja'].select_set(True)
    bpy.data.objects[f'tiang'].select_set(True)
    bpy.data.objects[f'kubus'].select_set(True)
    bpy.data.objects[f'balok.001'].select_set(True)

    bpy.context.view_layer.objects.active = bpy.data.objects['meja']

    bpy.ops.object.join()
    bpy.data.objects[f'meja'].select_set(True)
    meja = bpy.context.view_layer.objects.active
    object3D.translate_object(meja, 27.5, 23.0, 1.2)
    
    #duplikat meja duduk
    bpy.ops.object.join()
    bpy.ops.object.duplicate(linked=False)
    meja = bpy.context.view_layer.objects.active

    object3D.translate_object(meja, 36.0, 23.0, 1.2)
    
    # end meja duduk
    
    
    #jalan dan bunderan
    jalan1 = Square("jalan.001", 10.3, 60.0, 0.1, location=(12, -8, 0))
    jalan2 = Square("jalan.002", 50, 10.3, 0.1, location=(-7, 30, 0))
    bunderan1 = Cylinder("bunderan.001", 8, 0.1, num_segments=64, location=(8.6, 17.55, 0))
    bunderan2 = Cylinder("bunderan.002", 3.5, 1, num_segments=64, location=(8.6, 17.55, 0))
    
    
    assign_texture_to_object("meja", "D:/images/Wood.jpg")
    assign_texture_to_object("meja.001", "D:/images/Wood.jpg")
    assign_texture_to_object("jalan.001", "D:/images/Stone.jpg")
    assign_texture_to_object("jalan.002", "D:/images/Stone.jpg")
    assign_texture_to_object("plane.001", "D:/PavingStones128_1K-JPG/PavingStones128_1K-JPG_Color.jpg")
        
    # Join and set material for "putih"
    join_objects_and_set_material(['atap', 'bunderan.002', 'ruangan', 'tiang kiri'], "putih", (1, 1, 1, 1))

    # Join and set material for "tembok"
    join_objects_and_set_material(['pagar kanan', 'pagar kiri', 'pagar kanan2'], "tembok", (255/255, 255/255, 185/255, 1))

    # Join and set material for "PagarBesi"
    join_objects_and_set_material(['PagarBesi', 'PagarBesiKanan', 'PagarBesiKiri'], "PagarBesi", (0, 0, 0, 1))
    
    # Deselect semua objek
    bpy.ops.object.select_all(action='DESELECT')
    
    #bpy.ops.curve.tree_add(do_update=True, chooseSet='0', bevel=True, prune=False, showLeaves=True, useArm=False, seed=0, handleType='0', levels=2, length=(0.8, 0.6, 0.5, 0.1), lengthV=(0, 0.1, 0, 0), taperCrown=0.5, branches=(0, 55, 10, 1), curveRes=(8, 5, 3, 1), curve=(0, -15, 0, 0), curveV=(20, 50, 75, 0), curveBack=(0, 0, 0, 0), baseSplits=3, segSplits=(0.1, 0.5, 0.2, 0), splitByLen=True, rMode='rotate', splitAngle=(18, 18, 22, 0), splitAngleV=(5, 5, 5, 0), scale=60, scaleV=2, attractUp=(3.5, -1.89984, 0, 0), attractOut=(0, 0.8, 0, 0), shape='6', shapeS='10', customShape=(1, 1, 0.1, 0.5), branchDist=1.5, nrings=0, baseSize=0.3, baseSize_s=0.16, splitHeight=0.2, splitBias=0.55, ratio=0.015, minRadius=0.0015, closeTip=False, rootFlare=1, autoTaper=True, taper=(1, 1, 1, 1), radiusTweak=(1, 1, 1, 1), ratioPower=1.2, downAngle=(0, 26.21, 52.56, 30), downAngleV=(0, 10, 10, 10), useOldDownAngle=True, useParentAngle=True, rotate=(99.5, 137.5, 137.5, 137.5), rotateV=(15, 0, 0, 0), scale0=1, scaleV0=0.1, pruneWidth=0.34, pruneBase=0.12, pruneWidthPeak=0.5, prunePowerHigh=0.5, prunePowerLow=0.001, pruneRatio=0.75, leaves=150, leafDownAngle=30, leafDownAngleV=-10, leafRotate=137.5, leafRotateV=15, leafScale=3, leafScaleX=0.2, leafScaleT=0.1, leafScaleV=0.15, leafShape='hex', bend=0, leafangle=-12, horzLeaves=True, leafDist='6', bevelRes=1, resU=4, armAnim=False, previewArm=False, leafAnim=False, frameRate=1, loopFrames=0, wind=1, gust=1, gustF=0.075, af1=1, af2=1, af3=4, makeMesh=False, armLevels=2, boneStep=(1, 1, 1, 1))
    


    
if __name__ == "__main__":
    main()