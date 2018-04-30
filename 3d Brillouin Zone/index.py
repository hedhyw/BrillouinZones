#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  index.py
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

"""Start application point."""

import itertools

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # This is implicitly used
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from base_centered_reciprocal_lattice import BaseCenteredReciprocalLattice
from body_centered_reciprocal_lattice import BodyCenteredReciprocalLattice
from face_centered_reciprocal_lattice import FaceCenteredReciprocalLattice
from geometry import GeometryUtils, Plane, Point3D, Segment3D, Vector3D
from hexagonal_close_packed_reciprocal_lattice import \
    HexagonalClosePackedReciprocalLattice
from primitive_reciprocal_lattice import PrimitiveReciprocalLattice

WIDTH = 0.05 # lattice period
LATTICE_SIZE = 3 # count of atoms in one direction
MIN_ZONES_COUNT = 2 # consider minimum N zones
CENTER = Point3D(0, 0, 0)

def __get_bragg_planes(zone_points):
  """Return the Bragg planes."""
  for points in zone_points:
    middle_points = map(lambda point: point * 0.5, points)
    for middle_point in middle_points:
      yield Plane(middle_point, Vector3D(tuple(middle_point)))

def get_intersections(planes):
  """Return lines that are intersections of the Bragg planes."""
  first_it = iter(planes)
  try:
    while True:
      first_plane = next(first_it)
      first_it, second_it = itertools.tee(first_it)
      for second_plane in  second_it:
        intersection = GeometryUtils.intersection(first_plane, second_plane)
        if intersection is not None:
          yield intersection
  except StopIteration:
    pass

def __get_intersection_points(intersection_lines, bragg_planes):
  """Return all intersections of lines and planes."""
  for line in intersection_lines:
    for plane in bragg_planes:
      intersection = GeometryUtils.intersection(line, plane)
      if intersection is None:
        continue
      yield (intersection, plane)

def __get_zone_points(start_point, intersection_points, bragg_planes):
  """Return points of area that is limited by the Bragg planes."""
  zone_points_by_plane = {}
  for point, point_in_plane in intersection_points:
    segment = Segment3D(start_point, point)
    is_intersected = False
    for plane in bragg_planes:
      intersection = GeometryUtils.intersection(plane, segment)
      if (intersection is None or
          GeometryUtils.points_are_equal(intersection, segment.first_point) or
          GeometryUtils.points_are_equal(intersection, segment.second_point)):
        continue
      is_intersected = True
      break
    if not is_intersected:
      if point_in_plane in zone_points_by_plane:
        zone_points_by_plane[point_in_plane].add(point)
      else:
        zone_points_by_plane[point_in_plane] = set([point])
  return zone_points_by_plane

def __find_average_center(points, interations=3):
  """Return average center of all points"""
  new_points = []
  for _ in range(interations):
    first_it = iter(points)
    try:
      while True:
        first_point = next(first_it)
        first_it, second_it = itertools.tee(first_it)
        for second_point in second_it:
          new_points.append(Segment3D(first_point, second_point).center)
    except StopIteration:
      points = new_points
      new_points = []
  return points[0]

def __sort_vertices(points):
  """Return vertices that are sorted by average center of all points."""
  points = list(set(points))
  if len(points) < 3:
    return None
  start_point = __find_average_center(points)
  start_vector = Vector3D.by_points(start_point, points[0])
  return sorted(points, key=lambda point:
                GeometryUtils.angle_between(
                    start_vector,
                    Vector3D.by_points(start_point, point)))

def __get_reciprocal_lattice():
  """Return tuple(reciprocal lattice, zones-count) by the read of user input."""
  print("""
Select lattice:
  1. Body-centered
  2. Face-centered
  3. Primitive
  4. Hexagonal close–packed
  5. Base-centered
  0. Exit
  """)
  while True:
    print("Input the number:")
    lattice_number = input()
    if lattice_number == "1":
      return (BodyCenteredReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
              max(MIN_ZONES_COUNT, 2))
    elif lattice_number == "2":
      return (FaceCenteredReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
              max(MIN_ZONES_COUNT, 2))
    elif lattice_number == "3":
      return (PrimitiveReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
              max(MIN_ZONES_COUNT, 2))
    elif lattice_number == "4":
      return (HexagonalClosePackedReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
              max(MIN_ZONES_COUNT, 3))
    elif lattice_number == "5":
      return (BaseCenteredReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
              max(MIN_ZONES_COUNT, 2))
    elif lattice_number == "0":
      return (None, MIN_ZONES_COUNT)
    else:
      print("Invalid number, try again")
      continue
    break

def main():
  lattice, zones_count = __get_reciprocal_lattice()
  if lattice is None:
    return 0

  zone_points = list(lattice.points())[1:zones_count+1]
  print("Crystal is generated.")

  # Draw atoms in the reciprocal space
  fig = plt.figure(figsize=(6, 5.3))
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(float(CENTER.x), float(CENTER.y), float(CENTER.z), c='b', marker='o')
  for nearest_points in zone_points:
    for point in nearest_points:
      ax.scatter(float(point.x), float(point.y), float(point.z), c='b', marker='o')

  bragg_planes = list(__get_bragg_planes(zone_points))
  intersection_lines = list(get_intersections(bragg_planes))
  print("Intersection lines are calculated")

  intersection_points = list(__get_intersection_points(intersection_lines,
                                                       bragg_planes))
  print("Intersection points are calculated")

  zone_points = __get_zone_points(CENTER, intersection_points, bragg_planes)
  print("Zone points are calculated")

  # Draw polygons of the first zone
  for points in zone_points.values():
    points = __sort_vertices(points)
    if points is None:
      continue
    verts = [(float(point.x), float(point.y), float(point.z)) for point in points]
    col = Poly3DCollection([verts], linewidths=1, alpha=0.8)
    col.set_facecolor([0.5, 0.5, 1])
    col.set_edgecolor('k')
    ax.add_collection3d(col)

  # Show plot
  str_dimension = '{0}*a'.format(1.0 / WIDTH)
  ax.set_xlabel('X, ' + str_dimension)
  ax.set_ylabel('Y, ' + str_dimension)
  ax.set_zlabel('Z, ' + str_dimension)
  plt.show()

  main()
  return 0

if __name__ == '__main__':
  import sys
  sys.exit(main())
