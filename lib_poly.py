from lib_math import *
import shapely.geometry
from typing import List

def to_polygon(shell:List[Point], holes:List[List[Point]] = None) -> shapely.geometry.Polygon:
  shell_pos = []
  for point in shell:
    shell_pos.append([point.x, point.y])

  holes_pos = None
  if holes != None:
    holes_pos = []
    for hole_list in holes:
      holes_ind_pos = []
      holes_pos.append(holes_ind_pos)
      for point in hole_list:
        holes_ind_pos.append([point.x, point.y])

  return shapely.geometry.Polygon(shell_pos, holes_pos)

def to_line(p0:Point, p1:Point) -> shapely.geometry.LineString:
  return shapely.geometry.LineString([[p0.x, p0.y], [p1.x, p1.y]])

def poly_diff(p0:Point, p1:Point, poly:shapely.geometry.Polygon) -> List[Point]:
  if poly is None:
    return [p0, p1]
  line = to_line(p0, p1)
  difference = line.difference(poly)
  x, y = difference.xy
  if len(x) <= 0:
    return []
  return [Point(x[0], y[0]), Point(x[1], y[1])]
