#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Model of simple trigonal lattice """

from crystal import Crystal
from sympy.geometry import Point

class ParallelogramCrystal(Crystal):
  """ Model of simple trigonal lattice """

  def __init__(self, a, size, center):
    self._a = a
    super().__init__(size, center)

  def _translate(self, pos_x, pos_y):
    half_a_periodic = self._a / 2 if pos_y % 2 == 0 else 0
    return [Point(pos_x * self._a + half_a_periodic, pos_y * self._a)]
