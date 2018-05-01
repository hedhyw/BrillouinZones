#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
