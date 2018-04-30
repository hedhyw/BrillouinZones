#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  hexagonal_close_packed_reciprocal_lattice.py
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

"""Hexagonal close packed reciprocal lattice."""

from decimal import Decimal

from geometry import Vector3D
from reciprocal_lattice import ReciprocalLattice


class HexagonalClosePackedReciprocalLattice(ReciprocalLattice):
  """Model of the hexagonal close packed reciprocal lattice."""

  def __init__(self, a, size, center):
    self._a = a
    super().__init__(size, center)

  @property
  def primitive_vectors(self):
    a = Decimal(self._a)
    half_a = Decimal(self._a / 2.)
    c = Decimal(8 / 3.).sqrt() * a
    return (
        Vector3D(a, 0, 0),
        Vector3D(half_a, half_a * Decimal(3).sqrt(), 0),
        Vector3D(0, 0, c)
    )
