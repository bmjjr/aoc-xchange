#!/usr/bin/env python
# coding: utf-8

r"""STL file reading tests"""

import logging

import pytest
from OCC import TopoDS
from OCCUtils.Topology import Topo

from OCCDataExchange.stl import StlImporter
from OCCDataExchange.utils import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')


def test_iges_importer_wrong_path():
    r"""Wrong filename"""
    with pytest.raises(AssertionError):
        StlImporter("C:/stupid-filename.bad_extension")


def test_stl_importer_wrong_extension():
    r"""wrong file format (i.e. trying to read a step file with iges importer)"""
    with pytest.raises(AssertionError):
        StlImporter(path_from_file(__file__, "./models_in/aube_pleine.stp"))


# Reading an empty or corrupt stl file seems to block everything

# def test_stl_importer_wrong_file_content():
#     r"""wrong file content"""
#     with pytest.raises(OCCDataExchange.exceptions.IgesFileReadException):
#         OCCDataExchange.stl.StlImporter(OCCDataExchange.path_from_file(__file__, "./models_in/empty.stl"))


def test_stl_importer_happy_path():
    r"""happy path"""
    importer = StlImporter(path_from_file(__file__, "./models_in/box_binary.stl"))
    assert isinstance(importer.shape, TopoDS.TopoDS_Shape)


def test_stl_importer_happy_topology():
    r"""import iges file containing a box and test topology"""

    # binary STL
    importer = StlImporter(path_from_file(__file__, "./models_in/box_binary.stl"))
    topo = Topo(importer.shape)
    # assert len(topo.solids()) == 1
    assert len([i for i in topo.shells()]) == 1
    assert next(topo.shells()).Closed() is True  # direct method on TopoDS_Shell
    assert len([i for i in topo.faces()]) == 108
    assert len([i for i in topo.edges()]) == 162

    # ascii STL
    importer = StlImporter(path_from_file(__file__, "./models_in/box_ascii.stl"))
    topo = Topo(importer.shape)
    # assert len(topo.solids) == 1
    assert len([i for i in topo.shells()]) == 1
    assert next(topo.shells()).Closed() is True
    assert len([i for i in topo.faces()]) == 108
    assert len([i for i in topo.edges()]) == 162


def test_stl_importer_2_boxes():
    r"""Import an iges file containing 2 distinct boxes and test topology

    Notes
    -----
    This shows the current limitations of the IgesImporter as 2 boxes cannot be distinguished from one another

    """
    # binary STL
    importer = StlImporter(path_from_file(__file__, "./models_in/2_boxes_binary.stl"))

    topo = Topo(importer.shape)
    assert len([i for i in topo.shells()]) == 2
    assert next(topo.shells()).Closed() is True
    assert [i for i in topo.shells()][1].Closed() is True
    assert topo.number_of_faces() == 108 * 2
    assert topo.number_of_edges() == 162 * 2

    # ascii STL
    importer = StlImporter(path_from_file(__file__, "./models_in/2_boxes_ascii.stl"))

    topo = Topo(importer.shape)
    assert len([i for i in topo.shells()]) == 2
    assert next(topo.shells()).Closed() is True
    assert [i for i in topo.shells()][1].Closed() is True
    assert topo.number_of_faces() == 108 * 2
    assert topo.number_of_edges() == 162 * 2


