from lib import *


class CircleStackParams:
  def __init__(self) -> None:
    self.draw = True
    self.count = 20
    self.clamp_start = 50
    self.stack_range = RangeInt(35, 35)
    self.min_size = 10
    self.max_size_range = RangeInt(50, 150)

def draw_circle_stack(params:CircleStackParams):
  circles = []

  for _ in range(params.count):
    x = rand_int(svg_safe().x, svg_safe().w)
    y = rand_int(svg_safe().y, svg_safe().h)

    x = round(x / params.clamp_start, 0) * params.clamp_start
    y = round(y / params.clamp_start, 0) * params.clamp_start

    add_nondup_point(x, y, circles)

    # Debug show origins
    # draw_rect(x, y, 10, 10)

  circles.sort()

  for point in circles:
    stack_count = params.stack_range.rand()
    max_size = params.max_size_range.rand()

    for i in range(0, stack_count + 1):
      percent = i / stack_count
      pi_percent = percent * pi

      size = params.min_size + sin(pi_percent) * max_size
      half = size / 2

      x = point.x + 10 * i
      y = point.y + 10 * i
      if not svg_safe().contains(x - half, y - half) or not svg_safe().contains(x + half, y + half):
        continue

      if params.draw:
        draw_circ(x, y, half)


class RectStackParams:
  def __init__(self) -> None:
    self.draw = True
    self.count = 20
    self.stack_count = 15
    self.clamp_start = 10
    self.stack_range = 10
    self.size_range = RangeInt(100, 100)
    self.clamp_size = 10

def draw_rect_stack(params:RectStackParams):
  rects = []

  for _ in range(params.count):
    x = rand_int(0, svg_full().w)
    y = rand_int(0, svg_full().h)

    x = round(x / params.clamp_start, 0) * params.clamp_start
    y = round(y / params.clamp_start, 0) * params.clamp_start

    for i in range(0, params.stack_count + 1):
      add_nondup_point(x + i * params.stack_range, y + i * params.stack_range, rects)

  rects.sort()

  for point in rects:
    size = params.size_range.rand()
    size = round(size / params.clamp_size, 0) * params.clamp_size
    half = size / 2

    x = point.x - half
    y = point.y - half

    if not svg_safe().contains(x, y) or not svg_safe().contains(x + size, y + size):
      continue

    if params.draw:
      draw_rect(x, y, size, size)