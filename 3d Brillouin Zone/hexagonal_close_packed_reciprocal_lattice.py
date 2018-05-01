#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Hexagonal close packed reciprocal lattice."""

from decimal import Decimal

from geometry import Vector3D
from reciprocal_lattice import ReciprocalLattice


class HexagonalClosePackedReciprocalLattice(ReciprocalLattice):
  """Model of the hexagonal close packed reciprocal lattice."""

  def __init__(self, a, size, center):
    self._a = a
    super().__init__(size, center)

  @property
  def primitive_vectors(self):
    a = Decimal(self._a)
    half_a = Decimal(self._a / 2.)
    c = Decimal(8 / 3.).sqrt() * a
    return (
        Vector3D(a, 0, 0),
        Vector3D(half_a, half_a * Decimal(3).sqrt(), 0),
        Vector3D(0, 0, c)
    )
