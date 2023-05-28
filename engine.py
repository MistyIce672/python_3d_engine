import pygame
import math
import numpy as np
from PIL import Image, ImageDraw

pygame.init()
FPS = 30
width = 900
height = 600
clock = pygame.time.Clock()
bg_color = (0, 0, 0)  
window = pygame.display.set_mode((width, height))
image = Image.new("RGB", (width, height), bg_color)
draw = ImageDraw.Draw(image)


class object():
    def __init__(self) -> None:
        self.vertices = None
        self.links = None
        self.obj = None
        self.line_color = (255,255,255)
        self.shade = (44, 114, 178)
        self.scale = 100
        self.rotation_speed = 0
        self.build_speed = 5
        self.rotation = {"x":0,"y":0,"z":0}
        self.scaling = {"x":0,"y":0,"z":0}
        self.offset= {"x":0,"y":0,"z":0}
        self.visible = True
        self.type = "faces"

    def load(self,file):
        if self.type == "faces":
            self.load_obj_from_file(file)
        else:
            self.load_wireframe(file)

    def load_wireframe(self,file):
        with open(file,"r")as f:
            lines = f.readlines()

        vertices = []
        for line in lines:
            if line[0:2] == "v ":
                verts = line.split(" ")
                x = verts[-3]
                y = verts[-2]
                z = verts[-1]
                vertices.append((float(x),float(y),float(z)))   
        
        conections = []
        for line in lines:
            if line[0:2] == "f ":
                points = line.split(" ")
                points.pop(0)
                items = []
                for item in points:
                    val = item.split("/")
                    val = val[0]
                    if val != "\n":
                        items.append(int(val))
                for count in range(0,len(items)):
                    conections.append((items[count]-1,items[count-1]-1))
        self.vertices = vertices
        self.links = conections
        return(vertices,conections)
    
    def load_obj_from_file(self,file):
        with open(file,"r")as f:
            lines = f.readlines()
        vertices = []
        for line in lines:
            if line[0:2] == "v ":
                verts = line.split(" ")
                x = verts[-3]
                y = verts[-2]
                z = verts[-1]
                vertices.append((float(x),float(y),float(z)))   
        conections = []
        for line in lines:
            if line[0:2] == "f ":
                points = line.split(" ")
                points.pop(0)
                items = []
                for item in points:
                    val = item.split("/")
                    val = val[0]
                    if val != "\n":
                        items.append(int(val))
                links = []
                for count in range(0,len(items)):
                    links.append(items[count]-1)
                conections.append(tuple(links))
        self.vertices = vertices
        self.links = conections
        return(vertices,conections)
    
    def rotate_y(self,verts,a):
        new_verts = []
        for vert in verts:
            x,y,z = vert
            vertex = np.array([x,y,z])
            angle_degrees = a
            angle_radians = math.radians(angle_degrees)
            rotation_matrix = np.array([[math.cos(angle_radians), 0, math.sin(angle_radians)],
                                        [0, 1, 0],
                                        [-math.sin(angle_radians), 0, math.cos(angle_radians)]])
            rotated_vertex = np.dot(rotation_matrix, vertex)
            x = rotated_vertex[0]
            y = rotated_vertex[1]
            z = rotated_vertex[2]
            vert = (x,y,z)
            new_verts.append(vert)
        return(new_verts)
    
    def rotate_x(self,verts,a):
        new_verts = []
        for vert in verts:
            x,y,z = vert
            vertex = np.array([x,y,z])
            angle_degrees = a
            angle_radians = math.radians(angle_degrees)
            rotation_matrix = np.array([[1,0,0],
                                        [0, math.cos(angle_radians), -math.sin(angle_radians)],
                                        [0,  math.sin(angle_radians), math.cos(angle_radians)]])
            rotated_vertex = np.dot(rotation_matrix, vertex)
            x = rotated_vertex[0]
            y = rotated_vertex[1]
            z = rotated_vertex[2]
            vert = (x,y,z)
            new_verts.append(vert)
        return(new_verts)
    
    def rotate_z(self,verts,a):
        new_verts = []
        for vert in verts:
            x,y,z = vert
            vertex = np.array([x,y,z])
            angle_degrees = a
            angle_radians = math.radians(angle_degrees)
            rotation_matrix = np.array([[math.cos(angle_radians), -math.sin(angle_radians), 0],
                                        [math.sin(angle_radians), math.cos(angle_radians), 0],
                                        [0, 0, 1]])
            rotated_vertex = np.dot(rotation_matrix, vertex)
            x = rotated_vertex[0]
            y = rotated_vertex[1]
            z = rotated_vertex[2]
            vert = (x,y,z)
            new_verts.append(vert)
        return(new_verts)
    
    def displace(self,vertices,offset):
        new_verts = []
        for vert in vertices:
            x,y,z = vert
            x = x+offset["x"]
            y = y+offset["y"]
            z = z+offset["z"]
            vert = (x,y,z)
            new_verts.append(vert)
        return(new_verts)
    
    def quik_sort(self,items):
        items.sort(key=lambda f: (-sum(v[2] for v in f) / len(f), sum(v[1] for v in f) / len(f)))
        return(items)

    def sort(self, items):
        n = len(items)
        for i in range(n):
            for j in range(n - i - 1):
                total = sum(vert[2] for vert in items[j])
                next_total = sum(vert[2] for vert in items[j + 1])

                if total / len(items[j]) < next_total / len(items[j + 1]):
                    items[j], items[j + 1] = items[j + 1], items[j]
                elif total / len(items[j]) == next_total / len(items[j + 1]):
                    x_offset = sum(vert[0] for vert in items[j])
                    n_x_offset = sum(vert[0] for vert in items[j + 1])

                    if x_offset / len(items[j]) < n_x_offset / len(items[j + 1]):
                        items[j], items[j + 1] = items[j + 1], items[j]
                    elif x_offset / len(items[j]) == n_x_offset / len(items[j + 1]):
                        y_offset = sum(vert[1] for vert in items[j])
                        n_y_offset = sum(vert[1] for vert in items[j + 1])

                        if y_offset / len(items[j]) > n_y_offset / len(items[j + 1]):
                            items[j], items[j + 1] = items[j + 1], items[j]
        return items

    def build_wireframe(self,verts,network):
        obj = []
        for link in network:
            start,finish = link
            obj.append((verts[start],verts[finish]))
        
        return(obj)
    
    def build_faces(self,verts,network):
        obj = []
        for link in network:
            face = []
            for item in link:
                face.append(verts[item])
            obj.append((face))
        return(obj)
    
    def draw(self,window,draw):
        if self.type == "faces":
            self.draw_faces(window,draw)
        else:
            self.draw_wireframe(window,draw)
    
    def draw_wireframe(self,window,draw):
        if self.visible == True:
            vertices = self.vertices

            if self.rotation["x"] != 0:
                vertices = self.rotate_y(vertices,self.rotation["x"])
            if self.rotation["y"] != 0:
                vertices = self.rotate_x(vertices,self.rotation["y"])
            if self.rotation["z"] != 0:
                vertices = self.rotate_z(vertices,self.rotation["z"])

            center = [sum(coord) / len(vertices) for coord in zip(*vertices)]
            scaled_vectors = []
            cx,cy,cz = center
            scalar = self.scale
            scale = scalar
            for vector in vertices:
                x,y,z = vector
                dx = cx-x
                x = x-(dx*scalar)
                dy = cy-y
                y = y-(dy*scalar)
                scaled_vectors.append((x,y,z))
            vertices = scaled_vectors


            
            if self.offset != {"x":0,"y":0,"z":0}:
                vertices = self.displace(vertices,self.offset)

            obj = self.build_wireframe(vertices,self.links)

            for vertex in obj:
                start,finish = vertex
                sx,sy,sz = start
                fx,fy,fz = finish
                z_shift = (self.scale/2)
                scale = 1
                
                fx = (width/2)-(fx*scale)
                fy= (height/2)-(fy*scale)
                sx = (width/2)-(sx*scale)
                sy= (height/2)-(sy*scale)
                sx = sx + (sz*z_shift)
                sy = sy - (sz*z_shift)
                fx = fx + (fz*z_shift)
                fy = fy - (fz*z_shift)
                color = self.line_color
                pygame.draw.line(window, color, (sx, sy), (fx, fy))
                line_coordinates = [(sx, sy), (fx, fy)]
                draw.line(line_coordinates, color, width=1)
    
    def draw_faces(self,window,draw):
        if self.visible == True:
            print("drawing")
            vertices = self.vertices

            if self.rotation["x"] != 0:
                vertices = self.rotate_y(vertices,self.rotation["x"])
            if self.rotation["y"] != 0:
                vertices = self.rotate_x(vertices,self.rotation["y"])
            if self.rotation["z"] != 0:
                vertices = self.rotate_z(vertices,self.rotation["z"])

            center = [sum(coord) / len(vertices) for coord in zip(*vertices)]
            scaled_vectors = []
            cx,cy,cz = center
            scalar = self.scale
            scale = scalar
            for vector in vertices:
                x,y,z = vector
                dx = cx-x
                x = x-(dx*scalar)
                dy = cy-y
                y = y-(dy*scalar)
                scaled_vectors.append((x,y,z))
            vertices = scaled_vectors


            
            if self.offset != {"x":0,"y":0,"z":0}:
                vertices = self.displace(vertices,self.offset)
            obj = self.build_faces(vertices,self.links)
            obj = self.quik_sort(obj)
            count = 0
            for face in obj:
                count += 1
                new_face = []
                bigz = face[0][2]
                smallz = face[0][2]
                bigy = face[0][0]
                smally = face[0][0]
                for vertex in face:
                    sx,sy,sz = vertex
                    if sz > bigz:
                        bigz = sz
                    if sz < smallz:
                        smallz = sz
                    if sy > bigy:
                        bigy = sx
                    if sy < smally:
                        smally = sx
                    z_shift = (self.scale/2)
                    scale = 1
                    sx = 400-(sx*scale)
                    sy= 300-(sy*scale)
                    sx = sx + (sz*z_shift)
                    sy = sy - (sz*z_shift)
                    new_face.append((sx,sy))
                if (bigy-smally) != 0:
                    color = self.line_color
                else:
                    color = self.shade
                pygame.draw.polygon(window, color,tuple(new_face) )
                polygon_color = color  # RGB color tuple for red
                draw.polygon(new_face, fill=polygon_color)
            
def next_frame(current_frame,window,image):
    image.save(f"output\\{current_frame}.png") 
    window.fill(bg_color)
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    return(draw,image)

items = []

one = object()
one.load("novacain\\one.obj")

more = object()
more.load("novacain\\more.obj")


shot = object()
shot.load("novacain\\shot.obj")

cuz = object()
cuz.load("novacain\\cuz.obj")

feel = object()
feel.load("novacain\\i feel.obj")

like = object()
like.load("novacain\\like.obj")

your = object()
your.load("novacain\\your.obj")

upto = object()
upto.load("novacain\\up to.obj")

something = object()
something.load("novacain\\something.obj")

fuck = object()
fuck.load("novacain\\fuck.obj")

that = object()
that.load("novacain\\that.obj")

scan = object()
scan.load("novacain\\scan.obj")

bullet = object()
bullet.type = "wireframe"
bullet.load("novacain\\bullet.obj")



bullet.line_color=(241, 191, 79)

heart = object()
heart.type = "wireframe"
heart.load("novacain\\heart.obj")

left = object()
left.type = "wireframe"
left.load("novacain\\left.obj")

right = object()
right.type = "wireframe"
right.load("novacain\\right.obj")

heart.line_color = (255, 25, 21)
left.line_color = (255, 25, 21)
right.line_color = (255, 25, 21)

items.append(one)
items.append(more)
items.append(shot)
items.append(cuz)
items.append(feel)
items.append(like)
items.append(your)
items.append(upto)
items.append(something)
items.append(fuck)
items.append(that)
items.append(scan)
items.append(bullet)
items.append(heart)
items.append(left)
items.append(right)


current = 0
end = 350
keyframes = {}
for item in range(current,end+1):
    keyframes[item] = []

template = {"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":True}

keyframes[0].append({"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":False})
keyframes[0].append({"item":more,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":False})
keyframes[0].append({"item":shot,"location":{"x":600,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":False})
keyframes[0].append({"item":cuz,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":False})
keyframes[0].append({"item":feel,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":like,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":your,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":upto,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":something,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":fuck,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":that,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":scan,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":bullet,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":heart,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":left,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[0].append({"item":right,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})

keyframes[19].append({"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":True})
keyframes[26].append({"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":True})

keyframes[45].append({"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":True})
keyframes[45].append({"item":more,"location":{"x":-600,"y":30,"z":0},"rotation":{"x":180,"y":0,"z":0},"scale":120,"visibility":True})

keyframes[56].append({"item":one,"location":{"x":600,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":False})
keyframes[56].append({"item":more,"location":{"x":0,"y":30,"z":0},"rotation":{"x":180,"y":0,"z":0},"scale":120,"visibility":True})

keyframes[64].append({"item":shot,"location":{"x":600,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":False})
keyframes[64].append({"item":more,"location":{"x":0,"y":30,"z":0},"rotation":{"x":180,"y":0,"z":0},"scale":120,"visibility":True})

keyframes[70].append({"item":more,"location":{"x":0,"y":30,"z":0},"rotation":{"x":180,"y":120,"z":0},"scale":120,"visibility":False})
keyframes[70].append({"item":shot,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":300,"z":0},"scale":120,"visibility":True})
keyframes[70].append({"item":bullet,"location":{"x":-600,"y":-100,"z":0},"rotation":{"x":180,"y":300,"z":0},"scale":60,"visibility":True})

keyframes[76].append({"item":shot,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})
keyframes[76].append({"item":bullet,"location":{"x":0,"y":-100,"z":0},"rotation":{"x":180,"y":300,"z":0},"scale":60,"visibility":True})

keyframes[80].append({"item":bullet,"location":{"x":600,"y":-100,"z":0},"rotation":{"x":180,"y":300,"z":0},"scale":60,"visibility":True})

keyframes[100].append({"item":shot,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":False})
keyframes[100].append({"item":cuz,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})

keyframes[104].append({"item":cuz,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})

keyframes[144].append({"item":cuz,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[144].append({"item":feel,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})

keyframes[148].append({"item":feel,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})

keyframes[158].append({"item":feel,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[158].append({"item":like,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})

keyframes[162].append({"item":like,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})

keyframes[166].append({"item":like,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[166].append({"item":your,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})

keyframes[170].append({"item":your,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})

keyframes[174].append({"item":your,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[174].append({"item":upto,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})

keyframes[178].append({"item":upto,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})

keyframes[184].append({"item":upto,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[184].append({"item":something,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})

keyframes[188].append({"item":something,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})

keyframes[208].append({"item":something,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[208].append({"item":fuck,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})

keyframes[212].append({"item":fuck,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})
keyframes[214].append({"item":fuck,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[214].append({"item":that,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})
keyframes[218].append({"item":that,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})
keyframes[220].append({"item":that,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})

keyframes[220].append({"item":your,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})
#
keyframes[224].append({"item":your,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})
keyframes[244].append({"item":your,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
#
keyframes[244].append({"item":upto,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})
#
keyframes[248].append({"item":upto,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})
keyframes[254].append({"item":upto,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})

keyframes[254].append({"item":something,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})

keyframes[258].append({"item":something,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})
keyframes[300].append({"item":something,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[300].append({"item":scan,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":120,"visibility":True})
keyframes[300].append({"item":heart,"location":{"x":20,"y":-100,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":140,"visibility":True})

keyframes[304].append({"item":heart,"location":{"x":20,"y":-100,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":140,"visibility":False})
keyframes[304].append({"item":left,"location":{"x":-15,"y":-105,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":140,"visibility":True})
keyframes[304].append({"item":right,"location":{"x":55,"y":-105,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":140,"visibility":True})
keyframes[304].append({"item":scan,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":True})

keyframes[315].append({"item":left,"location":{"x":-50,"y":-125,"z":0},"rotation":{"x":180,"y":360,"z":30},"scale":140,"visibility":True})
keyframes[315].append({"item":right,"location":{"x":90,"y":-125,"z":0},"rotation":{"x":180,"y":360,"z":-30},"scale":140,"visibility":True})

keyframes[340].append({"item":scan,"location":{"x":0,"y":60,"z":0},"rotation":{"x":180,"y":360,"z":0},"scale":130,"visibility":False})
keyframes[340].append({"item":left,"location":{"x":-50,"y":-125,"z":0},"rotation":{"x":180,"y":360,"z":30},"scale":140,"visibility":False})
keyframes[340].append({"item":right,"location":{"x":90,"y":-125,"z":0},"rotation":{"x":180,"y":360,"z":-30},"scale":140,"visibility":False})



current = 0


while current < 350:
    #for event in pygame.event.get():
    if current < end:

        for item in items:
            now = None
            start = None
            finish = None
            sf = None
            ff = None
            br = False
            for frame in keyframes:

                if br == True:
                    break
                for obj in keyframes[frame]:
                    if obj['item'] == item  and frame == current:
                        now = obj
                    if obj['item'] == item  and frame < current:
                        start = obj
                        sf = frame
                    if obj['item'] == item  and frame > current:
                        finish = obj
                        ff = frame
                        br = True
                        break
            if ff == None:
                ff = sf
                finish = start
            if now != None:
                item.visible = now['visibility']
                item.offset = now['location']
                item.rotation = now['rotation']
                item.scale = now['scale']
            else:
                item.visible = start['visibility']

                differnce = ff - sf
                multiplier = current-sf

                #scale
                if finish['scale'] - start['scale'] != 0:
                    scale = finish['scale'] - start['scale']
                    scale = start['scale']+((scale/differnce)*multiplier)
                else:
                    scale = start['scale']
                item.scale = scale

                #offset
                finishx,finishy,finishz = finish['location']['x'],finish['location']['y'],finish['location']['z']
                startx,starty,startz = start['location']['x'],start['location']['y'],start['location']['z']
                x = finishx-startx
                y = finishy-starty
                z = finishz-startz
                if x == 0:
                    x = startx
                else:
                    x = startx+((x/differnce)*multiplier)
                if y == 0:
                    y = starty
                else:
                    y = starty+((y/differnce)*multiplier)
                if z == 0:
                    z = startz
                else:
                    z = startz+((z/differnce)*multiplier)
                offset = {"x":x,"y":y,"z":z}
                item.offset = offset

                #rotation
                finishx,finishy,finishz = finish['rotation']['x'],finish['rotation']['y'],finish['rotation']['z']
                startx,starty,startz = start['rotation']['x'],start['rotation']['y'],start['rotation']['z']
                x = finishx-startx
                y = finishy-starty
                z = finishz-startz
                
                if x == 0:
                    x = startx
                else:
                    x = startx+((x/differnce)*multiplier)
                if y == 0:
                    y = starty
                else:
                    y = starty+((y/differnce)*multiplier)
                if z == 0:
                    z = startz
                else:
                    z = startz+((z/differnce)*multiplier)
                roation = {"x":x,"y":y,"z":z}
                item.rotation = roation
                    
            item.draw(window,draw)
        print("next")
        pygame.display.update()
        draw,image = next_frame(current,window,image)
        current += 1
        dt = clock.tick(5)



