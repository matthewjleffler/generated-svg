from lib import *
from lib_path import *
from math import *
from typing import List


###
### Vertical Wave Drawing
###

class VerticalWaveParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.pad_x: int = 50
    self.pad_y: int = 0
    self.row_range: RangeInt = RangeInt(3, 10)
    self.col_range: RangeInt = RangeInt(5, 10)
    self.wave_range: float = 100
    self.wave_y_range: float = 30
    self.step_size: int = 2
    self.hatch: bool = True
    self.hatch_range_on: RangeInt = RangeInt(5, 25)
    self.hatch_range_off: RangeInt = RangeInt(1, 2)

    super().__init__(defaults)


class _Wave:
  def __init__(self, point:Point, val:float) -> None:
    self.point = point
    self.val = val


def _create_wave_columns(pad_rect:Rect, rows:int, cols:int, params:VerticalWaveParams, group:Group = None) -> List[List[Point]]:
  # Calculate wave points
  col_delta = pad_rect.w / (cols - 1)
  row_delta = pad_rect.h / (rows - 1)

  # Create column points
  result: List[List[Point]] = []
  for col in range(0, cols):
    col_x = pad_rect.x + col_delta * col
    col_list: List[Point] = []
    result.append(col_list)
    for row in range(0, rows):
      col_y = pad_rect.y + row_delta * row
      # Shuffle Y position
      if row != 0 and row != rows - 1:
        col_y += rand_float(-params.wave_y_range, params.wave_y_range)
      col_list.append(Point(col_x, col_y))
    # Debug Draw Points
    # draw_point_circles(col_list, group)
    # draw_point_path(col_list, group)

  return result

def _create_wave_patterns(pad_rect:Rect, rows:int, cols:int, params:VerticalWaveParams, group:Group = None) -> List[List[_Wave]]:
  # Calculate wave points
  col_delta = pad_rect.w / (cols - 1)
  row_delta = pad_rect.h / (rows - 1)

  # Create wave patterns
  result: List[List[_Wave]] = []
  for row in range(0, rows):
    row_y = pad_rect.y + row_delta * row
    wave_list: List[_Wave] = []
    result.append(wave_list)
    for col in range(0, cols):
      x = pad_rect.x + col_delta * col
      val = rand_float(-params.wave_range, params.wave_range)
      wave_list.append(_Wave(Point(x, row_y), val))

  # Normalize start and end rows
  last_start = result[0][0].val
  last_end = result[0][-1].val
  for row in range(1, rows):
    next_start = -last_start
    next_end = -last_end
    result[row][0].val = next_start
    result[row][-1].val = next_end
    last_start = next_start
    last_end = next_end

  # Debug draw wave patterns
  # for row in range(0, len(result)):
  #   wave_list = result[row]
  #   for col in range(0, len(wave_list) - 1):
  #     wave = wave_list[col]
  #     wave_next = wave_list[col + 1]
  #     path = f"M{wave.point.x} {wave.point.y}L{wave_next.point.x} {wave_next.point.y}"
  #     draw_path(path, group)
  #     path = f"M{wave.point.x} {wave.point.y}l{0} {wave.val}L{wave_next.point.x} {wave_next.point.y + wave_next.val}"
  #     draw_path(path, group)

  return result


def draw_wave(params:VerticalWaveParams, group:Group = None):
  # draw_border(group)

  # Create pad rect
  pad_rect = svg_safe().shrink_xy_copy(params.pad_x, params.pad_y)
  # Debug draw pad rect
  # draw_rect(pad_rect.x, pad_rect.y, pad_rect.w, pad_rect.h, group)

  # Create row and column counts
  rows = params.row_range.rand()
  cols = params.col_range.rand()

  # Create Points and Waves
  column_lists = _create_wave_columns(pad_rect, rows, cols, params, group)
  wave_lists = _create_wave_patterns(pad_rect, rows, cols, params, group)

  # Calculate delta between steps
  col_delta = wave_lists[0][1].point.x - wave_lists[0][0].point.x
  col_steps = floor(col_delta / params.step_size)

  # Create Final Points
  total_step = 0
  first_x = wave_lists[0][0].point.x
  final_points: List[List[Point]] = []
  for col in range(0, cols - 1):
    column = column_lists[col]
    column_next = column_lists[col + 1]
    for step in range(0, col_steps):
      # Start Path
      first_wave = wave_lists[0][col]
      x = round(first_x + params.step_size * total_step, 2)
      total_step += 1
      percent = step / (col_steps - 1)

      points: List[Point] = []
      final_points.append(points)
      add_nondup_floats(x, first_wave.point.y, points)

      # Draw Column
      # last_y = column[0].y
      # last_y = lerp(column[0].y, column_next[0].y, percent)
      last_y = ease_in_out_quad(percent, column[0].y, column_next[0].y - column[0].y, 1)
      for row in range(1, rows):
        wave = wave_lists[row][col]
        wave_next = wave_lists[row][col + 1]
        # current_y = lerp(column[row].y, column_next[row].y, percent)
        current_y = ease_in_out_quad(percent, column[row].y, column_next[row].y - column[row].y, 1)

        # Create control
        control_y = last_y + (current_y - last_y) * .5
        # control_x = lerp(wave.val, wave_next.val, percent)
        control_x = ease_in_out_quad(percent, wave.val, wave_next.val - wave.val, 1)

        # Add to path
        add_nondup_floats(x + control_x, control_y, points) # Control
        add_nondup_floats(x, current_y, points) # End point
        last_y = current_y

      # Reverse alternating rows
      if total_step % 2 == 1:
        points.reverse()

  # Draw points
  if params.draw:
    for col in range(0, len(final_points)):
      column = final_points[col]

      if not params.hatch:
        first = column[0]
        path = f"M{first.x} {first.y}"
        for row in range(1, len(column) - 1, 2):
          control = column[row]
          point = column[row + 1]
          path += f"Q{control.x} {control.y} {point.x} {point.y}"
        draw_path(path)
      else:
        hatch_params = HatchParams(params.hatch_range_on, params.hatch_range_off)

        all_points: List[Point] = []
        # Collect all the subdivided curves into a single point array
        p0 = column[0]
        for row in range(1, len(column) - 1, 2):
          control = column[row]
          p1 = column[row + 1]
          subdivide_quadratic(p0, p1, control, 5, all_points)
          p0 = p1

        # draw_point_path(all_points)
        draw_point_path_hatched(all_points, hatch_params, group)



