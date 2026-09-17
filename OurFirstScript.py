import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

bpy.ops.mesh.primitive_uv_sphere_add(radius=1,
enter_editmode=False, align='WORLD', location=(0, 0, 2), scale=
(1, 1, 1))
#~ {'FINISHED'}
#~ 