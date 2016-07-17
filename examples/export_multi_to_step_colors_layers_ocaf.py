#!/usr/bin/env python
# coding: utf-8

r"""Exporting multiple shapes to STEP with colors and layers"""

import logging

from OCC import BRepPrimAPI
from OCC.Display import SimpleGui

from OCCDataExchange.step_ocaf import StepOcafExporter, StepOcafImporter

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

# First create a simple shape to export
my_box_shape = BRepPrimAPI.BRepPrimAPI_MakeBox(50, 50, 50).Shape()
my_sphere_shape = BRepPrimAPI.BRepPrimAPI_MakeSphere(20).Shape()

# Export to STEP
my_step_exporter = StepOcafExporter("./models_out/result_export_multi_ocaf.stp")
my_step_exporter.set_color(r=1, g=0, b=0)  # red
my_step_exporter.set_layer('red')
my_step_exporter.add_shape(my_box_shape)
my_step_exporter.set_color(r=0, g=1, b=0)  # green
my_step_exporter.set_layer('green')
my_step_exporter.add_shape(my_sphere_shape)
my_step_exporter.write_file()

# Read the exported STEP file back
my_step_importer = StepOcafImporter("./models_out/result_export_multi_ocaf.stp")
# step = OCCDataExchange.step_ocaf.StepOcafImport("./models_in/66m.stp")
# step.read_file()
the_shapes = my_step_importer.shapes
the_colors = my_step_importer.colors
the_layers = my_step_importer.layers
the_layers_str = my_step_importer.layers_str

print("Number of shapes : %i " % len(the_shapes))

display, start_display, add_menu, add_function_to_menu = SimpleGui.init_display()

for i, shape in enumerate(the_shapes):
    display.DisplayShape(shape, color=the_colors[i])
    print(the_layers_str[i])

display.View_Iso()
display.FitAll()
start_display()
