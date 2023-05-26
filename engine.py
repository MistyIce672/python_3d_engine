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
        self.scale = 100
        self.rotation_speed = 0
        self.build_speed = 5
        self.rotation = {"x":0,"y":0,"z":0}
        self.scaling = {"x":0,"y":0,"z":0}
        self.offset= {"x":0,"y":0,"z":0}
        self.visible = True

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

    def build_wireframe(self,verts,network):
        obj = []
        for link in network:
            start,finish = link
            obj.append((verts[start],verts[finish]))
        
        return(obj)
    
    def draw_wireframe(self,window,draw,color=None):
        if self.visible == True:
            vertices = self.vertices
            if self.rotation["x"] != 0:
                vertices = self.rotate_y(vertices,self.rotation["x"])
            if self.rotation["y"] != 0:
                vertices = self.rotate_x(vertices,self.rotation["y"])
            if self.rotation["z"] != 0:
                vertices = self.rotate_z(vertices,self.rotation["z"])
            
            if self.offset != {"x":0,"y":0,"z":0}:
                vertices = self.displace(vertices,self.offset)

            obj = self.build_wireframe(vertices,self.links)
            for vertex in obj:
                start,finish = vertex
                sx,sy,sz = start
                fx,fy,fz = finish
                scale = self.scale
                z_shift = (scale/2)
                fx = 400-(fx*scale)
                fy= 300-(fy*scale)
                sx = 400-(sx*scale)
                sy= 300-(sy*scale)
                sx = sx + (sz*z_shift)
                sy = sy - (sz*z_shift)
                fx = fx + (fz*z_shift)
                fy = fy - (fz*z_shift)
                if color == None:
                    color = self.line_color
                pygame.draw.line(window, color, (sx, sy), (fx, fy))
                line_coordinates = [(sx, sy), (fx, fy)]
                draw.line(line_coordinates, color, width=1)
            

def next_frame(current_frame,window,image):
    image.save(f"output\\{current_frame}.png") 
    window.fill(bg_color)
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    return(draw,image)


cube = object()
cube.load_wireframe("cube.obj")




frame = 0
end = 30
while frame < end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        cube.draw_wireframe(window,draw)
        cube.offset["y"] += .1
        pygame.display.update()
        draw,image = next_frame(frame,window,image)
        frame += 1
        dt = clock.tick(5)



