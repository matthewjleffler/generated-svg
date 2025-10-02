from lib import *
from PIL import Image
import alphashape

###
### Photo Parsing
###


class PhotoParams(
  TypedDict,
):
  draw: bool
  debug_draw_boundary: bool
  debug_draw_points: bool

def CreateParams(defaults: Defaults) -> 'PhotoParams':
  result: PhotoParams = {
    'draw': True,
    'debug_draw_boundary': True,
    'debug_draw_points': False,
  }
  return apply_defaults(result, defaults)

# TODOML lib
# def _get_clip_line(
#     p0:Point,
#     p1:Point,
#     clip:shapely.geometry.Polygon,
#     group: Group
# ) -> List[List[Point]]:
#   # extra: List[Point] = []
#   # result: List[List[Point]] = []
#   line = [p0, p1]

#   return poly_intersect(p0, p1, clip)

  # for poly in clip:
  #   intersection =
  #   print(intersection)

  #   line = intersection[0]
  #   for i in range(1, len(intersection)):
  #     extra.append(intersection[i])
  #   if len(line) < 1:
  #     break

  # if len(line) > 0:
  #   result.append(line)
  #   draw_point_path(line, group)
  # for ext in extra:
  #   extra_lines = _get_clip_line(ext[0], ext[1], clip, group)
  #   if len(extra_lines) > 0:
  #     for extra_line in extra_lines:
  #       result.append(extra_line)

  # return result

# def _draw_clip_path(path: List[Point], clip:List[shapely.geometry.Polygon], group: Group):
#   for i in range(0, len(path) - 1):
#     _draw_clip_line(path[i], path[i + 1], clip, group)


def draw_photo(params: PhotoParams, group: Group, seed: int):
  reload_libs(globals())

  pad = svg_safe().copy()

  # Draw safety border and page border
  if params['debug_draw_boundary']:
    draw_border(group)

  delta = 0.03 #TODOML how much?
  threshold = 0.4 # Beyond this range, don't bother drawing the shape
  draw_step_min = 1
  draw_step_max = 5
  clamp_value = 100
  min_bounds_size = 5 # Don't draw shapes that are less than this many pixels on a side

  # TODOML image path?
  # Find all the pixel darknesses
  width = 0
  height = 0
  pixel_values: dict[tuple[int, int], float] = dict()
  with Image.open('./photo/unnamed.jpg') as im:
    (width, height) = im.size
    for y in range(0, height):
      for x in range(0, width):
        (r, g, b) = im.getpixel((x, y))
        avg = (((r + g + b) / 3) / 255)
        pixel_values[(x, y)] = avg

  neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
  (offset, scale) = scale_rect_to_fit(Rect(0, 0, width, height), pad)

  # Sort pixels into groups
  sort_groups: List[List[Position]] = []
  for y in range(0, height):
    for x in range(0, width):
      start_key = (x, y)
      if not start_key in pixel_values:
        continue
      cur_avg = pixel_values[start_key]
      clamped_avg = floor(cur_avg * clamp_value) / clamp_value

      if clamped_avg >= 1 - threshold:
        # Don't include, too bright
        continue

      cur_group: List[Position] = []
      sort_groups.append(cur_group)

      edges: List[Point] = [Point(x, y)]
      while len(edges) > 0:
        next = edges.pop()
        next_key = (int(next.x), int(next.y))
        if not next_key in pixel_values:
          continue

        next_avg = pixel_values[next_key]

        cur_delta = abs(next_avg - cur_avg)
        if cur_delta > delta:
          # Not in group
          continue

        # In group, append and delete from points
        cur_group.append(Position(offset.x + next.x * scale, offset.y + next.y * scale, clamped_avg))
        pixel_values.pop(next_key)

        for (o_x, o_y) in neighbors:
          n_x = int(next.x + o_x)
          n_y = int(next.y + o_y)
          neighbor_key = (n_x, n_y)
          if not neighbor_key in pixel_values:
            continue

          # This is a valid neighbor, add it to edge
          edges.append(Point(n_x, n_y))


  # Make polygons from each group
  group_len = len(sort_groups)

  all_polygons: List[shapely.Polygon] = []
  polygon_density: List[float] = []
  for i in range(group_len):
    shape = sort_groups[i]
    points: List[tuple[float, float]] = []

    print_overwrite(f"Processing shape {pad_max(i + 1, group_len)}")
    x_min = width + 100
    y_min = height + 100
    x_max = 0
    y_max = 0
    for pos in shape:
      x_min = min(pos.x, x_min)
      y_min = min(pos.y, y_min)
      x_max = max(pos.x, x_max)
      y_max = max(pos.y, y_max)
      points.append((pos.x, pos.y))

    if x_min == x_max or y_min == y_max:
      # Degenerate
      continue

    # alpha = 0.95 * alphashape.optimizealpha(points)
    hull = alphashape.alphashape(points, 0.95)

    if hull.geom_type == 'Polygon':
      hull = shapely.MultiPolygon([hull])

    for polygon in hull.geoms:
      (minx, miny, maxx, maxy) = polygon.bounds
      if maxx - minx < min_bounds_size or maxy - miny < min_bounds_size:
        # Too small to draw
        continue
      all_polygons.append(polygon)
      polygon_density.append(shape[0].size)

  print_finish_overwite()

  all_len = len(all_polygons)
  print(f"Finished processing shapes, found {all_len} polygons")

  # Process polygons
  for i in range(all_len):
    first_polygon = all_polygons[i]
    print_overwrite(f"Finding overlaps {pad_max(i + 1, all_len)}")

    for j in range(all_len):
      second_polygon = all_polygons[j]
      if first_polygon == second_polygon:
        continue

      if first_polygon.contains(second_polygon):
        all_polygons[i] = first_polygon - second_polygon
      elif second_polygon.contains(first_polygon):
        all_polygons[j] = second_polygon - first_polygon

  print_finish_overwite()
  print("Finished finding overlaps")

  # Draw lines
  draw_lines: List[List[Point]] = []
  for i in range(all_len):
    print_overwrite(f"Creating lines {pad_max(i + 1, all_len)}")
    polygon = all_polygons[i]
    density = polygon_density[i]
    (minx, miny, maxx, maxy) = polygon.bounds
    draw_y = 0
    while draw_y <= maxy:
      lines = poly_intersect(Point(minx, draw_y), Point(maxx, draw_y), polygon)
      for line in lines:
        if len(line) < 1:
          continue
        draw_lines.append(line)
      draw_y += draw_step_min + draw_step_max * density

  print_finish_overwite()

  # Sort lines
  draw_lines.sort(key=lambda x: (x[0].y, x[0].x))

  # Draw sorted lines
  for line in draw_lines:
    draw_point_path(line, group)

  print("Finished photo")

