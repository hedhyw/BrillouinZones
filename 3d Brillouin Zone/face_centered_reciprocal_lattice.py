#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Face-centered reciprocal lattice."""

from geometry import Vector3D
from reciprocal_lattice import ReciprocalLattice


class FaceCenteredReciprocalLattice(ReciprocalLattice):
  """Model of the face-centered reciprocal lattice."""

  def __init__(self, a, size, center):
    self._a = a
    super().__init__(size, center)

  @property
  def primitive_vectors(self):
    half_a = self._a / 2.0
    return (
        Vector3D(half_a, half_a, 0),
        Vector3D(0, half_a, half_a),
        Vector3D(half_a, 0, half_a)
    )
