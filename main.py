import pygame
import math
import numpy as np

x = "left right"
pygame.init()

class object():
    def __init__(self) -> None:
        self.vertices = None
        self.links = None
        self.bg_color = (0,0,0)
        self.line_color = (255,255,255)
        self.window = pygame.display.set_mode((800, 600))
        self.scale = 100
        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.rotation_speed = 0
        self.build_speed = 5
    
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
    
    def rotate_x(self,verts,a):
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
    
    def draw_faces(self,obj,color):
        count = 0
        for face in obj:
            count += 1
            new_face = []
            for vertex in face:
                sx,sy,sz = vertex
                scale = self.scale
                z_shift = (scale/2)
                sx = 400-(sx*scale)
                sy= 300-(sy*scale)
                sx = sx + (sz*z_shift)
                sy = sy - (sz*z_shift)
                new_face.append((sx,sy))

            depth = (255/len(obj))*count
            print(count)
            color = (depth,depth,depth)
            pygame.draw.polygon(self.window, color,tuple(new_face) )
         
    def draw_wireframe(self,object,color=None):
        for vertex in object:
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
            pygame.draw.line(self.window, color, (sx, sy), (fx, fy)) 
            
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
                
    def sort(self,items):
        for count in range(0,len(items)):
            for count in range(0,len(items)):
                if count +1 <len(items):
                    total = 0
                    next_total = 0
                    x_offset =0
                    n_x_offset = 0
                    y_offset =0
                    n_y_offset = 0
                    for vert in items[count]:
                        x,y,z = vert
                        total = total + z
                        x_offset = x_offset + x
                        y_offset = y_offset + y
                    for vert in items[count+1]:
                        x,y,z = vert
                        next_total = next_total + z
                        n_x_offset = n_x_offset + x
                        n_y_offset = n_y_offset + y
                    if total/len(items[count]) < next_total/len(items[count+1]):
                        items[count],items[count + 1] = items[count + 1],items[count]
                    elif total/len(items[count]) == next_total/len(items[count+1]):
                        if x_offset/len(items[count]) < n_x_offset/len(items[count+1]):
                            items[count],items[count + 1] = items[count + 1],items[count]
                    elif x_offset/len(items[count]) == x_offset/len(items[count+1]):
                        if y_offset/len(items[count]) > n_y_offset/len(items[count+1]):
                            items[count],items[count + 1] = items[count + 1],items[count]
        return(items)
    
    def crop(self,items,num,axis = "y"):
        for count in range(0,len(items)):
            for count in range(0,len(items)):
                if count +1 <len(items):
                    total = 0
                    next_total = 0
                    x_offset =0
                    n_x_offset = 0
                    y_offset =0
                    n_y_offset = 0
                    for vert in items[count]:
                        x,y,z = vert
                        total = total + z
                        x_offset = x_offset + x
                        y_offset = y_offset + y
                    for vert in items[count+1]:
                        x,y,z = vert
                        next_total = next_total + z
                        n_x_offset = n_x_offset + x
                        n_y_offset = n_y_offset + y
                    if axis == "x":
                        if x_offset/len(items[count]) > n_x_offset/len(items[count+1]):
                            items[count],items[count + 1] = items[count + 1],items[count]
                    if axis == "y":
                        if y_offset/len(items[count]) > n_y_offset/len(items[count+1]):
                            items[count],items[count + 1] = items[count + 1],items[count]
                    if axis == "z":
                        if total/len(items[count]) > next_total/len(items[count+1]):
                            items[count],items[count + 1] = items[count + 1],items[count]
        return(items[0:num])

    def clear(self,color=None):
        if color == None:
            color = self.bg_color
        self.window.fill(color)

    def run(self):
        vertices = self.vertices
        num = 0
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.clear()
                num = num + 1
                vertices = self.rotate_x(vertices,self.rotation_speed)
                faces = self.build_faces(vertices,self.links)
                faces = self.sort(faces)
                self.draw_faces(faces,(0,0,0))
                pygame.display.update()
                dt = clock.tick(5)
    
    def run_wireframe(self):
        vertices = self.vertices
        num = 0
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.clear()
                num = num + 1
                vertices = self.rotate_x(vertices,self.rotation_speed)
                faces = self.build_wireframe(vertices,self.links)
                self.draw_wireframe(faces)
                pygame.display.update()
                dt = clock.tick(5)

    def build(self,axis="y"):
        vertices = self.vertices
        num = 0
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.clear()
                vertices = self.rotate_x(vertices,self.rotation_speed)
                
                lines = self.build_wireframe(vertices,self.links)
                if num < len(lines):
                    num = num + self.build_speed
                lines = self.crop(lines,num,axis)
                self.draw_wireframe(lines)
                pygame.display.set_caption(str(self.clock.get_fps()))
                pygame.display.update()
                dt = self.clock.tick(self.FPS)
    
    def display(self):
        faces = self.build_faces(self.vertices,self.links)
        faces = self.sort(faces)
        self.draw_faces(faces,(0,0,0))
        pygame.display.update()


cube = object()
cube.bg_color = (10,10,10)
cube.line_color = (	31, 81, 255)
cube.scale = 10
cube.rotation_speed = 1
cube.build_speed = 50
cube.load_wireframe("building.obj")
cube.build("y")

#other examples

#load obj from will will load object as faces 
##cube.load_obj_from_file("text.obj")
#run will render loaded faces
##cube.run()

#load wireframe will load the file as a wireframe
##cube.load_wireframe("text.obj")
#run wireframe will display loaded wireframe while rotating it 
##cube.run_wireframe()





