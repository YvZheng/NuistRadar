"""
this code is modified from pyart.graph.cm file, developed by Helmus, J.J. & Collis, S.M.
https://github.com/ARM-DOE/pyart
==============

Radar related colormaps.

.. autosummary::
    :toctree: generated/

    revcmap
    _reverser
    _reverse_cmap_spec
    _generate_cmap


Available colormaps, reversed versions (_r) are also provided, these
colormaps are available within matplotlib with names 'pyart_COLORMAP':

    * BlueBrown10
    * BlueBrown11
    * BrBu10
    * BrBu12
    * Bu10
    * Bu7
    * BuDOr12
    * BuDOr18
    * BuDRd12
    * BuDRd18
    * BuGr14
    * BuGy8
    * BuOr10
    * BuOr12
    * BuOr8
    * BuOrR14
    * Carbone11
    * Carbone17
    * Carbone42
    * Cat12
    * EWilson17
    * GrMg16
    * Gray5
    * Gray9
    * NWSRef
    * NWSVel
    * NWS_SPW
    * PD17
    * RRate11
    * RdYlBu11b
    * RefDiff
    * SCook18
    * StepSeq25
    * SymGray12
    * Theodore16
    * Wild25
    * LangRainbow12
    * CN_ref
    * CN_vel
    * CN_hcl

"""
# the code for colormaps in this file were adapted from pyart by Helmus, J.J. & Collis, S.M.
# https://github.com/ARM-DOE/pyart

# This file was adapted from the cm.py file of the matplotlib project,
# http://matplotlib.org/.
# Copyright (c) 2012-2013 Matplotlib Development Team; All Rights Reserved

from __future__ import print_function, division
import warnings

import matplotlib as mpl
import matplotlib.colors as colors
from ._cm import datad
import matplotlib.cm

import matplotlib
from matplotlib import colors
# 检查 Matplotlib 版本
version = matplotlib.__version__.split('.')
major_version = int(version[0])
minor_version = int(version[1])

# 根据版本选择适当的 colormap 注册方法
if major_version > 3 or (major_version == 3 and minor_version >= 9):
    # Matplotlib 3.9.0 及以上版本
    register_cmap = matplotlib.colormaps.register
else:
    # Matplotlib 3.8.x 及以下版本
    register_cmap = matplotlib.cm.register_cmap

cmap_d = dict()

# reverse all the colormaps.
# reversed colormaps have '_r' appended to the name.


def _reverser(f):
    """ perform reversal. """
    def freversed(x):
        """ f specific reverser. """
        return f(1 - x)
    return freversed


def revcmap(data):
    """Can only handle specification *data* in dictionary format."""
    data_r = {}
    for key, val in data.items():
        if callable(val):
            valnew = _reverser(val)
            # This doesn't work: lambda x: val(1-x)
            # The same "val" (the first one) is used
            # each time, so the colors are identical
            # and the result is shades of gray.
        else:
            # Flip x and exchange the y values facing x = 0 and x = 1.
            valnew = [(1.0 - x, y1, y0) for x, y0, y1 in reversed(val)]
        data_r[key] = valnew
    return data_r

#
# def _reverse_cmap_spec(spec):
#     """Reverses cmap specification *spec*, can handle both dict and tuple
#     type specs."""
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore", FutureWarning)
#         if 'red' in spec:
#             return revcmap(spec)
#         else:
#             revspec = list(reversed(spec))
#             if len(revspec[0]) == 2:    # e.g., (1, (1.0, 0.0, 1.0))
#                 revspec = [(1.0 - a, b) for a, b in revspec]
#             return revspec
def _reverse_cmap_spec(spec):
    """Reverses cmap specification *spec*, can handle both dict and tuple
    type specs."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        if isinstance(spec, dict) and "red" in spec.keys():
            return revcmap(spec)
        else:
            revspec = list(reversed(spec))
            if len(revspec[0]) == 2:  # e.g., (1, (1.0, 0.0, 1.0))
                revspec = [(1.0 - a, b) for a, b in revspec]
            return revspec

def _generate_cmap(name, lutsize):
    """Generates the requested cmap from it's name *name*.  The lut size is
    *lutsize*."""

    spec = datad[name]

    # Generate the colormap object.
    if isinstance(spec, dict) and "red" in spec.keys():
        return colors.LinearSegmentedColormap(name, spec, lutsize)
    else:
        return colors.LinearSegmentedColormap.from_list(name, spec, lutsize)

LUTSIZE = mpl.rcParams['image.lut']

# need this list because datad is changed in loop
_cmapnames = list(datad.keys())

# Generate the reversed specifications ...

for cmapname in _cmapnames:
    spec = datad[cmapname]
    spec_reversed = _reverse_cmap_spec(spec)
    datad[cmapname + '_r'] = spec_reversed

# Precache the cmaps with ``lutsize = LUTSIZE`` ...

# Use datad.keys() to also add the reversed ones added in the section above:
for cmapname in datad.keys():
    cmap_d[cmapname] = _generate_cmap(cmapname, LUTSIZE)

locals().update(cmap_d)

# register the colormaps so that can be accessed with the names pyart_XXX
for name, cmap in cmap_d.items():
    if name in ["ref", "vel"]:
        register_cmap(name="CN_"+name, cmap=cmap)
    else:
        full_name = 'copy_pyart_' + name
        register_cmap(name=full_name, cmap=cmap)

hid_colors = ['LightBlue', 'MediumBlue', 'DarkOrange', 'LightPink',
              'Cyan', 'DarkGray', 'Lime', 'Yellow', 'Red', 'Fuchsia']
cmaphid = colors.ListedColormap(hid_colors)
register_cmap(name="CN_hcl", cmap=cmaphid)
