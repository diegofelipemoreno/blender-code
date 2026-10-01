
bl_info = {
    "name": "Action to Range",
    "author": "Diego Moreno",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Timeline > View > Action to Scene Range",
    "description": " Action Duration to Scene Range",
    "category": "Learning",
}

import bpy

class ActionToSceneRange(bpy.types.Operator):
    """Set Playback range to current action Start/End"""
    bl_idname = "anim.action_to_range"
    bl_label = "Action Range to Scene"
    bl_description = "Transfer action range to scene range"
    bl_options = {'REGISTER', 'UNDO'}

    use_preview: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        obj = context.object
        if not obj:
            return False
        if not obj.animation_data:
            return False
        if not obj.animation_data.action:
            return False
        return True

    def execute(self, context):
        anim_data = context.object.animation_data
        first, last = anim_data.action.frame_range

        scn = context.scene
        if self.use_preview:
            scn.frame_preview_start = int(first)
            scn.frame_preview_end = int(last)
        else:
            scn.frame_start = int(first)
            scn.frame_end = int(last)

        try:
            # Para que pueda ser llamada de otro lado de la UI desde el menu por ejemplo edit > adjust last operation
            bpy.ops.action.view_all()
        except RuntimeError:
            # we are not in the timeline context
            for window in context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type != 'DOPESHEET_EDITOR':
                        continue
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            with context.temp_override(window=window,
                                                        area=area,
                                                        region=region):
                                bpy.ops.action.view_all()
                            break
                    break
        return {'FINISHED'}

def view_menu_items(self, context):
    props = self.layout.operator(
                        ActionToSceneRange.bl_idname,
                        text=ActionToSceneRange.bl_label +
                            " (preview)")
    props.use_preview = True

    props = self.layout.operator(ActionToSceneRange.bl_idname,
                                text=ActionToSceneRange.bl_label)
    props.use_preview = False

def register():
    bpy.utils.register_class(ActionToSceneRange)
    #Para cargarlo en el menu del timeline donde lo necesitamos
    bpy.types.TIME_MT_view.append(view_menu_items)

def unregister():
    bpy.utils.unregister_class(ActionToSceneRange)
    bpy.types.TIME_MT_view.remove(view_menu_items)

if __name__ == "__main__":
    register()