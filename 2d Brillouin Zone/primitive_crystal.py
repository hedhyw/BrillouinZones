#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
