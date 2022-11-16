# -*- coding: utf-8 -*-
#
#  Copyright 2021, 2022 Ramil Nugmanov <nougmanoff@protonmail.com>
#  This file is part of chython.
#
#  chython is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from itertools import zip_longest
from typing import List, Optional
from ..containers import MoleculeContainer
from ..algorithms.depict import _render_config, _graph_svg


def grid_depict(molecules: List[MoleculeContainer], labels: Optional[List[str]] = None, *, cols: int = 3):
    """
    Depict molecules grid.

    :param molecules: list of molecules
    :param labels: optional list of text labels
    :param cols: number of molecules per row
    """
    font_size = _render_config['font_size']
    symbols_font_style = _render_config['symbols_font_style']
    font125 = 1.25 * font_size
    font75 = .75 * font_size

    planes = []
    render = []
    render_labels = []
    shift_y = 0.
    shift_x = 0.
    if labels is not None:
        assert len(molecules) == len(labels)
        labels = iter(labels)

    for ms in zip_longest(*[iter(molecules)] * cols):
        height = 0.
        for m in ms:
            if m is None:
                break
            min_y = min(y for x, y in m._plane.values())
            max_y = max(y for x, y in m._plane.values())
            h = max_y - min_y
            if height < h:  # get height of row
                height = h
            planes.append(m._plane.copy())

        max_x = 0.
        for m in ms:
            if m is None:
                break
            if labels is not None:
                render_labels.append(f'    <text x="{max_x:.2f}" y="{-shift_y:.2f}">{next(labels)}</text>')
                y = shift_y - height / 2. - font125  # blank
            else:
                y = shift_y - height / 2.
            max_x = m._fix_plane_mean(max_x, y) + 2.
            render.append(m.depict(_embedding=True)[:5])
            if max_x > shift_x:  # get total width
                shift_x = max_x
        shift_y -= height + 2.

    # restore planes
    for p, m in zip(planes, molecules):
        m._plane = p

    width = shift_x + 3.0 * font_size
    height = -shift_y + 2.5 * font_size
    svg = [f'<svg width="{width:.2f}cm" height="{height:.2f}cm" '
           f'viewBox="{-font125:.2f} {-font125:.2f} {width:.2f} {height:.2f}" '
           'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">']
    for atoms, bonds, define, masks, uid in render:
        svg.extend(_graph_svg(atoms, bonds, define, masks, uid, -font125, -font125, width, height))
    svg.append(f'  <g font-size="{font75:.2f}" font-family="{symbols_font_style}">')
    svg.extend(render_labels)
    svg.append('  </g>')
    svg.append('</svg>')
    return '\n'.join(svg)


class GridDepict:
    """
    Grid depict for Jupyter notebooks.
    """
    def __init__(self, molecules: List[MoleculeContainer], labels: Optional[List[str]] = None, *, cols: int = 3):
        """
        :param molecules: list of molecules
        :param labels: optional list of text labels
        :param cols: number of molecules per row
        """
        self.molecules = molecules
        self.labels = labels
        self.cols = cols

    def _repr_svg_(self):
        return grid_depict(self.molecules, self.labels, cols=self.cols)


__all__ = ['grid_depict', 'GridDepict']
