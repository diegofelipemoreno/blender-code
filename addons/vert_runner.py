
bl_info = {
    "name": "Vert Runner",
    "author": "John Packt",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Object > Animation > Vert Runner",
    "description": "Run over vertices of the active object",
    "category": "Learning",
}


import bpy
from math import asin, pi


class VertRunner(bpy.types.Operator):
    """Run over the vertices of the active object"""
    bl_idname = "object.vert_runner"
    bl_label = "Vertex Runner"
    bl_description = "Animate along vertices of active object"
    bl_options = {'REGISTER', 'UNDO'}

    step: bpy.props.IntProperty(default=12)
    loop: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        obj = context.object

        if not obj:
            return False

        if not obj.type == 'MESH':
            return False
        
        if not len(context.selected_objects) > 1:
            return False

        return True

    def aim_to_point(self, ob, target_co):
        direction = target_co - ob.location
        direction.normalize()

        arc = asin(direction.y)
        if direction.x < 0:
            arc = pi - arc
        
        arc += pi / 2
        arcs = (arc, arc + 2*pi, arc - 2*pi)

        diffs = [abs(ob.rotation_euler.z - a) for a in arcs]
        shortest = min(diffs)

        res = next(a for i, a in enumerate(arcs) if diffs[i] == shortest)
        ob.rotation_euler.z = res

    def execute(self, context):
        verts = list(context.object.data.vertices)
        
        if self.loop:
            verts.append(verts[0])

        for ob in context.selected_objects:
            if ob == context.active_object:
                continue      

            # move to last position to orient towards first vertex
            ob.location = context.object.data.vertices[-1].co

            frame = context.scene.frame_current
            for vert in verts:                
                # orient towards destination before moving the object
                self.aim_to_point(ob, vert.co)
                ob.keyframe_insert('rotation_euler', frame=frame, index=2)

                ob.location = vert.co
                ob.keyframe_insert('location', frame=frame)

                frame += self.step
 
        return {'FINISHED'}


def anim_menu_func(self, context):
    self.layout.separator()
    self.layout.operator(VertRunner.bl_idname,
                         text=VertRunner.bl_label)

def register():
    bpy.utils.register_class(VertRunner)
    bpy.types.VIEW3D_MT_object_animation.append(anim_menu_func)  #TODO: header button

def unregister():
    bpy.types.VIEW3D_MT_object_animation.remove(anim_menu_func)
    bpy.utils.unregister_class(VertRunner)

"""
    def aim_to_point(self, ob, point_co):
       Orienta el objeto para que apunte hacia las coordenadas 'point_co'
        
        # 1. DIRECCIÓN: Obtiene el vector desde el objeto hacia el punto de destino
        direction = point_co - ob.location

        # 2. NORMALIZACIÓN: Reduce la longitud del vector a 1 manteniendo su dirección.
        # Esto evita diferencias de escala y estandariza los cálculos trigonométricos.
       Sin normalize(), el obj se movería un 41% más rápido al ir en diagonal.Al aplicar .normalize() al vector diagonal $(1, 1)$, este se transforma en aprox. $(0.707, 0.707)$, cuya longitud vuelve a ser exactamente $1$, manteniendo la velocidad uniforme en cualquier dirección.
       
        direction.normalize()

        # 3. ÁNGULO BASE: Arcoseno de 'y' para obtener el ángulo de inclinación según la altura[cite: 1].
        # (asin solo calcula valores para el lado derecho del círculo, donde X >= 0)[cite: 1].
        arc = asin(direction.y)

        # 4. CORRECCIÓN DE LADO (Eje X): Si el punto está a la izquierda (X < 0),
        # reflejamos el ángulo restándolo de pi (180°) para mantener la misma altura Y[cite: 1].
        if direction.x < 0:
            arc = pi - arc  #[cite: 1]
        
        # 5. ALINEACIÓN CON BLENDER: En Blender los objetos miran por defecto hacia -Y[cite: 1].
        # Sumamos pi/2 (+90°) para compensar el frente por defecto del objeto[cite: 1].
        arc += pi / 2  #[cite: 1]

        # 6. OPCIONES DE GIRO: Generamos 3 ángulos equivalentes (misma dirección final)[cite: 1]:
        # - Ángulo directo
        # - Ángulo dando una vuelta en sentido horario (+360° / +2*pi)
        # - Ángulo dando una vuelta en sentido antihorario (-360° / -2*pi)
        arcs = (arc, arc + 2*pi, arc - 2*pi)  #[cite: 1]

        # 7. CÁLCULO DE DISTANCIA: Mide cuánta rotación real requiere cada una de las 3 opciones
        # comparándola con la rotación actual del objeto en el eje Z[cite: 1].
        diffs = [abs(ob.rotation_euler.z - a) for a in arcs]  #[cite: 1]

        # 8. CAMINO MÁS CORTO: Encuentra la menor diferencia de ángulo necesaria[cite: 1].
        shortest = min(diffs)  #[cite: 1]

        # 9. SELECCIÓN: Busca cuál de los 3 ángulos de 'arcs' produjo esa distancia mínima[cite: 1].
        res = next(a for i, a in enumerate(arcs) if diffs[i] == shortest)  #[cite: 1]

        # 10. APLICACIÓN: Asigna el ángulo más corto al eje Z del objeto para evitar giros de 360°[cite: 1].
        ob.rotation_euler.z = res  #[cite: 1]
"""