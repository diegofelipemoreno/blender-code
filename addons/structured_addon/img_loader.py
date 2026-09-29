from bpy.utils import previews
import os

_CUSTOM_ICONS = None

def register_icons():
    """Load icon from the add-on folder"""
    global _CUSTOM_ICONS

    if _CUSTOM_ICONS:  # avoid loading icons twice
        return

    img_extensions = ('.png', '.jpg')
    collection = previews.new()
    module_path = os.path.dirname(__file__)
    picture_path = os.path.join(module_path, 'pictures')
 
    for img_file in os.listdir(picture_path):
        img_name, ext = os.path.splitext(img_file)
        if ext.lower() not in img_extensions:
            # skip non image files
            continue
        
        disk_path = os.path.join(picture_path, img_file)
        collection.load(img_name, disk_path, 'IMAGE')
        _CUSTOM_ICONS = collection

def unregister_icons():
    """Clear Icons loaded from file"""
    global _CUSTOM_ICONS

    if _CUSTOM_ICONS:
        previews.remove(_CUSTOM_ICONS)
        _CUSTOM_ICONS = None

def get_icons_collection():
    """Get icons loaded from folder"""
    register_icons()  # load icons from disk
    assert _CUSTOM_ICONS  # if None something is wrong
    return _CUSTOM_ICONS