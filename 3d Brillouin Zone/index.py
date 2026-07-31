#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Start application point."""

import itertools
import os
import sys

import matplotlib
import matplotlib.pyplot as plt
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
IMAGE_FILE_NAME = os.environ.get("BRILLOUIN_OUTPUT", "brillouin_zone_3d.png")

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

def get_reciprocal_lattice_by_number(lattice_number):
  """Return tuple(reciprocal lattice, zones-count) by the lattice number
     or None if the number is invalid; ("0", zones-count) means exit."""
  if lattice_number == "1":
    return (BodyCenteredReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
            max(MIN_ZONES_COUNT, 2))
  if lattice_number == "2":
    return (FaceCenteredReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
            max(MIN_ZONES_COUNT, 2))
  if lattice_number == "3":
    return (PrimitiveReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
            max(MIN_ZONES_COUNT, 2))
  if lattice_number == "4":
    return (HexagonalClosePackedReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
            max(MIN_ZONES_COUNT, 3))
  if lattice_number == "5":
    return (BaseCenteredReciprocalLattice(WIDTH, LATTICE_SIZE, CENTER),
            max(MIN_ZONES_COUNT, 2))
  if lattice_number == "0":
    return (None, MIN_ZONES_COUNT)
  return None

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
    result = get_reciprocal_lattice_by_number(input())
    if result is None:
      print("Invalid number, try again")
      continue
    return result

def is_interactive_backend():
  """Return True if the matplotlib backend can open a window."""
  return matplotlib.get_backend().lower() not in ("agg", "pdf", "ps", "svg",
                                                  "cairo", "template")

def render(lattice, zones_count):
  """Construct the first Brillouin zone of the lattice and draw it."""
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
  if is_interactive_backend():
    plt.show()
  else:
    fig.savefig(IMAGE_FILE_NAME)
    print("Figure is saved to " + IMAGE_FILE_NAME)
  plt.close(fig)

def main(argv=None):
  """Run the drawer: non-interactive if a lattice number is given as an
     argument, otherwise prompt for lattice numbers in a loop."""
  argv = sys.argv[1:] if argv is None else argv
  if argv:
    result = get_reciprocal_lattice_by_number(argv[0])
    if result is None or result[0] is None:
      print("Usage: index.py [lattice-number 1..5]")
      return 2
    render(*result)
    return 0
  while True:
    lattice, zones_count = __get_reciprocal_lattice()
    if lattice is None:
      return 0
    render(lattice, zones_count)

if __name__ == '__main__':
  sys.exit(main())
