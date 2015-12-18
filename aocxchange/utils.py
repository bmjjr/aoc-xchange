#!/usr/bin/python
# coding: utf-8

r"""utils module of occaddons.dataexchange"""

from __future__ import print_function

import os

from OCC.IGESControl import *
from OCC.STEPControl import *


def shape_to_file(shape, pth, filename, format='iges'):
    r"""write a Shape to a .iges .brep .stl or .step file

    Parameters
    ----------
    shape
    pth
    filename
    format

    """
    _pth = os.path.join(pth, filename)
    assert not os.path.isdir(_pth), 'wrong path, filename'
    _file = "%s.%s" % (_pth, format)

    _formats = ['iges', 'igs', 'step', 'stp', 'brep', 'stl']
    assert format in _formats, '%s is not a readable format, should be one of %s ' % (format, _formats)

    if format in ['iges', 'igs']:
        i = IGESControl_Controller()
        i.Init()
        writer = IGESControl_Writer()
        writer.AddShape(shape)
        writer.Write(_file)
        return _file

    elif format in ['step', 'stp']:
        i = STEPControl_Controller()
        i.Init()
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        writer.Write(_file)
        return _file

    elif format == 'brep':
        from OCC import TopoDS, BRep, BRepTools
        # shape = TopoDS.TopoDS_Shape()
        builder = BRep.BRep_Builder()
        BRepTools.breptools_Write(shape, _file, builder)

    elif format == 'stl':
        from OCC import TopoDS, StlAPI
        # shape = TopoDS.TopoDS_Shape()
        stl_writer = StlAPI.StlAPI_Writer()
        stl_writer.Write(shape, _file)

    else:
        raise TypeError('format should be one of [iges,igs], [step,stp], brep, stl\ngot %s' % format)


def file_to_shape(pth):
    r"""get a Shape from an .iges or .step file

    Parameters
    ----------
    pth : str

    """
    assert os.path.isfile(pth), '%s is not a valid directory' % pth
    ext = os.path.splitext(pth)[1]
    print('ext', ext)
    assert ext in ['.iges', '.igs', '.stp', '.step', '.brep', '.stl'], '%s is not an readable format' % ext

    if ext in ['.iges', '.igs']:
        __i = IGESControl_Controller()
        __i.Init()
        reader = IGESControl_Reader()

    elif ext in ['.step', '.stp']:
        reader = STEPControl_Reader()

    elif ext == '.brep':
        from OCC import TopoDS, BRep, BRepTools
        shape = TopoDS.TopoDS_Shape()
        builder = BRep.BRep_Builder()
        BRepTools.BRepTools().Read(shape, pth, builder)
        return shape

    elif ext == '.stl':
        from OCC import TopoDS, StlAPI
        shape = TopoDS.TopoDS_Shape()
        stl_reader = StlAPI.StlAPI_Reader()
        stl_reader.Read(shape, pth)
        return shape

    reader.ReadFile(pth)
    n_translated = reader.TransferRoots()
    shape = reader.OneShape()
    del reader
    return shape


def path_from_file(file_origin, relative_path):
    r"""Builds an absolute path from a file using a relative path

    Parameters
    ----------
    file_origin : str
    relative_path : str
    """
    dir_of_file_origin = os.path.dirname(os.path.realpath(file_origin))
    return os.path.abspath(os.path.join(dir_of_file_origin, relative_path))


def extract_file_extension(filename):
    r"""Extract the extension from the file name

    Parameters
    ----------
    filename : str
        Path to the file

    """
    return (filename.split("/")[-1]).split(".")[-1]