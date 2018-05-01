#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
