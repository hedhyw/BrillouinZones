"""Tests for the 3D reciprocal lattice models."""

import math
from decimal import Decimal

from body_centered_reciprocal_lattice import BodyCenteredReciprocalLattice
from face_centered_reciprocal_lattice import FaceCenteredReciprocalLattice
from geometry import GeometryUtils, Point3D
from primitive_reciprocal_lattice import PrimitiveReciprocalLattice

WIDTH = 0.05
CENTER = Point3D(0, 0, 0)


def shell_sizes(lattice, count):
  shells = list(lattice.points())[:count]
  return [len(shell) for shell in shells]


def test_primitive_reciprocal_vectors_are_orthogonal():
  lattice = PrimitiveReciprocalLattice(WIDTH, 2, CENTER)
  first, second, third = lattice.reciprocal_primitive_vectors
  assert GeometryUtils.dot_product(first, second) == 0
  assert GeometryUtils.dot_product(second, third) == 0
  assert GeometryUtils.dot_product(first, third) == 0


def test_primitive_reciprocal_vector_magnitude():
  # The reciprocal of a simple cubic lattice with period a/2
  # has |b| = 2 * pi / (a / 2).
  lattice = PrimitiveReciprocalLattice(WIDTH, 2, CENTER)
  expected = 2 * math.pi / (WIDTH / 2)
  for vector in lattice.reciprocal_primitive_vectors:
    assert math.isclose(float(vector.module), expected)


def test_primitive_reciprocal_shells():
  # Simple cubic coordination: the center, 6 nearest, 12 next-nearest.
  lattice = PrimitiveReciprocalLattice(WIDTH, 2, CENTER)
  assert shell_sizes(lattice, 3) == [1, 6, 12]


def test_body_centered_reciprocal_shells():
  # The reciprocal of a BCC lattice is FCC: 12 nearest neighbours.
  lattice = BodyCenteredReciprocalLattice(WIDTH, 2, CENTER)
  assert shell_sizes(lattice, 2) == [1, 12]


def test_face_centered_reciprocal_shells():
  # The reciprocal of an FCC lattice is BCC: 8 nearest, 6 next-nearest.
  lattice = FaceCenteredReciprocalLattice(WIDTH, 3, CENTER)
  assert shell_sizes(lattice, 3) == [1, 8, 6]


def test_lattice_is_deterministic():
  first = list(PrimitiveReciprocalLattice(WIDTH, 2, CENTER).points())
  second = list(PrimitiveReciprocalLattice(WIDTH, 2, CENTER).points())
  assert first == second


def test_lattice_points_are_finite():
  lattice = PrimitiveReciprocalLattice(WIDTH, 2, CENTER)
  for shell in lattice.points():
    for point in shell:
      for coord in point:
        assert isinstance(coord, Decimal)
        assert coord.is_finite()


def test_shells_are_equidistant_and_sorted():
  lattice = PrimitiveReciprocalLattice(WIDTH, 2, CENTER)
  previous = Decimal(-1)
  for shell in lattice.points():
    distances = [GeometryUtils.distance(CENTER, point) for point in shell]
    assert max(distances) - min(distances) < Decimal("0.01")
    assert min(distances) > previous
    previous = max(distances)
