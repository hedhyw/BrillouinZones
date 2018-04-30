#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  primitive_crystal.py
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

""" Model of simple cubic lattice """

from crystal import Crystal
from sympy.geometry import Point

class PrimitiveCrystal(Crystal):
  """ Model of simple cubic lattice """

  def __init__(self, a, size, center):
    self._a = a
    super().__init__(size, center)

  def _translate(self, pos_x, pos_y):
    return [Point(pos_x, pos_y) * self._a]
