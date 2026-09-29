
bl_info = {
    "name": "A Structured Add-on",
    "author": "Diego Moreno",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "description": "Add-on consisting of multiple files",
    "category": "Learning",
}

from . import img_loader
from . import preferences
from . import operators
from . import panel
from . import _refresh_ # to make sure that the changes to our add-on .py files are always applied. Normally for develop purposes.
_refresh_.reload_modules()

def register():
    img_loader.register_icons()
    preferences.register_classes()
    panel.register_classes()
    operators.register_classes()

def unregister():
    img_loader.unregister_icons()
    panel.unregister_classes()
    preferences.unregister_classes()
    operators.unregister_classes()