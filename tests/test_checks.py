#!/usr/bin/env python
# coding: utf-8

r"""checks.py module tests"""

import pytest
from OCC import BRepBuilderAPI
from OCC import TopoDS
from OCC import gp
from OCCUtils.Topology import Topo

from OCCDataExchange.checks import check_importer_filename, check_exporter_filename, check_overwrite, check_shape
from OCCDataExchange.utils import path_from_file


def test_check_importer_filename_inexistent_file():
    r"""Inexistent file test for check_importer_filename()"""
    with pytest.raises(AssertionError):
        check_importer_filename(path_from_file(__file__, "./models_out/dummy.igs"))


def test_check_importer_filename_wrong_extension():
    r"""Wrong extension test for check_importer_filename()"""
    with pytest.raises(AssertionError):
        check_importer_filename(path_from_file(__file__, "./models_in/box.igs"),
                                ["step"])


def test_check_importer_filename_happy_path():
    r"""Happy path for check_importer_filename()"""
    check_importer_filename(path_from_file(__file__, "./models_in/box.igs"))


def test_check_exporter_filename_inexistent_directory():
    r"""Inexistent directory test for check_exporter_filename()"""
    with pytest.raises(AssertionError):
        check_exporter_filename(path_from_file(__file__,
                                               "./inexistent-dir/dummy.igs"))


def test_check_exporter_filename_wrong_extension():
    r"""Wrong extension test for check_exporter_filename()"""
    with pytest.raises(AssertionError):
        check_exporter_filename(
            path_from_file(__file__, "./models_out/box.igs"),
            ["step"])


def test_check_exporter_filename_happy_path():
    r"""Happy path for check_exporter_filename()"""
    check_exporter_filename(
        path_from_file(__file__, "./models_out/box.igs"))


def test_check_overwrite():
    r"""check_overwrite() tests"""
    # file exists
    assert check_overwrite(
        path_from_file(__file__, "./models_in/box.igs")) is True

    # file does not exist
    assert check_overwrite(
        path_from_file(__file__, "./models_in/bo_.igs")) is False


def test_check_shape():
    r"""check_shape() tests"""
    # Null shapes should raise a ValueError
    with pytest.raises(ValueError):
        check_shape(TopoDS.TopoDS_Shape())
    with pytest.raises(ValueError):
        check_shape(TopoDS.TopoDS_Shell())

    builderapi_makeedge = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(gp.gp_Pnt(), gp.gp_Pnt(10, 10, 10))
    shape = builderapi_makeedge.Shape()

    # a ValueError should be raised is check_shape() is not give a TopoDS_Shape or subclass
    with pytest.raises(ValueError):
        check_shape(gp.gp_Pnt())
    with pytest.raises(ValueError):
        check_shape(builderapi_makeedge)

    # a TopoDS_Shape should pass the check without raising any exception
    check_shape(shape)

    # a subclass of shape should not raise any exception
    check_shape(next(Topo(shape).edges()))


