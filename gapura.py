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
        
    def rotate_object(self, obj, rotation_x, rotation_y, rotation_z):
        sudut_rotasi_x = math.radians(rotation_x)
        sudut_rotasi_y = math.radians(rotation_y)
        sudut_rotasi_z = math.radians(rotation_z)
        
        obj.rotation_euler = (sudut_rotasi_x, sudut_rotasi_y, sudut_rotasi_z)
        
    

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
    def __init__(self, name, size, cuts, thickness, location=(0, 0, 0)):
        super().__init__()
        self.name = name
        self.size = size
        self.cuts = cuts
        self.thickness = thickness
        self.location = location
        self.obj = None
        self.create()

    def create_dynamic_plane(self):
        # Tambahkan plane
        bpy.ops.mesh.primitive_plane_add(size=self.size, location=self.location)

        # Resize dan rotasi plane
        bpy.ops.transform.resize(value=(4.2, 1, 1))
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


def main():
    object3D = Object3D()
    object3D.clear_scene()

    ## Membuat instance dari kelas-kelas objek geometri
    plane = Square("plane.001", 400, 600, 1, location=(0, 0, 0))
    
    for i in range(7):
        x_offset = i * 10
        tiangSquareKiri = Square("tiangSquareKiri.001", 8, 5, 50, location=(0,0, 0))
        tiangSquareKiri.translate_object(tiangSquareKiri.obj, 50 + x_offset, 100, 0)
        
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
        y_offset = i * 12
        tiangCylinder = Cylinder("tiangCylinder", 2, 60, num_segments=64, location=(0, 0, 0))
        tiangCylinder.translate_object(tiangCylinder.obj, 103, 110 + y_offset, 0)
    
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
        x_offset = i * 7
        tiangSquareKanan = Square("tiangSquareKanan.001", 3, 20, 100, location=(0,0, 0))
        tiangSquareKanan.translate_object(tiangSquareKanan.obj, 226 + x_offset, 100, 0)\
        
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
        x_offset = i * 8.3
        tiangSquareKanan = Square("tiangSquareKanan.001", 3, 20, 30, location=(0,0, 0))
        tiangSquareKanan.translate_object(tiangSquareKanan.obj, 268 + x_offset, 95, 0)
        
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
        y_offset = i * 50
        ruangan = Square("ruangan.002", 68, 8, 60, location=(0, 0, 0))
        ruangan.translate_object(ruangan.obj, 226, 113 + y_offset, 0)
        
    ruangan = Square("ruangan.001", 3, 63.8, 60, location=(293, 107.2, 0))
    ruangan = Square("ruangan.001", 8, 27.8, 60, location=(226, 113, 0))
    
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
    
    
    planeAtap = Square("planeAtap.001", 130, 71, 5, location=(98, 100, 60))
    planeAtapRuangan = Square("planeAtapRuangan.001", 70, 65, 5, location=(226, 107.2, 60))
    
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
    size_fence = 25
    fence_instance = Fence(name="PagarBesi", size=size_fence, cuts=10, thickness=0.4, location=(170, 107, size_fence/2))
#    fence_instance.translate_object(170, 107, 25/2)
if __name__ == "__main__":
    main()