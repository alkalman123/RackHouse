"""Blender (bpy / Cycles) helpers for the photoreal product renders:
scene setup, physically based materials and mesh import."""

import math
import os

import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
HDRI = os.path.join(HERE, "hdri", "studio.exr")
MM = 0.001                    # scene units are metres; geometry is built in mm


def srgb(hexcol):
    h = hexcol.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c) + (1.0,)


def reset(samples=96, size=1400):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _MATS.clear()
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.02
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = 10
    sc.cycles.glossy_bounces = 6
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.blur_glossy = 0.5
    sc.render.film_transparent = True
    sc.render.resolution_x = size
    sc.render.resolution_y = size
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = -1.8
    sc.render.threads_mode = "AUTO"
    world(sc)
    return sc


def world(sc, strength=0.7, rotation=0.0):
    w = bpy.data.worlds.new("world")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(HDRI)
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, rotation)
    nt.links.new(coord.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def area_light(name, loc, target, size, energy, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA")
    d.shape = "DISK"
    d.size = size
    d.energy = energy
    d.color = color
    o = bpy.data.objects.new(name, d)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o


def look_at(obj, target):
    from mathutils import Vector
    d = Vector(target) - Vector(obj.location)
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def camera(target, direction, dist, lens=85):
    d = bpy.data.cameras.new("cam")
    d.lens = lens
    d.sensor_width = 36
    d.clip_start = 0.01
    o = bpy.data.objects.new("cam", d)
    bpy.context.scene.collection.objects.link(o)
    o.location = tuple(np.asarray(target) + np.asarray(direction) * dist)
    look_at(o, target)
    bpy.context.scene.camera = o
    return o


# --------------------------------------------------------------- materials

_MATS = {}


def _new(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    return m, nt, bsdf


def _bump(nt, bsdf, height_socket, strength, distance):
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = strength
    b.inputs["Distance"].default_value = distance
    nt.links.new(height_socket, b.inputs["Height"])
    nt.links.new(b.outputs["Normal"], bsdf.inputs["Normal"])
    return b


def _bevel(nt, bsdf, radius_mm, into=None):
    bv = nt.nodes.new("ShaderNodeBevel")
    bv.samples = 6
    bv.inputs["Radius"].default_value = radius_mm * MM
    nt.links.new(bv.outputs["Normal"], into if into is not None else bsdf.inputs["Normal"])
    return bv


def _noise_rough(nt, bsdf, lo, hi, scale=900.0):
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = scale
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = lo
    mr.inputs["To Max"].default_value = hi
    nt.links.new(n.outputs["Fac"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], bsdf.inputs["Roughness"])


def _uv_wave(nt, axis, period_mm, extra=None):
    """sin(2 pi * uv[axis] / period) from the mm UVs (stored in metres)."""
    uv = nt.nodes.new("ShaderNodeUVMap")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(uv.outputs["UV"], sep.inputs["Vector"])
    src = sep.outputs["X" if axis == 0 else "Y"]
    if extra is not None:
        add = nt.nodes.new("ShaderNodeMath")
        add.operation = "MULTIPLY_ADD"
        add.inputs[1].default_value = extra[1]
        nt.links.new(sep.outputs["Y" if axis == 0 else "X"], add.inputs[0])
        nt.links.new(src, add.inputs[2])
        src = add.outputs[0]
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 2 * math.pi / (period_mm * MM)
    nt.links.new(src, mul.inputs[0])
    sn = nt.nodes.new("ShaderNodeMath")
    sn.operation = "SINE"
    nt.links.new(mul.outputs[0], sn.inputs[0])
    return sn.outputs[0]


def material(key):
    """Materials by key: 'pla-<hex>', 'alu-<hex>', 'steel', 'cable',
    'sling-<hex>', 'thread-<hex>', 'rubber', 'plastic-<hex>', 'wall'."""
    if key in _MATS:
        return _MATS[key]
    kind, _, col = key.partition("-")
    m, nt, b = _new(key)
    if kind == "pla":
        b.inputs["Base Color"].default_value = srgb(col)
        b.inputs["Roughness"].default_value = 0.52
        b.inputs["Specular IOR Level"].default_value = 0.3
        # 0.2 mm layer lines across the print's thickness (use-orientation y)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        mul.inputs[1].default_value = 2 * math.pi / (0.2 * MM)
        nt.links.new(sep.outputs["Y"], mul.inputs[0])
        sn = nt.nodes.new("ShaderNodeMath")
        sn.operation = "SINE"
        nt.links.new(mul.outputs[0], sn.inputs[0])
        bp = _bump(nt, b, sn.outputs[0], 0.25, 0.00004)
        _bevel(nt, b, 0.5, bp.inputs["Normal"])
        _noise_rough(nt, b, 0.46, 0.58, 400)
    elif kind == "alu":
        b.inputs["Base Color"].default_value = srgb(col)
        b.inputs["Metallic"].default_value = 1.0
        b.inputs["Anisotropic"].default_value = 0.25
        _noise_rough(nt, b, 0.22, 0.34)
        b.inputs["Coat Weight"].default_value = 0.15
        b.inputs["Coat Roughness"].default_value = 0.2
        _bevel(nt, b, 0.45)
    elif kind == "steel":
        b.inputs["Base Color"].default_value = (0.56, 0.57, 0.58, 1)
        b.inputs["Metallic"].default_value = 1.0
        _noise_rough(nt, b, 0.18, 0.28)
    elif kind == "cable":
        b.inputs["Base Color"].default_value = (0.5, 0.51, 0.52, 1)
        b.inputs["Metallic"].default_value = 1.0
        b.inputs["Roughness"].default_value = 0.3
        # twisted strands: diagonal bands round the cable
        _bump(nt, b, _uv_wave(nt, 0, 2.6, extra=(1, 0.45)), 0.45, 0.00015)
    elif kind == "sling":
        base = srgb(col)
        b.inputs["Base Color"].default_value = base
        b.inputs["Roughness"].default_value = 0.72
        b.inputs["Sheen Weight"].default_value = 0.18
        b.inputs["Sheen Roughness"].default_value = 0.5
        # woven webbing: weft ribs across the strap + fine warp lines
        weft = _uv_wave(nt, 0, 0.9)
        warp = _uv_wave(nt, 1, 0.5)
        mix = nt.nodes.new("ShaderNodeMath")
        mix.operation = "MULTIPLY_ADD"
        mix.inputs[1].default_value = 0.35
        nt.links.new(warp, mix.inputs[0])
        nt.links.new(weft, mix.inputs[2])
        _bump(nt, b, mix.outputs[0], 0.6, 0.00025)
        # darker in the weave grooves
        ramp = nt.nodes.new("ShaderNodeMapRange")
        ramp.inputs["From Min"].default_value = -1.3
        ramp.inputs["From Max"].default_value = 1.3
        ramp.inputs["To Min"].default_value = 0.72
        ramp.inputs["To Max"].default_value = 1.0
        nt.links.new(mix.outputs[0], ramp.inputs["Value"])
        tint = nt.nodes.new("ShaderNodeMix")
        tint.data_type = "RGBA"
        tint.blend_type = "MULTIPLY"
        tint.inputs["Factor"].default_value = 1.0
        tint.inputs["A"].default_value = base
        nt.links.new(ramp.outputs["Result"], tint.inputs["B"])
        cr = nt.nodes.new("ShaderNodeCombineColor")
        for ch in ("Red", "Green", "Blue"):
            nt.links.new(ramp.outputs["Result"], cr.inputs[ch])
        nt.links.new(cr.outputs["Color"], tint.inputs["B"])
        nt.links.new(tint.outputs["Result"], b.inputs["Base Color"])
    elif kind == "thread":
        b.inputs["Base Color"].default_value = srgb(col)
        b.inputs["Roughness"].default_value = 0.8
        b.inputs["Sheen Weight"].default_value = 0.5
        _bump(nt, b, _uv_wave(nt, 0, 0.7, extra=(1, 2.0)), 0.8, 0.0003)
    elif kind == "rubber":
        b.inputs["Base Color"].default_value = (0.025, 0.025, 0.028, 1)
        b.inputs["Roughness"].default_value = 0.55
    elif kind == "plastic":
        b.inputs["Base Color"].default_value = srgb(col)
        b.inputs["Roughness"].default_value = 0.38
        b.inputs["Coat Weight"].default_value = 0.2
    elif kind == "wall":
        b.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
        b.inputs["Roughness"].default_value = 0.9
    _MATS[key] = m
    return m


def add_mesh(name, mesh, mat_key, sharp_angle=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata((mesh.V * MM).tolist(), [], mesh.F.tolist())
    if mesh.FUV is not None and len(mesh.FUV) == len(mesh.F):
        uv = me.uv_layers.new(name="UVMap")
        uv.data.foreach_set("uv", (mesh.FUV * MM).astype(np.float32).ravel())
    me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    if sharp_angle is not None:
        me.set_sharp_from_angle(angle=math.radians(sharp_angle))
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(material(mat_key))
    return o


def shadow_wall(y_mm, size_m=3.0):
    me = bpy.data.meshes.new("wall")
    s = size_m / 2
    y = y_mm * MM
    me.from_pydata([(-s, y, -s), (s, y, -s), (s, y, s), (-s, y, s)], [], [(0, 1, 2, 3)])
    o = bpy.data.objects.new("wall", me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(material("wall"))
    o.is_shadow_catcher = True
    return o
