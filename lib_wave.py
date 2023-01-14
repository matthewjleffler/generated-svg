from lib import *
from lib_path import *
from math import *
from typing import List


###
### Vertical Wave Drawing
###

# TODO smooth out the columns

class VerticalWaveParams:
  def __init__(self) -> None:
    self.draw: bool = True
    self.pad_x: int = 50
    self.pad_y: int = 0
    self.vert_subdivisions: RangeInt = RangeInt(3, 10)
    self.wave_subdivisions: RangeInt = RangeInt(5, 10)
    self.wave_range: float = 100
    self.step_size: int = 5


class _Wave:
  def __init__(self, point:Point, val:float) -> None:
    self.point = point
    self.val = val


def draw_wave(params:VerticalWaveParams, group:Group = None):
  # draw_border(group)

  # Create pad rect
  pad_rect = svg_safe().shrink_xy_copy(params.pad_x, params.pad_y)
  # Debug draw pad rect
  # draw_rect(pad_rect.x, pad_rect.y, pad_rect.w, pad_rect.h, group)

  # Create rough line
  vertical_rough: List[Point] = []
  add_nondup_point(pad_rect.x, pad_rect.y, vertical_rough)
  add_nondup_point(pad_rect.x, pad_rect.bottom(), vertical_rough)
  # Debug draw rough line
  # draw_point_circles(rough, group)

  # Subdivide line
  vertical_sub = subdivide_point_path(vertical_rough, params.vert_subdivisions)
  # Debug draw subdivided line
  # draw_point_circles(sub, group)
  rows = len(vertical_sub)

  # Create wave points
  wave_rough: List[Point] = []
  add_nondup_point(pad_rect.x, pad_rect.y, wave_rough)
  add_nondup_point(pad_rect.right(), pad_rect.y, wave_rough)
  wave_sub = subdivide_point_path(wave_rough, params.wave_subdivisions)
  cols = len(wave_sub)

  # Create wave patterns
  wave_lists: List[List[_Wave]] = []
  for row in range(0, rows):
    row = vertical_sub[row].y
    wave_list: List[_Wave] = []
    wave_lists.append(wave_list)
    for col in range(0, cols): # Extra row for final lerp
      x = wave_sub[col].x
      val = rand_float(-params.wave_range, params.wave_range)
      wave_list.append(_Wave(Point(x, row), val))

  # Normalize start and end rows
  last_start = wave_lists[0][0].val
  last_end = wave_lists[0][-1].val
  for row in range(1, rows):
    next_start = -last_start
    next_end = -last_end
    wave_lists[row][0].val = next_start
    wave_lists[row][-1].val = next_end
    last_start = next_start
    last_end = next_end

  # Debug draw wave patterns
  # for row in range(0, len(wave_lists)):
  #   wave_list = wave_lists[row]
  #   for col in range(0, len(wave_list) - 1):
  #     wave = wave_list[col]
  #     wave_next = wave_list[col + 1]
  #     path = f"M{wave.point.x} {wave.point.y}L{wave_next.point.x} {wave_next.point.y}"
  #     draw_path(path, group)
  #     path = f"M{wave.point.x} {wave.point.y}l{0} {wave.val}L{wave_next.point.x} {wave_next.point.y + wave_next.val}"
  #     draw_path(path, group)

  col_delta = wave_lists[0][1].point.x - wave_lists[0][0].point.x
  col_steps = floor(col_delta / params.step_size)
  # step_size = col_delta / col_steps # Round out step size to remove gaps

  # Draw Wave Patterns
  total_step = 0
  first_x = wave_lists[0][0].point.x
  for col in range(0, cols - 1):
    for step in range(0, col_steps):
      # Start Path
      first_wave = wave_lists[0][col]
      x = round(first_x + params.step_size * total_step, 2)
      total_step += 1
      percent = step / (col_steps - 1)

      path = f"M{x} {first_wave.point.y}"

      # TODO flip alternating lines reverse
      # Draw Column
      last_vert = vertical_sub[0]
      for row in range(1, rows):
        wave = wave_lists[row][col]
        wave_next = wave_lists[row][col + 1]
        vert = vertical_sub[row]

        # Create control
        control = vert.subtract_copy(last_vert)
        delta = control.length() * .5
        control.normalize()
        control.multiply(delta)
        # control.x = lerp(wave.val, wave_next.val, percent)
        control.x = ease_in_out_quad(percent, wave.val, wave_next.val - wave.val, 1)

        # Draw
        path += f"Q{round(x + control.x, 2)} {last_vert.y + control.y} {x} {vert.y}"
        last_vert = vert
      draw_path(path, group)

