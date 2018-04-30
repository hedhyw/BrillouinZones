#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  hex_crystal.py
#
#  Copyright 2017 Maxim Krivchun <hedhyw>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
""" Model of simple hexagonal lattice """

import math

from crystal import Crystal
from sympy.geometry import Point

class HexCrystal(Crystal):
  """ Model of simple hexagonal lattice """

  def __init__(self, a, size, center):
    self._a = a
    super().__init__(size, center)

  def _translate(self, pos_x, pos_y):
    width = self._a
    points = []
    half_width = int(width / 2)
    side_length = int(width * math.sqrt(3))
    height = int(math.sqrt(side_length ** 2 - width ** 2 / 4))
    pos_y *= (side_length + height)
    pos_x *= width
    half_width_periodic = half_width if pos_y % 2 == 0 else 0

    points.append(Point(pos_x + half_width_periodic,
                        pos_y))
    points.append(Point(pos_x + half_width_periodic + width,
                        pos_y))
    points.append(Point(pos_x + half_width_periodic,
                        pos_y + side_length))
    points.append(Point(pos_x + half_width_periodic + width,
                        pos_y + side_length))
    points.append(Point(pos_x + half_width_periodic + half_width,
                        pos_y - height))
    points.append(Point(pos_x + half_width_periodic + half_width,
                        pos_y + side_length + height))

    return points
