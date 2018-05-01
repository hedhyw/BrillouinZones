#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main file for Brillouin Zone Drawer"""

import itertools

from PIL import Image, ImageDraw

#from hex_crystal import HexCrystal
#from parallelogram_crystal import ParallelogramCrystal
from primitive_crystal import PrimitiveCrystal
from sympy.geometry import Line, Point, Point2D, Segment

IMAGE_FILE_NAME = "/tmp/brillouin_zone.png"
IMAGE_SIZE = (720, 720)
WIDTH = 160 # px, lattice period
IMAGE_CENTER = (0.5 * IMAGE_SIZE[0], 0.5 * IMAGE_SIZE[1])
CENTER = Point(0, 0)
ZONES_COUNT = 12
CRYSTAL_RANGE = 4 # (4+4) x (4+4)
ATOM_COLOR = "black"
ATOM_RADIUS = 3 # px
LINE_STRETCH = 1000
LINE_COLOR = "black"
RADIUS_EXPLORER = 2 # distance out the border
ZERO_EPS_EXPLORER = 1e-4
COLORS = itertools.cycle([(0xef, 0x9a, 0x9a, 0xff),
                          (0xce, 0x93, 0xd8, 0xff),
                          (0x9f, 0xa8, 0xda, 0xff),
                          (0x81, 0xd4, 0xfa, 0xff),
                          (0x80, 0xcb, 0xc4, 0xff),
                          (0xc5, 0xe1, 0xa5, 0xff),
                          (0xff, 0xf5, 0x9d, 0xff),
                          (0x8F, 0xF4, 0xEE, 0xFF),
                          (0xb0, 0xbe, 0xc5, 0xFF),
                          (0x90, 0xCA, 0xF9, 0xFF)])

def flat_intersections(vals):
  """ Return 1d list from 1d list """

  for val in itertools.chain.from_iterable(vals):
    if isinstance(val, Point2D):
      #if val.x == 20: print(val)
      yield val

def get_bragg_plane_lines(zone_points):
  """ Return bragg plane boundaries
  Bragg plane is a plane in reciprocal space
  which bisects a reciprocal lattice vector"""

  for points in zone_points:
    middle_points = map(lambda point: point * 0.5, points)
    perpendicular_lines = []
    for middle_point in middle_points:
      line = Line(CENTER, middle_point).perpendicular_line(middle_point)
      vec = line.p2 - line.p1
      perpendicular_lines.append(Line(line.points[0] - vec * LINE_STRETCH,
                                      line.points[0] + vec * LINE_STRETCH))
    yield from perpendicular_lines

def get_area_points(image, start_point, points_map):
  """ Return points of area """

  points_to_explore = [tuple(start_point + IMAGE_CENTER)]
  points = set()
  while points_to_explore:
    point = points_to_explore.pop()
    pos_x = round(point[0])
    pos_y = round(point[1])
    try:
      if points_map[pos_y][pos_x] is not None and points_map[pos_y][pos_x] != 0:
        points.add(points_map[pos_y][pos_x])
      red, green, blue = image.getpixel((pos_x, pos_y))[:3]
    except IndexError:
      continue
    if (red, green, blue) == (0, 0, 0):
      continue
    points_map[pos_y][pos_x] = 0 # The point is processed
    if pos_x == 0 or pos_y == 0 \
        or pos_x == IMAGE_SIZE[0] \
        or pos_y == IMAGE_SIZE[1]:
      continue
    if points_map[pos_y - 1][pos_x] != 0:
      points_to_explore.append((pos_x, pos_y - 1))
    if points_map[pos_y + 1][pos_x] != 0:
      points_to_explore.append((pos_x, pos_y + 1))
    if points_map[pos_y][pos_x - 1] != 0:
      points_to_explore.append((pos_x - 1, pos_y))
    if points_map[pos_y][pos_x + 1] != 0:
      points_to_explore.append((pos_x + 1, pos_y))
  return points

def explore_next(image, point, points_map):
  """ Explore nearest zones """

  area_points = list(get_area_points(image, point, points_map))
  for points_pair in itertools.combinations(area_points, 2):
    segment = Segment(points_pair[0], points_pair[1])
    if segment.length == 0: # is the same point
      continue
    mid = segment.midpoint
    p_line = segment.perpendicular_line(mid)
    vec = p_line.p2 - p_line.p1
    if abs(vec.x) < ZERO_EPS_EXPLORER:
      yield mid + (0, RADIUS_EXPLORER * vec.y / abs(vec.y))
      yield mid - (0, RADIUS_EXPLORER * vec.y / abs(vec.y))
    elif abs(vec.y) < ZERO_EPS_EXPLORER:
      yield mid + (RADIUS_EXPLORER * vec.x / abs(vec.x), 0)
      yield mid - (RADIUS_EXPLORER * vec.x / abs(vec.x), 0)
    else:
      yield mid + (vec.x / abs(vec.x), RADIUS_EXPLORER * vec.y / abs(vec.y))
      yield mid - (vec.x / abs(vec.x), RADIUS_EXPLORER * vec.y / abs(vec.y))
    # angle = segment.angle_between(Line(CENTER, Point(0, 10)))
    # angle += math.pi/3.0
    # yield mid + (RADIUS * math.cos(angle), RADIUS * math.sin(angle))
    # yield mid - (RADIUS * math.cos(angle), RADIUS * math.sin(angle))

def explore(image, start_point, points_map):
  """ Start zone exploring """
  exploring_points = explore_next(image,
                                  start_point,
                                  points_map)
  exploring_points = list(set(exploring_points))
  zone = 1
  while zone <= ZONES_COUNT:
    print("Exploring zone #:" + str(zone))
    points_to_explore = []
    color = next(COLORS)
    for point in exploring_points:
      coords = (int(point.x + IMAGE_CENTER[0]), int(point.y + IMAGE_CENTER[1]))
      try:
        red, green, blue = image.getpixel(coords)[:3]
      except IndexError:
        continue
      if (red, green, blue) == (0xFF, )*3:
        ImageDraw.floodfill(image, coords, color)
        points_to_explore.append(point)
    print(str(len(points_to_explore)) + " points to explore")
    exploring_points = []
    for point in points_to_explore:
      exploring_points += explore_next(image, point, points_map)
    zone += 1

def main():
  """ Generate Brillouin zones for crystal """

  image = Image.new('RGBA', IMAGE_SIZE, (255, 255, 255, 255))

  ### CRYSTAL INITIALIZATION ###
  #crystal = ParallelogramCrystal(WIDTH, CRYSTAL_RANGE, CENTER)
  crystal = PrimitiveCrystal(WIDTH, CRYSTAL_RANGE, CENTER)
  #crystal = HexCrystal(WIDTH, CRYSTAL_RANGE, CENTER)
  zone_points = list(crystal.points())[1:ZONES_COUNT+2] # first is center
  #zone_points.reverse()
  print("Crystal is generated.")

  ### BRAGG PLANES ###
  bragg_plane_lines = list(get_bragg_plane_lines(zone_points))
  print("Bragg planes are constructed.")

  ### INTERSECTIONS ###
  line_combinations = itertools.permutations(bragg_plane_lines, 2)
  intersections = map(lambda line_pair:
                      line_pair[0].intersection(line_pair[1]),
                      line_combinations)
  intersection_points = list(set(flat_intersections(intersections)))
  points_map = [[None for x in range(IMAGE_SIZE[0] + 1)]
                for y in range(IMAGE_SIZE[1] + 1)]
  for intersection in intersection_points:
    point_x = int(intersection.x + IMAGE_CENTER[0])
    point_y = int(intersection.y + IMAGE_CENTER[1])
    for pos_y in range(point_y - 5, point_y + 5):
      if pos_y > IMAGE_SIZE[1] or pos_y < 0: break
      for pos_x in range(point_x - 5, point_x + 5):
        if pos_x > IMAGE_SIZE[0] or pos_x < 0: break
        points_map[pos_y][pos_x] = Point(round(intersection.x), round(intersection.y))
  print("Intersections are calculated.")

  ### DRAWING ###
  # lines
  draw = ImageDraw.Draw(image)
  for line in bragg_plane_lines:
    draw.line(
        tuple((line.points[0] + IMAGE_CENTER)) +
        tuple((line.points[1] + IMAGE_CENTER)),
        fill=LINE_COLOR)
  print("Lines are drawn.")

  # zone highlighting
  ImageDraw.floodfill(image, IMAGE_CENTER, next(COLORS))
  explore(image, CENTER, points_map)
  print('Zones are highlighted.')

  # draw atoms
  draw.ellipse(
      [(IMAGE_CENTER[0] - ATOM_RADIUS, IMAGE_CENTER[1] - ATOM_RADIUS),
       (IMAGE_CENTER[0] + ATOM_RADIUS, IMAGE_CENTER[1] + ATOM_RADIUS)],
      fill=ATOM_COLOR)
  for points in zone_points:
    for point in points:
      draw.ellipse(
          [tuple(point - (ATOM_RADIUS,)*2 + IMAGE_CENTER),
           tuple(point + (ATOM_RADIUS,)*2 + IMAGE_CENTER)],
          fill=ATOM_COLOR)
  print('Atoms are allocated on plot.')

  del draw
  image.save(IMAGE_FILE_NAME)
  image.show()

  return 0

if __name__ == '__main__':
  import sys
  sys.exit(main())
