#!/usr/bin/env python
# coding: utf-8

r"""Exporting a single shape to BREP"""

import logging

from OCC import BRepPrimAPI

from OCCDataExchange.brep import BrepExporter
from OCCDataExchange.utils import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

# First create a simple shape to export
box_shape = BRepPrimAPI.BRepPrimAPI_MakeBox(50, 50, 50).Shape()

# Export to BREP
filename = path_from_file(__file__, "./models_out/box.brep")
step_exporter = BrepExporter(filename)
step_exporter.set_shape(box_shape)
step_exporter.write_file()
