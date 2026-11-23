%cd "C:\Users\trish\Desktop\laser cut\Challange_1_LaserCut-GmbH\DSF4E_Challenge1-2"

from pathlib import Path

from helpers import (
    get_cutting_length,
    get_dxf_bounds,
    get_number_of_holes,
    load_dxf_geometry,
    plot_dxf,
)


path = r"10991360\Geo (10).DXF"

print("DXF path:", path)
print("get_dxf_bounds:", get_dxf_bounds(path))
print("get_cutting_length:", get_cutting_length(path))
print("get_number_of_holes:", get_number_of_holes(path))

polygons, lines = load_dxf_geometry(path)
print("load_dxf_geometry:")
print("  polygons:", len(polygons))
print("  lines:", len(lines))

print("plot_dxf: opening plot")
plot_dxf(path)

print("bounding box area:", bounding_box_area(path))