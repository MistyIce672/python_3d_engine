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
    
    def draw_wireframe(self,window,draw,color=None):
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
                if color == None:
                    color = self.line_color
                pygame.draw.line(window, color, (sx, sy), (fx, fy))
                line_coordinates = [(sx, sy), (fx, fy)]
                draw.line(line_coordinates, color, width=1)
    
    def draw_faces(self,window,draw):
        obj = self.build_faces(self.vertices,self.links)
        obj = self.sort(obj)
        color = self.line_color
        count = 0
        for face in obj:
            count += 1
            new_face = []
            x
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
            color = (depth,depth,depth)
            pygame.draw.polygon(window, color,tuple(new_face) )
            polygon_color = (255, 0, 0)  # RGB color tuple for red
            draw.polygon(new_face, fill=polygon_color)
            

def next_frame(current_frame,window,image):
    image.save(f"output\\{current_frame}.png") 
    window.fill(bg_color)
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    return(draw,image)

items = []

one = object()
one.load_wireframe("novacain\\one.obj")


more = object()
more.load_wireframe("novacain\\more.obj")


shot = object()
shot.load_wireframe("novacain\\shot.obj")



items.append(one)
items.append(more)
items.append(shot)

current = 0
end = 120
keyframes = {}
for item in range(current,end+1):
    keyframes[item] = []

template = {"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":True}

keyframes[0].append({"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":True})
keyframes[0].append({"item":more,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":False})
keyframes[0].append({"item":shot,"location":{"x":600,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":0,"visibility":False})

keyframes[10].append({"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":True})

keyframes[30].append({"item":one,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":True})
keyframes[30].append({"item":shot,"location":{"x":-600,"y":30,"z":0},"rotation":{"x":180,"y":0,"z":0},"scale":120,"visibility":True})

keyframes[38].append({"item":one,"location":{"x":600,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":True})
keyframes[38].append({"item":shot,"location":{"x":0,"y":30,"z":0},"rotation":{"x":180,"y":0,"z":0},"scale":120,"visibility":True})

keyframes[120].append({"item":shot,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":False})
keyframes[120].append({"item":more,"location":{"x":0,"y":30,"z":0},"rotation":{"x":200,"y":10,"z":5},"scale":120,"visibility":False})


while current < end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

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
                differnce = ff - sf
                multiplier = current-sf

                #scale
                if finish['scale'] - start['scale'] != 0:
                    scale = finish['scale'] - start['scale']
                    scale = (scale/differnce)*multiplier
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


                
            item.draw_wireframe(window,draw)
        pygame.display.update()
        draw,image = next_frame(current,window,image)
        current += 1
        dt = clock.tick(5)



