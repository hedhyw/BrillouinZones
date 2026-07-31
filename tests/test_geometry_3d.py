"""Tests for the 3D geometry primitives."""

import math
from decimal import Decimal

from geometry import GeometryUtils, Line3D, Plane, Point3D, Segment3D, Vector3D


def test_point_arithmetic():
  point = Point3D(1, 2, 3) + Point3D(4, 5, 6)
  assert tuple(point) == (5, 7, 9)
  point = Point3D(1, 2, 3) - (1, 1, 1)
  assert tuple(point) == (0, 1, 2)
  point = Point3D(1, 2, 3) * 2
  assert tuple(point) == (2, 4, 6)


def test_point_equality_and_hash():
  assert Point3D(1, 2, 3) == Point3D(1, 2, 3)
  assert hash(Point3D(1, 2, 3)) == hash(Point3D(1, 2, 3))
  assert Point3D(1, 2, 3) != (1, 2, 3)


def test_distance():
  assert GeometryUtils.distance(Point3D(0, 0, 0), Point3D(3, 4, 0)) == 5
  assert GeometryUtils.distance(Point3D(1, 1, 1), Point3D(1, 1, 1)) == 0


def test_dot_and_cross_product():
  x_axis = Vector3D(1, 0, 0)
  y_axis = Vector3D(0, 1, 0)
  assert GeometryUtils.dot_product(x_axis, y_axis) == 0
  assert tuple(GeometryUtils.cross_product(x_axis, y_axis)) == (0, 0, 1)
  assert GeometryUtils.dot_product(Vector3D(1, 2, 3), Vector3D(4, 5, 6)) == 32


def test_vector_module_and_normalized():
  vector = Vector3D(3, 4, 0)
  assert vector.module == 5
  assert abs(vector.normalized.module - 1) < Decimal("1e-9")


def test_angle_between_orthogonal_vectors():
  angle = GeometryUtils.angle_between(Vector3D(1, 0, 0), Vector3D(0, 1, 0))
  assert math.isclose(abs(angle), math.pi / 2)


def test_segment_center_and_length():
  segment = Segment3D(Point3D(0, 0, 0), Point3D(2, 2, 2))
  assert tuple(segment.center) == (1, 1, 1)
  assert math.isclose(float(segment.length), math.sqrt(12))
  assert segment.is_contain_point(Point3D(1, 1, 1))
  assert not segment.is_contain_point(Point3D(5, 5, 5))


def test_plane_line_intersection():
  # Plane z = 1 and the z axis intersect at (0, 0, 1).
  plane = Plane(Point3D(0, 0, 1), Vector3D(0, 0, 1))
  line = Line3D(Point3D(0, 0, 0), Vector3D(0, 0, 1))
  intersection = GeometryUtils.intersection(plane, line)
  assert tuple(intersection) == (0, 0, 1)


def test_plane_line_no_intersection():
  # Plane z = 1 and a parallel line in the plane z = 0.
  plane = Plane(Point3D(0, 0, 1), Vector3D(0, 0, 1))
  line = Line3D(Point3D(0, 0, 0), Vector3D(1, 0, 0))
  assert GeometryUtils.intersection(plane, line) is None


def test_plane_plane_intersection():
  # Planes x = 0 and y = 0 intersect in the z axis.
  first = Plane(Point3D(0, 0, 0), Vector3D(1, 0, 0))
  second = Plane(Point3D(0, 0, 0), Vector3D(0, 1, 0))
  line = GeometryUtils.intersection(first, second)
  assert line is not None
  assert (line.l, line.m) == (0, 0)
  assert abs(line.n) == 1
  assert (line.x0, line.y0) == (0, 0)


def test_parallel_planes_do_not_intersect():
  first = Plane(Point3D(0, 0, 0), Vector3D(0, 0, 1))
  second = Plane(Point3D(0, 0, 1), Vector3D(0, 0, 1))
  assert GeometryUtils.intersection(first, second) is None


def test_points_are_equal():
  assert GeometryUtils.points_are_equal(Point3D(0, 0, 0),
                                        Point3D(0.001, 0.001, 0.001))
  assert not GeometryUtils.points_are_equal(Point3D(0, 0, 0),
                                            Point3D(1, 0, 0))
