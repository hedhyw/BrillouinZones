"""Tests for the 2D crystal models."""

from sympy.geometry import Point

from hex_crystal import HexCrystal
from parallelogram_crystal import ParallelogramCrystal
from primitive_crystal import PrimitiveCrystal

CENTER = Point(0, 0)


def shell_sizes(crystal):
  return [len(shell) for shell in crystal.points()]


def test_primitive_crystal_shell_sizes():
  # Square lattice with period 1, coordination shells:
  # center, 4 at d=1, 4 at d=sqrt(2), 4 at d=2, 8 at d=sqrt(5).
  assert shell_sizes(PrimitiveCrystal(1, 2, CENTER)) == [1, 4, 4, 4, 8]


def test_primitive_crystal_first_shell_symmetry():
  shells = list(PrimitiveCrystal(1, 2, CENTER).points())
  assert shells[0] == {CENTER}
  first_shell = shells[1]
  assert first_shell == {Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)}
  # 4-fold symmetric: for every point the rotated point is present.
  for point in first_shell:
    assert Point(-point.y, point.x) in first_shell


def test_primitive_crystal_is_deterministic():
  first = list(PrimitiveCrystal(1, 2, CENTER).points())
  second = list(PrimitiveCrystal(1, 2, CENTER).points())
  assert first == second


def test_parallelogram_crystal_one_point_per_translation():
  crystal = ParallelogramCrystal(2, 1, CENTER)
  # (2 * size + 1) ** 2 translations, one atom each.
  assert len(crystal._points) == 9


def test_hex_crystal_six_points_per_translation():
  crystal = HexCrystal(2, 1, CENTER)
  assert len(crystal._points) == 9 * 6


def test_shells_are_sorted_by_distance():
  crystal = PrimitiveCrystal(1, 3, CENTER)
  distances = []
  for shell in crystal.points():
    shell_distances = {point.distance(CENTER) for point in shell}
    assert len(shell_distances) == 1  # all points of a shell are equidistant
    distances.append(shell_distances.pop())
  assert distances == sorted(distances)
