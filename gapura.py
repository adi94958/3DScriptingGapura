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


def main():
    object3D = Object3D()
    object3D.clear_scene()

    ## Membuat instance dari kelas-kelas objek geometri
    plane = Square("plane.001", 500, 600, 1, location=(-70, -80, 0))
    
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
        tiangCylinder = Cylinder("tiangCylinder", 3, 60, num_segments=64, location=(0, 0, 0))
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
        
    ruangan = Square("ruangan.003", 3, 63.8, 60, location=(293, 107.2, 0))
    ruangan = Square("ruangan.004", 8, 27.8, 60, location=(226, 113, 0))
    ruangan = Square("ruangan.005", 8, 27.8, 29, location=(226, 138, 35))
    
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
    
    
    planeAtap = Square("planeAtap.001", 130, 72.2, 5, location=(98, 100, 60))
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
    size_fence = 35
    fence_instance = Fence(name="PagarBesi", width=3, length=1, heigth=1.2, size=size_fence, cuts=20, thickness=0.4, location=(0, 0, 0))
    fence_instance.translate_object(172, 107, size_fence/2)
    
    bpy.ops.curve.tree_add(do_update=True, chooseSet='0', bevel=True, prune=False, showLeaves=True, useArm=False, seed=0, handleType='0', levels=2, length=(0.8, 0.6, 0.5, 0.1), lengthV=(0, 0.1, 0, 0), taperCrown=0.5, branches=(0, 55, 10, 1), curveRes=(8, 5, 3, 1), curve=(0, -15, 0, 0), curveV=(20, 50, 75, 0), curveBack=(0, 0, 0, 0), baseSplits=3, segSplits=(0.1, 0.5, 0.2, 0), splitByLen=True, rMode='rotate', splitAngle=(18, 18, 22, 0), splitAngleV=(5, 5, 5, 0), scale=60, scaleV=2, attractUp=(3.5, -1.89984, 0, 0), attractOut=(0, 0.8, 0, 0), shape='6', shapeS='10', customShape=(1, 1, 0.1, 0.5), branchDist=1.5, nrings=0, baseSize=0.3, baseSize_s=0.16, splitHeight=0.2, splitBias=0.55, ratio=0.015, minRadius=0.0015, closeTip=False, rootFlare=1, autoTaper=True, taper=(1, 1, 1, 1), radiusTweak=(1, 1, 1, 1), ratioPower=1.2, downAngle=(0, 26.21, 52.56, 30), downAngleV=(0, 10, 10, 10), useOldDownAngle=True, useParentAngle=True, rotate=(99.5, 137.5, 137.5, 137.5), rotateV=(15, 0, 0, 0), scale0=1, scaleV0=0.1, pruneWidth=0.34, pruneBase=0.12, pruneWidthPeak=0.5, prunePowerHigh=0.5, prunePowerLow=0.001, pruneRatio=0.75, leaves=150, leafDownAngle=30, leafDownAngleV=-10, leafRotate=137.5, leafRotateV=15, leafScale=3, leafScaleX=0.2, leafScaleT=0.1, leafScaleV=0.15, leafShape='hex', bend=0, leafangle=-12, horzLeaves=True, leafDist='6', bevelRes=1, resU=4, armAnim=False, previewArm=False, leafAnim=False, frameRate=1, loopFrames=0, wind=1, gust=1, gustF=0.075, af1=1, af2=1, af3=4, makeMesh=False, armLevels=2, boneStep=(1, 1, 1, 1))
    size_fence = 40
    PagarBesiKiri = Fence(name="PagarBesiKiri", width=2.8, length=1, heigth=1.2, size=size_fence, cuts=10, thickness=4, location=(0, 0, 0))
    PagarBesiKiri.translate_object(-8, 102.5, size_fence/2)
    PagarBesiKanan = Fence(name="PagarBesiKanan", width=3.1, length=1, heigth=1.2, size=size_fence, cuts=10, thickness=4, location=(0, 0, 0))
    PagarBesiKanan.translate_object(360, 117, size_fence/2)
    
    #taman
    balok1 = Square("balok.001", 6, 36, 8, location=(8, 10, 0))
    balok2 = Square("balok.002", 6, 36, 8, location=(38, 10, 0)) 
    balok3 = Square("balok.003", 6, 36, 8, location=(8, 16, 0))
    balok3.rotation_object(balok3.obj, 0, 0, -90)
    balok4 = Square("balok.004", 6, 36, 8, location=(8, 46, 0))
    balok4.rotation_object(balok4.obj, 0, 0, -90)
    kubus = Square("kubus", 9, 9, 14, location=(22, 23.5, 0))
    meja = Square("meja", 20, 20, 0.5, location=(16, 17.5, 14))
    tiang = Square("tiang", 4, 4, 35, location=(24.5, 25.5, 14))
    bunga1 = Square("bunga.001", 1.5, 1.5, 25, location=(26, 28.5, 23))
    bunga1.rotation_object(bunga1.obj, 45, 0, 0)
    bunga2 = Square("bunga.002", 1.5, 1.5, 22, location=(26, 28.5, 14))
    bunga2.rotation_object(bunga2.obj, 28, 0, 0)
    bunga3 = Square("bunga.003", 1.5, 1.5, 8, location=(26, 16.5, 37))
    bunga3.rotation_object(bunga3.obj, -45, 0, 0)
    bunga4 = Square("bunga.004", 1.5, 1.5, 8, location=(26, 24, 23))
    bunga4.rotation_object(bunga4.obj, 65, 0, 0)
    bunga5 = Square("bunga.005", 1.5, 1.5, 6, location=(26, 17, 26.2))
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
    object3D.translate_object(balok, 17.5, 19, 45)

    bpy.ops.object.select_all(action='DESELECT')
    for i in range(1, 6):
        bpy.data.objects[f'bunga.{str(i).zfill(3)}'].select_set(True)

    bpy.context.view_layer.objects.active = bpy.data.objects['bunga.001']

    bpy.ops.object.join()
    bpy.ops.object.duplicate(linked=False)
    bunga = bpy.context.view_layer.objects.active

    object3D.translate_object(bunga, 27, 29, 33)
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
    object3D.translate_object(meja, 275, 230, 12)
    
    #duplikat meja duduk
    bpy.ops.object.join()
    bpy.ops.object.duplicate(linked=False)
    meja = bpy.context.view_layer.objects.active

    object3D.translate_object(meja, 360, 230, 12)
    
    # end meja duduk
    
    
    #jalan dan bunderan
    jalan1 = Square("jalan.001", 103, 600, 1, location=(120, -80, 0))
    jalan2 = Square("jalan.002", 500, 103, 1, location=(-70, 300, 0))
    bunderan1 = Cylinder("bunderan.001", 80, 1, num_segments=64, location=(86, 175.5, 0))
    bunderan2 = Cylinder("bunderan.002", 35, 10, num_segments=64, location=(86, 175.5, 0))
    
    #bpy.ops.curve.tree_add(do_update=True, chooseSet='0', bevel=True, prune=False, showLeaves=True, useArm=False, seed=0, handleType='0', levels=2, length=(0.8, 0.6, 0.5, 0.1), lengthV=(0, 0.1, 0, 0), taperCrown=0.5, branches=(0, 55, 10, 1), curveRes=(8, 5, 3, 1), curve=(0, -15, 0, 0), curveV=(20, 50, 75, 0), curveBack=(0, 0, 0, 0), baseSplits=3, segSplits=(0.1, 0.5, 0.2, 0), splitByLen=True, rMode='rotate', splitAngle=(18, 18, 22, 0), splitAngleV=(5, 5, 5, 0), scale=60, scaleV=2, attractUp=(3.5, -1.89984, 0, 0), attractOut=(0, 0.8, 0, 0), shape='6', shapeS='10', customShape=(1, 1, 0.1, 0.5), branchDist=1.5, nrings=0, baseSize=0.3, baseSize_s=0.16, splitHeight=0.2, splitBias=0.55, ratio=0.015, minRadius=0.0015, closeTip=False, rootFlare=1, autoTaper=True, taper=(1, 1, 1, 1), radiusTweak=(1, 1, 1, 1), ratioPower=1.2, downAngle=(0, 26.21, 52.56, 30), downAngleV=(0, 10, 10, 10), useOldDownAngle=True, useParentAngle=True, rotate=(99.5, 137.5, 137.5, 137.5), rotateV=(15, 0, 0, 0), scale0=1, scaleV0=0.1, pruneWidth=0.34, pruneBase=0.12, pruneWidthPeak=0.5, prunePowerHigh=0.5, prunePowerLow=0.001, pruneRatio=0.75, leaves=150, leafDownAngle=30, leafDownAngleV=-10, leafRotate=137.5, leafRotateV=15, leafScale=3, leafScaleX=0.2, leafScaleT=0.1, leafScaleV=0.15, leafShape='hex', bend=0, leafangle=-12, horzLeaves=True, leafDist='6', bevelRes=1, resU=4, armAnim=False, previewArm=False, leafAnim=False, frameRate=1, loopFrames=0, wind=1, gust=1, gustF=0.075, af1=1, af2=1, af3=4, makeMesh=False, armLevels=2, boneStep=(1, 1, 1, 1))
    


    
if __name__ == "__main__":
    main()
    
    
    
