#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  geometry.py
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

"""Module for geometric calculations."""

import math
from decimal import Decimal

POINT_APROX_DIGITS = 4
NORMAL_VECTOR = (2, 3, 4) # for angle calculation

class Segment3D(object):
  """The mathematical model of a line segmnet
     in three-dimensional space.

     Keyword arguments:
       first_point -- first Point3D
       second_point -- second Point3D
  """

  def __init__(self, first_point, second_point):
    self._first_point = first_point
    self._second_point = second_point
    self._length = GeometryUtils.distance(self._first_point, self._second_point)

  @property
  def center(self):
    """Return Point3D that is center of a line segment."""
    return (self._first_point + self._second_point) * 0.5

  @property
  def points(self):
    """Return the end points of a line segment."""
    return (self._first_point, self._second_point)

  @property
  def first_point(self):
    """Return the first end point of the segment."""
    return self._first_point

  @property
  def second_point(self):
    """Return the second end point of the segment."""
    return self._second_point

  @property
  def line(self):
    """Return a line that contains a line segment."""
    vector = Vector3D.by_points(self.first_point, self.second_point)
    return Line3D(self.first_point, vector)

  @property
  def length(self):
    """Return the size of a line segment."""
    return self._length

  def is_contain_point(self, point, eps=Decimal(0.01)):
    """Check that the segment contains a point."""
    distance_a = GeometryUtils.distance(point, self._first_point)
    distance_b = GeometryUtils.distance(point, self._second_point)
    return abs(self.length - distance_a - distance_b) <= eps * self.length


class Point3D(object):
  """The mathematical model of a point in three-dimensional space.

    Keyword arguments:
      x -- x coordinate or tuple if y and z are None
      y -- y coordinate (default None)
      z -- z coordinate (default None)
  """

  def __init__(self, x, y=None, z=None):
    if y is None and z is None:
      self._x = x[0]
      self._y = x[1]
      self._z = x[2]
    else:
      self._x = x
      self._y = y
      self._z = z
    if self._z is None:
      self._z = 0
    self._x = Decimal(self._x)
    self._y = Decimal(self._y)
    self._z = Decimal(self._z)

  def __eq__(self, other):
    if isinstance(self, other.__class__):
      return (round(self.x, POINT_APROX_DIGITS) ==
              round(self.x, POINT_APROX_DIGITS) and
              round(self.y, POINT_APROX_DIGITS) ==
              round(self.y, POINT_APROX_DIGITS) and
              round(self.z, POINT_APROX_DIGITS) ==
              round(self.z, POINT_APROX_DIGITS))
    return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
    return hash((round(self._x, POINT_APROX_DIGITS) + Decimal(1e8),
                 round(self._y, POINT_APROX_DIGITS) + Decimal(1e4),
                 round(self._z, POINT_APROX_DIGITS)))

  def __repr__(self):
    return ('<{0} object {{ x: {1}, y: {2}, z: {3} }}>'
            .format(self.__class__.__name__, self.x, self.y, self.z))

  def __add__(self, another_point):
    another_point = tuple(another_point)
    point = Point3D(self.x + another_point[0],
                    self.y + another_point[1],
                    self.z + another_point[2])
    return point

  def __sub__(self, another_point):
    another_point = tuple(another_point)
    point = Point3D(self.x - another_point[0],
                    self.y - another_point[1],
                    self.z - another_point[2])
    return point

  def __mul__(self, k):
    k = Decimal(k)
    return Point3D(self.x * k, self.y * k, self.z * k)

  def __iter__(self):
    yield self.x
    yield self.y
    yield self.z

  @property
  def coords(self):
    """Return tuple that contains the coordinates of the point: x, y, z."""
    return tuple(self.__iter__)

  @property
  def x(self):
    """Return x coordinate of the point."""
    return self._x

  @property
  def y(self):
    """Return y coordinate of the point."""
    return self._y

  @property
  def z(self):
    """Return z coordinate of the point."""
    return self._z

class Vector3D(Point3D):
  """The mathematical model of a vector in three-dimensional space."""

  def __init(self, x, y, z=None):
    super(self, x, y, z)

  @staticmethod
  def by_points(first_point, second_point):
    """Return Vector3D which is defined by two points."""
    point = second_point - first_point
    point.__class__ = Vector3D
    if point.module == 0:
      raise TypeError("Two points must be different")
    return point

  @property
  def normalized(self):
    """Return Vector3D which is scaled so that length is 1."""
    k = self.module
    return Vector3D(self.x / k, self.y / k, self.z / k)

  @property
  def module(self):
    """Return absolute value of the vector."""
    return (self.x ** 2 + self.y ** 2 + self.z ** 2).sqrt()

class Plane(object):
  """The mathematical model of a plane
  by normal vector and point [A*x+B*y+C*y+D=0].
  """

  def __init__(self, point, normal_vector):
    self._normal_vector = normal_vector.normalized
    self._point = point

  def __repr__(self):
    return ('<{0} object {{ normal_vector: {1}, point: {2} }}>'
            .format(self.__class__.__name__,
                    tuple(self._normal_vector),
                    tuple(self._point)))

  def __hash__(self):
    return hash(tuple(self._normal_vector) + tuple(self._point))

  @property
  def A(self):
    """Return the x coordinate of normal vector."""
    return self._normal_vector.x

  @property
  def B(self):
    """Return the y coordinate of normal vector."""
    return self._normal_vector.y

  @property
  def C(self):
    """Return the z coordinate of normal vector."""
    return self._normal_vector.z

  @property
  def D(self):
    """Return the D = -x0*A - y0*B - z0*C,
       where x0, y0, z0 are coordinates of point on the plane;
       A, B, C are coordinates of normal vector.
    """
    return -self.x0 * self.A - self.y0 * self.B - self.z0 * self.C

  @property
  def x0(self):
    """Return x coordinate of point on the plane"""
    return self._point.x

  @property
  def y0(self):
    """Return y coordinate of point on the plane."""
    return self._point.y

  @property
  def z0(self):
    """Return z coordinate of point on the plane."""
    return self._point.z

class Line3D(object):
  """The mathematical model of a line
     by point and directing vector
     in three-dimensional space.
  """

  def __init__(self, point, directing_vector):
    self._directing_vector = directing_vector.normalized
    self._point = point

  def __repr__(self):
    return ('<{0} object {{ directing_vector: {1}, point: {2} }}>'
            .format(self.__class__.__name__,
                    tuple(self._directing_vector),
                    tuple(self._point)))

  @property
  def l(self):
    """The x coordinate of directing vector."""
    return self._directing_vector.x

  @property
  def m(self):
    """The y coordinate of directing vector."""
    return self._directing_vector.y

  @property
  def n(self):
    """The z coordinate of directing vector."""
    return self._directing_vector.z

  @property
  def x0(self):
    """The x coordinate of point on the line."""
    return self._point.x

  @property
  def y0(self):
    """The y coordinate of point on the line."""
    return self._point.y

  @property
  def z0(self):
    """The z coordinate of point on the line."""
    return self._point.z

class GeometryUtils(object):
  """Utils for working with geometric primitives."""

  @staticmethod
  def intersection(first_entity, second_entity):
    """Return an intersection of two entities
       if entities are Line3D/Segment3D and Plane return Point3D or None
       if entities are Planes return Line3D or None.
    """
    # Line3d - Plane
    if isinstance(first_entity, Plane) and isinstance(second_entity, Line3D):
      return GeometryUtils.plane_line_intersection(first_entity, second_entity)
    if isinstance(first_entity, Line3D) and isinstance(second_entity, Plane):
      return GeometryUtils.plane_line_intersection(second_entity, first_entity)
    # Segment3D - Plane
    if isinstance(first_entity, Plane) and isinstance(second_entity, Segment3D):
      return GeometryUtils.plane_segment_intersection(first_entity, second_entity)
    if isinstance(first_entity, Segment3D) and isinstance(second_entity, Plane):
      return GeometryUtils.plane_segment_intersection(second_entity, first_entity)
    # Plane - Plane
    if isinstance(first_entity, Plane) and isinstance(second_entity, Plane):
      return GeometryUtils.plane_plane_intersection(first_entity, second_entity)
    raise ValueError("It's not supported yet")

  @staticmethod
  def __cramer_solve(mat):
    """Solve a system of two equations by the Cramer method

       Keyword arguments:
         mat -- tuple(A, B, C, D, E, F)
         (A B | E)
         (C D | F)
    """
    A, B, C, D, E, F = mat
    calculate_det = lambda A, B, C, D: A * D - C * B
    det = calculate_det(A, B, C, D)
    if det == 0:
      return None
    det0 = calculate_det(E, B, F, D)
    det1 = calculate_det(A, E, C, F)
    return (det0 / det, det1 / det)

  @staticmethod
  def plane_plane_intersection(first_plane, second_plane):
    """Return an intersection of two planes or None."""
    l = (first_plane.B * second_plane.C -
         first_plane.C * second_plane.B)
    m = (first_plane.C * second_plane.A -
         first_plane.A * second_plane.C)
    n = (first_plane.A * second_plane.B -
         first_plane.B * second_plane.A)
    directing_vector = Vector3D(l, m, n)

    roots0 = GeometryUtils.__cramer_solve((first_plane.B, first_plane.C,
                                           second_plane.B, second_plane.C,
                                           -first_plane.D, -second_plane.D))
    roots1 = GeometryUtils.__cramer_solve((first_plane.A, first_plane.C,
                                           second_plane.A, second_plane.C,
                                           -first_plane.D, -second_plane.D))
    roots2 = GeometryUtils.__cramer_solve((first_plane.A, first_plane.B,
                                           second_plane.A, second_plane.B,
                                           -first_plane.D, -second_plane.D))
    if roots0 is not None:
      point = Point3D(0, roots0[0], roots0[1])
    elif roots1 is not None:
      point = Point3D(roots1[0], 0, roots1[1])
    elif roots2 is not None:
      point = Point3D(roots2[0], roots2[1], 0)
    else:
      return None
    return Line3D(point, directing_vector)

  @staticmethod
  def plane_segment_intersection(plane, segment):
    """Return an intersection of plane and segment or None."""
    intersection = GeometryUtils.plane_line_intersection(plane, segment.line)
    if intersection is not None and segment.is_contain_point(intersection):
      return intersection
    return None

  @staticmethod
  def plane_line_intersection(plane, line):
    """Return an intersection of plane and line or None."""
    t_denominator = plane.A * line.l + plane.B * line.m + plane.C * line.n
    if t_denominator == 0:
      return None
    dx0 = plane.x0 - line.x0
    dy0 = plane.y0 - line.y0
    dz0 = plane.z0 - line.z0
    t_numerator = dx0 * plane.A + dy0 * plane.B + dz0 * plane.C
    t = t_numerator / t_denominator
    return Point3D(line.l * t + line.x0,
                   line.m * t + line.y0,
                   line.n * t + line.z0)

  @staticmethod
  def distance(first_entity, second_entity):
    """Return an distance between two entities (points)."""
    if isinstance(first_entity, Point3D) and isinstance(second_entity, Point3D):
      return GeometryUtils.point_point_distance(first_entity, second_entity)
    raise ValueError("It's not supported yet")

  @staticmethod
  def point_point_distance(first_point, second_point):
    """Return an distance between two points."""
    delta = second_point - first_point
    return (delta.x ** 2 + delta.y ** 2 + delta.z ** 2).sqrt()

  @staticmethod
  def angle_between(first_entity, second_entity):
    """Return an angle between two entities (vectors)."""
    if isinstance(first_entity, Vector3D) and isinstance(second_entity, Vector3D):
      return GeometryUtils.vector_vector_angle(first_entity,
                                               second_entity)
    raise ValueError("It's not supported yet")

  @staticmethod
  def dot_product(first_vector, second_vector):
    """Return dot product of two vectors."""
    return (first_vector.x * second_vector.x +
            first_vector.y * second_vector.y +
            first_vector.z * second_vector.z)

  @staticmethod
  def cross_product(first_vector, second_vector):
    """Return cross product of two vectors."""
    x = (first_vector.y * second_vector.z - first_vector.z * second_vector.y)
    y = (first_vector.z * second_vector.x - first_vector.x * second_vector.z)
    z = (first_vector.x * second_vector.y - first_vector.y * second_vector.x)
    return Vector3D(x, y, z)

  @staticmethod
  def vector_vector_angle(first_vector, second_vector):
    """Return an distance between two (vectors)."""
    normal = Vector3D(NORMAL_VECTOR)
    dot_product = GeometryUtils.dot_product(first_vector, second_vector)
    cross_product = GeometryUtils.cross_product(first_vector, second_vector)
    mixed_product = GeometryUtils.dot_product(normal, cross_product)
    return math.atan2(mixed_product, dot_product)

  @staticmethod
  def points_are_equal(first_point, second_point, eps=0.01):
    """Check that the first point is the same as the second point."""
    return (abs(first_point.x - second_point.x) < eps and
            abs(first_point.y - second_point.y) < eps and
            abs(first_point.z - second_point.z) < eps)
