#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Primitive reciprocal lattice."""

from geometry import Vector3D
from reciprocal_lattice import ReciprocalLattice


class PrimitiveReciprocalLattice(ReciprocalLattice):
  """Model of the primitive reciprocal lattice."""

  def __init__(self, a, size, center):
    self._a = a
    super().__init__(size, center)

  @property
  def primitive_vectors(self):
    half_a = self._a / 2.0
    return (
        Vector3D(half_a, 0, 0),
        Vector3D(0, half_a, 0),
        Vector3D(0, 0, half_a)
    )
