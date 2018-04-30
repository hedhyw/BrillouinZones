#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  crystal.py
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

""" Primitive model of crystal """

import abc

class Crystal:
  """ Primitive model of crystal """

  def __init__(self, size, center):
    self._center = center
    self._points = []
    for pos_y in range(-size, size + 1):
      for pos_x in range(-size, size + 1):
        self._points += self._translate(pos_x, pos_y)

  @abc.abstractmethod
  def _translate(self, pos_x, pos_y):
    pass

  def points(self):
    """ Return generator of nearest points out the center in the crystal """

    return Crystal.nearly_points(self._points, self._center)

  @staticmethod
  def nearly_points(points, center):
    """ Return generator of nearest points """

    points = list(map(
        lambda point:
        (point.distance(center), point),
        points))
    points.sort(key=lambda v: v[0])
    distance = None
    if points:
      distance = points[0][0]
    yield_points = []
    for (distance_to_center, point) in points: # first is center
      if abs(distance_to_center - distance) > 0.1:
        distance = distance_to_center
        yield set(yield_points)
        yield_points = []
      yield_points.append(point)
