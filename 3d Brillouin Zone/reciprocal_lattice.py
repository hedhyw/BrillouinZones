#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Reciprocal lattice."""

import abc
import math
from decimal import Decimal

from geometry import GeometryUtils

DISTANCE_EPS = 0.01 # Approximation in the distance between atoms

class ReciprocalLattice(object):
  """Model of reciprocal lattice."""

  def __init__(self, size, center):
    self._center = center
    self.__calculate(size)

  def __calculate(self, size):
    points = set()
    new_points = [(self._center, 0)]
    while new_points:
      point, i = new_points.pop()
      if i > size:
        continue
      points.add(point)
      for vec in self.reciprocal_primitive_vectors:
        new_points.append((point + vec, i + 1))
        new_points.append((point - vec, i + 1))
    self._points = list(points)

  def points(self):
    """Return generator of nearest points out the center in the crystal."""
    return ReciprocalLattice.nearly_points(self._points, self._center)

  @abc.abstractmethod
  def primitive_vectors(self):
    """Return three primitive vectors of the lattice."""
    return ()

  @property
  def reciprocal_primitive_vectors(self):
    """Return three reciprocal primitive vectors of the lattice."""
    a = self.primitive_vectors[0]
    b = self.primitive_vectors[1]
    c = self.primitive_vectors[2]
    factor = (Decimal(2 * math.pi) /
              GeometryUtils.dot_product(a, GeometryUtils.cross_product(b, c)))
    return (GeometryUtils.cross_product(b, c) * factor,
            GeometryUtils.cross_product(c, a) * factor,
            GeometryUtils.cross_product(a, b) * factor,)

  @staticmethod
  def nearly_points(points, center):
    """Return generator of the nearest points."""
    points = [(GeometryUtils.distance(center, point), point) for point in points]
    points.sort(key=lambda v: v[0])
    distance = None
    if points:
      distance = points[0][0]
    yield_points = []
    for (distance_to_center, point) in points: # first is center
      if abs(distance_to_center - distance) > DISTANCE_EPS:
        distance = distance_to_center
        yield set(yield_points)
        yield_points = []
      yield_points.append(point)
