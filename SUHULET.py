# -*- coding: utf-8 -*-
"""
*******************************************************
                       SUHULET
                                 
Easy accsee to liayer and group in QGIS Layers panel

                              -------------------
        begin                : 2022-01-31
        author               : Kadir Şahbaz
        email                : kadirsahbaz@htomail.com
 *******************************************************

Sample Layer Tree:

A/                  Group
├─ LayerA           Layer
├─ B/               Group
│  ├─ LayerB        Layer
│  ├─ C/            Group
│  │  ├─ LayerC     Layer
│  │  ├─ LayerE     Layer
│  ├─ D/            Group
│  │  ├─ LayerD     Layer

G: Group
G() -> returns root
G("A") -> group A
G("A/B") -> group B

Gs: Groups
Gs() -> returns all group in root
Gs("A/B") returns [group C, group D]

L: Layer
L("Layer") -> returns the first layer (QgsMapLayer) named "Layer"   
              in layer tree. It is recursive. 
L("A/B/C/LayerC") -> LayerC (returns QgsMapLayer, not QgsLayerTreeLayer)
L("/A/B/C/LayerC/") -> the same above. Ignores leading and trailing "/"               
L("A/B/C") -> rises an error. The last item have to be a QgsMapLayer.
L("A/B/C")

Ls: Layers
Ls() -> all root layers, except groups
Ls("A/B/C") -> [LayerC, LayerE] - QgsMapLayers
"""

from qgis.core import (QgsProject, QgsMapLayer, QgsLayerTreeGroup, QgsLayerTreeLayer)


def L(layer_path):
    """ Return the layer given in path
    Example: Layer("group/subgroup/layer")
    """

    layer = None
    group = QgsProject.instance().layerTreeRoot()
    items =  layer_path.strip("/").split('/')
    if len(items) == 1:
        try:
            layer = QgsProject.instance().mapLayersByName(items[0])[0]
        except IndexError:
            raise Exception(f"Not found")
    else:
        group = G("/".join(items[:-1]))
        layer = [l for l in group.children()
                 if l.name()==items[-1] and isinstance(l, QgsLayerTreeLayer)]
        if not layer:
            raise Exception(f"Not found")

        layer = layer[0].layer()

    return layer


def Ls(group_path: str = None, recursive: bool = False):
    """ Return all layers (QgsMapLayer) in group path
    If group_path is None, returns all root layers
    """

    group = G(group_path)
    layers = [l.layer() for l in group.children()
                if isinstance(l, QgsLayerTreeLayer)]

    return layers


def G(group_path: str = None):
    """ Return the group given in path
    If group_path is None, returns root
    """

    group = QgsProject.instance().layerTreeRoot()

    if group_path:
        groups =  group_path.strip("/").split('/')
        for g in groups:
            group = group.findGroup(g)
            if not group:
                raise Exception(f"Not found")

    return group


def Gs(group_path: str = None):
    """ Return all groups given in path. Not recursive """

    return G(group_path).findGroups()


Layer, Layers = L, Ls
Group, Groups = G, Gs
