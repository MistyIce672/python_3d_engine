# 3d render engine python

A simple script that can load anime and display obj files to make you look like a hacker 


## Installation

Install my-project with npm

```bash
  pip install -r requirements.txt
```
    
## Usage



```python
    #define new empty object
    obj = object()

    #default attributes 
    bg_color = (0,0,0) #black
    line_color = (255,255,255) #white
    scale = 100
    FPS = 30
    rotation_speed = 0
    build_speed = 5


    #set background color 
    cube.bg_color = (10,10,10)

    #set line color
    cube.line_color = (	31, 81, 255)

    #set scale
    cube.scale = 100

    #set rotation speeds
    cube.rotation_speed = 5

    #set build speed
    cube.build_speed = 5

    #loading wireframe with build animation 
    cube.load_wireframe("text.obj")#file name to be loaded 
    cube.build("y")


    #load obj from will will load object as faces 
    cube.load_obj_from_file("text.obj")
    #run will render loaded faces
    cube.run()

    #load wireframe will load the file as a wireframe
    cube.load_wireframe("text.obj")
    #run wireframe will display loaded wireframe while rotating it 
    cube.run_wireframe()
```