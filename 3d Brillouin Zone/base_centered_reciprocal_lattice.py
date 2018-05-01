#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Base-centered reciprocal lattice."""

from decimal import Decimal

from geometry import Vector3D
from reciprocal_lattice import ReciprocalLattice


class BaseCenteredReciprocalLattice(ReciprocalLattice):
  """Model of the base-centered reciprocal lattice."""

  def __init__(self, a, size, center):
    self._a = a
    super().__init__(size, center)

  @property
  def primitive_vectors(self):
    a = Decimal(self._a)
    half_a = Decimal(self._a / 2.)
    return (
        Vector3D(+half_a, +half_a, 0),
        Vector3D(+half_a, -half_a, 0),
        Vector3D(0, 0, a),
    )
