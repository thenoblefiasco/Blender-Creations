
import bpy
import bmesh
import math

# This script generates 10 different low-poly swords from various historical civilizations.
# It is designed for creating game assets, focusing on clean topology and low vertex count.
#
# How to use:
# 1. Open Blender.
# 2. Go to the "Scripting" workspace.
# 3. Click "Open" and select this file.
# 4. Click the "Run Script" button.

def clear_scene():
    """Clears the scene of all mesh objects to start fresh."""
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def create_sword_component(name, verts, faces, location):
    """Helper function to create a single mesh component for a sword."""
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    obj.location.x = location
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    for v_co in verts:
        bm.verts.new(v_co)
    
    bm.verts.ensure_lookup_table()
    for f_indices in faces:
        bm.faces.new([bm.verts[i] for i in f_indices])
        
    bm.to_mesh(mesh)
    bm.free()
    return obj

def join_and_finalize(objects, name, bevel_width=0.01):
    """Joins components, applies a bevel, and names the final sword object."""
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    
    sword = bpy.context.active_object
    sword.name = name
    
    # Add a simple bevel for sharp edges (great for low-poly style)
    bevel = sword.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = bevel_width
    bevel.segments = 1 # 1 segment creates a nice chamfer
    
    # CORRECTED METHOD for shading in Blender 3.0+
    # This replaces the old use_auto_smooth property.
    # It shades the object smooth, then splits normals based on an angle for sharp edges.
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(45))

    return sword

def create_roman_gladius(location):
    """Short, broad Roman stabbing sword."""
    blade_verts = [
        (0.08, 0, 0), (-0.08, 0, 0), (-0.08, 0.8, 0), (0.08, 0.8, 0),
        (0, 1.0, 0) # Tip
    ]
    blade_faces = [(0, 1, 2, 3), (2, 4, 3)]
    blade = create_sword_component("Blade", blade_verts, blade_faces, location)
    
    guard_verts = [(-0.2, 0, 0.05), (0.2, 0, 0.05), (0.2, 0, -0.05), (-0.2, 0, -0.05)]
    guard_faces = [(0, 1, 2, 3)]
    guard = create_sword_component("Guard", guard_verts, guard_faces, location)
    
    hilt_verts = [(-0.06, -0.05, 0), (0.06, -0.05, 0), (0.06, -0.5, 0), (-0.06, -0.5, 0)]
    hilt_faces = [(0, 1, 2, 3)]
    hilt = create_sword_component("Hilt", hilt_verts, hilt_faces, location)
    
    pommel_verts = [(-0.1, -0.5, 0), (0.1, -0.5, 0), (0, -0.65, 0)]
    pommel_faces = [(0, 1, 2)]
    pommel = create_sword_component("Pommel", pommel_verts, pommel_faces, location)
    
    join_and_finalize([blade, guard, hilt, pommel], "Roman_Gladius")

def create_viking_sword(location):
    """Classic tapering Viking sword."""
    blade_verts = [
        (0.07, 0, 0), (-0.07, 0, 0), (-0.02, 1.2, 0), (0.02, 1.2, 0), # Main blade
        (0, 1.25, 0) # Tip
    ]
    blade_faces = [(0, 1, 2, 3), (2, 4, 3)]
    blade = create_sword_component("Blade", blade_verts, blade_faces, location)
    
    guard_verts = [(-0.25, 0.05, 0), (0.25, 0.05, 0), (0.2, -0.1, 0), (-0.2, -0.1, 0)]
    guard_faces = [(0, 1, 2, 3)]
    guard = create_sword_component("Guard", guard_verts, guard_faces, location)
    
    hilt_verts = [(-0.05, -0.1, 0), (0.05, -0.1, 0), (0.05, -0.6, 0), (-0.05, -0.6, 0)]
    hilt_faces = [(0, 1, 2, 3)]
    hilt = create_sword_component("Hilt", hilt_verts, hilt_faces, location)
    
    pommel_verts = [(-0.15, -0.6, 0), (0.15, -0.6, 0), (0.1, -0.75, 0), (-0.1, -0.75, 0)]
    pommel_faces = [(0, 1, 2, 3)]
    pommel = create_sword_component("Pommel", pommel_verts, pommel_faces, location)
    
    join_and_finalize([blade, guard, hilt, pommel], "Viking_Sword")

def create_katana(location):
    """Curved Japanese Katana."""
    blade_verts = []
    for i in range(11):
        y = i * 0.12
        # Add curve
        x_offset = (1- (abs(i-5)/5.0)**2) * -0.2
        x = 0.05 * (1 - (i/10.0)*0.5) + x_offset # Taper
        blade_verts.append((x, y, 0))
        blade_verts.append((x-0.1, y, 0))
        
    blade_verts.append((-0.2, 1.25, 0)) # Tip
    blade_faces = []
    for i in range(10):
        blade_faces.append((i*2, i*2+1, i*2+3, i*2+2))
    blade_faces.append((20, 21, 22))
    blade = create_sword_component("Blade", blade_verts, blade_faces, location)
    
    guard_verts = [(-0.1, 0, 0.05), (0.1, 0, 0.05), (0.1, 0, -0.05), (-0.1, 0, -0.05)]
    guard_faces = [(0, 1, 2, 3)]
    guard = create_sword_component("Guard", guard_verts, guard_faces, location)
    
    hilt_verts = [(-0.06, -0.05, 0), (0.06, -0.05, 0), (0.06, -0.4, 0), (-0.06, -0.4, 0)]
    hilt_faces = [(0, 1, 2, 3)]
    hilt = create_sword_component("Hilt", hilt_verts, hilt_faces, location)
    
    join_and_finalize([blade, guard, hilt], "Japanese_Katana")

def create_khopesh(location):
    """Sickle-shaped Egyptian Khopesh."""
    blade_verts = []
    for i in range(12):
        angle = (i/11.0) * 2.5 + 0.5
        r = 0.5 + (i/11.0) * 0.3
        x = r * -math.cos(angle)
        y = r * math.sin(angle) + 0.3
        blade_verts.append((x, y, 0.05))
        blade_verts.append((x, y, -0.05))
        
    blade_faces = []
    for i in range(11):
        blade_faces.append((i*2, i*2+1, i*2+3, i*2+2))
    
    blade = create_sword_component("Blade", blade_verts, blade_faces, location)
    
    hilt_verts = [(-0.06, 0.2, 0), (0.06, 0.2, 0), (0.06, -0.3, 0), (-0.06, -0.3, 0)]
    hilt_faces = [(0, 1, 2, 3)]
    hilt = create_sword_component("Hilt", hilt_verts, hilt_faces, location)

    join_and_finalize([blade, hilt], "Egyptian_Khopesh")
    
def create_scimitar(location):
    """Curved Persian Scimitar."""
    blade_verts = []
    for i in range(12):
        angle = (i / 11.0) * 2.0
        x_base = (i / 11.0) * 1.2
        y_base = (x_base**2) * 0.2
        width = 0.08 * (1 - (i / 22.0))
        blade_verts.append((x_base - width, y_base, 0))
        blade_verts.append((x_base + width, y_base, 0))
    blade_verts.append((1.25, (1.2**2) * 0.2 + 0.05, 0)) # Tip
    blade_faces = []
    for i in range(11):
        blade_faces.append((i*2, i*2+1, i*2+3, i*2+2))
    blade_faces.append((22, 23, 24))
    blade = create_sword_component("Blade", blade_verts, blade_faces, location)

    guard_verts = [(-0.15, 0.05, 0.05), (0.15, -0.05, 0.05), (0.15, -0.05, -0.05), (-0.15, 0.05, -0.05)]
    guard_faces = [(0, 1, 2, 3)]
    guard = create_sword_component("Guard", guard_verts, guard_faces, location)

    hilt_verts = [(-0.05, 0, 0), (0.05, 0, 0), (0.0, -0.4, 0)]
    hilt_faces = [(0, 1, 2)]
    hilt = create_sword_component("Hilt", hilt_verts, hilt_faces, location)

    join_and_finalize([blade, guard, hilt], "Persian_Scimitar")
    
def create_claymore(location):
    """Scottish Claymore with distinctive guard."""
    blade = create_sword_component("Blade", [(0.06,0,0),(-0.06,0,0),(-0.04,1.5,0),(0.04,1.5,0)], [(0,1,2,3)], location)
    guard = create_sword_component("Guard", [(-0.4,0.1,0),(0.4,0.1,0),(0.3,-0.1,0),(-0.3,-0.1,0)], [(0,1,2,3)], location)
    hilt = create_sword_component("Hilt", [(-0.05,-0.1,0),(0.05,-0.1,0),(0.05,-0.7,0),(-0.05,-0.7,0)], [(0,1,2,3)], location)
    pommel = create_sword_component("Pommel", [(-0.1,-0.7,0),(0.1,-0.7,0),(0,-0.8,0)], [(0,1,2)], location)
    join_and_finalize([blade, guard, hilt, pommel], "Scottish_Claymore")

def create_longsword(location):
    """European Longsword."""
    blade = create_sword_component("Blade", [(0.07,0,0),(-0.07,0,0),(-0.01,1.3,0),(0.01,1.3,0),(0,1.35,0)], [(0,1,2,3),(2,4,3)], location)
    guard = create_sword_component("Guard", [(-0.3,0.05,0),(0.3,0.05,0),(0.3,-0.05,0),(-0.3,-0.05,0)], [(0,1,2,3)], location)
    hilt = create_sword_component("Hilt", [(-0.05,-0.05,0),(0.05,-0.05,0),(0.05,-0.6,0),(-0.05,-0.6,0)], [(0,1,2,3)], location)
    pommel = create_sword_component("Pommel", [(-0.1,-0.6,0),(0.1,-0.6,0),(0,-0.7,0)], [(0,1,2)], location)
    join_and_finalize([blade, guard, hilt, pommel], "European_Longsword")

def create_dao(location):
    """Chinese Dao."""
    # Similar to scimitar but different curve and hilt
    blade_verts = []
    for i in range(10):
        x = i * 0.12
        y = (x**2) * 0.15
        w = 0.09 * (1-(i/20))
        blade_verts.append((x-w,y,0))
        blade_verts.append((x+w,y,0))
    blade_verts.append((1.2, (1.1**2)*0.15+0.05,0))
    faces = [(i*2,i*2+1,i*2+3,i*2+2) for i in range(9)] + [(18,19,20)]
    blade = create_sword_component("Blade", blade_verts, faces, location)
    guard = create_sword_component("Guard", [(-0.08,-0.02,0.05),(0.08,-0.02,0.05),(0.08,-0.02,-0.05),(-0.08,-0.02,-0.05)], [(0,1,2,3)], location)
    hilt = create_sword_component("Hilt", [(-0.06, -0.02, 0),(0.06, -0.02, 0),(0.04, -0.3, 0),(-0.04, -0.3, 0)], [(0,1,2,3)], location)
    join_and_finalize([blade, guard, hilt], "Chinese_Dao")

def create_khanda(location):
    """Indian Khanda."""
    blade = create_sword_component("Blade", [(0.1,0,0),(-0.1,0,0),(-0.1,1.1,0),(0.1,1.1,0)], [(0,1,2,3)], location)
    guard = create_sword_component("Guard", [(-0.2,0,0), (0.2,0,0), (0.2,-0.1,0),(-0.2,-0.1,0)],[(0,1,2,3)], location)
    hilt = create_sword_component("Hilt", [(-0.06,-0.1,0),(0.06,-0.1,0),(0.06,-0.5,0),(-0.06,-0.5,0)], [(0,1,2,3)], location)
    pommel = create_sword_component("Pommel", [(-0.1,-0.5,0),(0.1,-0.5,0),(0.1,-0.6,0),(-0.1,-0.6,0)], [(0,1,2,3)], location)
    pommel_spike = create_sword_component("Pommel_Spike", [(0.02,-0.6,0),(-0.02,-0.6,0),(0,-0.8,0)], [(0,1,2)], location)
    join_and_finalize([blade, guard, hilt, pommel, pommel_spike], "Indian_Khanda")

def create_zweihander(location):
    """German Zweihander."""
    blade = create_sword_component("Blade", [(0.07,0,0),(-0.07,0,0),(-0.05,1.7,0),(0.05,1.7,0)], [(0,1,2,3)], location)
    parry_hooks = create_sword_component("Parry_Hooks", [(-0.2,0.4,0),(0.2,0.4,0),(0.15,0.3,0),(-0.15,0.3,0)], [(0,1,2,3)], location)
    guard = create_sword_component("Guard", [(-0.4,0.05,0),(0.4,0.05,0),(0.4,-0.05,0),(-0.4,-0.05,0)], [(0,1,2,3)], location)
    hilt = create_sword_component("Hilt", [(-0.05,-0.05,0),(0.05,-0.05,0),(0.05,-0.8,0),(-0.05,-0.8,0)], [(0,1,2,3)], location)
    pommel = create_sword_component("Pommel", [(-0.1,-0.8,0),(0.1,-0.8,0),(0,-0.9,0)], [(0,1,2)], location)
    join_and_finalize([blade, parry_hooks, guard, hilt, pommel], "German_Zweihander")

def main():
    """Main function to create all swords.""""
    clear_scene()
    
    sword_functions = [
        create_roman_gladius,
        create_viking_sword,
        create_katana,
        create_khopesh,
        create_scimitar,
        create_claymore,
        create_longsword,
        create_dao,
        create_khanda,
        create_zweihander
    ]
    
    spacing = 2.0 # Distance between swords
    for i, create_func in enumerate(sword_functions):
        location = i * spacing
        create_func(location)
        
    print(f"Generated {len(sword_functions)} unique low-poly swords.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
