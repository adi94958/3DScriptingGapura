import bpy
import math

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

def main():
    object3D = Object3D()
    object3D.clear_scene()

    ## Membuat instance dari kelas-kelas objek geometri
    plane = Square("plane.001", 400, 600, 1, location=(0, 0, 0))
    
    for i in range(7):
        x_offset = i * 10
        tiangSquareKiri = Square("tiangSquareKiri.001", 8, 5, 50, location=(0,0, 0))
        tiangSquareKiri.translate_object(tiangSquareKiri.obj, 50 + x_offset, 100, 0)
        
    for i in range(5):
        y_offset = i * 12
        tiangCylinder = Cylinder("tiangCylinder", 2, 60, num_segments=64, location=(0, 0, 0))
        tiangCylinder.translate_object(tiangCylinder.obj, 103, 110 + y_offset, 0)
    
    for i in range(7):
        x_offset = i * 7
        tiangSquareKanan = Square("tiangSquareKanan.001", 3, 20, 100, location=(0,0, 0))
        tiangSquareKanan.translate_object(tiangSquareKanan.obj, 226 + x_offset, 100, 0)
        
    for i in range(7):
        x_offset = i * 8.3
        tiangSquareKanan = Square("tiangSquareKanan.001", 3, 20, 30, location=(0,0, 0))
        tiangSquareKanan.translate_object(tiangSquareKanan.obj, 268 + x_offset, 95, 0)
    
    for i in range(2):
        y_offset = i * 50
        ruangan = Square("ruangan.002", 68, 8, 60, location=(0, 0, 0))
        ruangan.translate_object(ruangan.obj, 226, 113 + y_offset, 0)
        
    ruangan = Square("ruangan.001", 3, 63.8, 60, location=(293, 107.2, 0))
    ruangan = Square("ruangan.001", 8, 27.8, 60, location=(226, 113, 0))
    planeAtap = Square("planeAtap.001", 130, 71, 5, location=(98, 100, 60))
    planeAtapRuangan = Square("planeAtapRuangan.001", 70, 65, 5, location=(226, 107.2, 60))
    
    #triangle = Triangle("segitiga" , 6, 4, 6, location=(10, 5, 0))
    #cylinder = Cylinder("tabung", 3, 10, num_segments=64, location=(4, 2, 4))
    #sphere = Sphere("bola", 2, num_segments=64, num_rings=32, location=(4, 10.5, 2))

    ## Rotasi objek
    #square.rotate_object(square.obj, 45, 0, 0)
    #triangle.rotate_object(triangle.obj, 0, 90, 0)
    #cylinder.rotate_object(cylinder.obj, 0, 0, 45)
    #sphere.rotate_object(sphere.obj, 30, 60, 90)

if __name__ == "__main__":
    main()