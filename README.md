# SUHULET
Easy access to groups and layers using PyQGIS.

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

`G`: Group
- 
`G()` -> returns root  
`G("A")` -> group A  
`G("A/B")` -> group B

`Gs`: Groups
-
`Gs()` -> returns all groups in root  
`Gs("A/B")` returns `[group C, group D]`

`L`: Layer
-
`L("Layer")` -> returns the first layer (`QgsMapLayer`) named "Layer"   
              in layer tree. It is recursive.  
`L("A/B/C/LayerC")` -> `LayerC` (returns `QgsMapLayer`, not `QgsLayerTreeLayer`)  
`L("/A/B/C/LayerC/")` -> the same above. Ignores leading and trailing "/"  
`L("A/B/C")` -> raises an error. The last item have to be a `QgsMapLayer`.  
`L("A/B/C")`

`Ls`: Layers
-
`Ls()` -> all root layers, except groups  
`Ls("A/B/C")` -> `[LayerC, LayerE]` - `QgsMapLayers`  