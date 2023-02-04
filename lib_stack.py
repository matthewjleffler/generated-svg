from lib import *


###
### Stack Drawing
###


# Circle Stack Drawing

class CircleStackParams:
  def __init__(self) -> None:
    self.draw = True
    self.count: int = 20
    self.clamp_start: int = 50
    self.stack_count: RangeInt = RangeInt(35, 35)
    self.fixed_size: int = 0
    self.min_size: int = 10
    self.max_size_range: RangeInt = RangeInt(50, 150)

def draw_circle_stack(params:CircleStackParams, group:Group = None):
  # draw_border(group)

  circles = []
  x_range = RangeInt(svg_safe().x, svg_safe().right())
  y_range = RangeInt(svg_safe().y, svg_safe().bottom())

  for _ in range(params.count):
    x = clamp_value(x_range.rand(), params.clamp_start)
    y = clamp_value(y_range.rand(), params.clamp_start)

    add_nondup_floats(x, y, circles)

    # Debug show origins
    # draw_rect(x, y, 10, 10, group)

  circles.sort()

  for point in circles:
    stack_count = params.stack_count.rand()
    max_size = params.max_size_range.rand()

    for i in range(0, stack_count + 1):
      percent = i / stack_count
      pi_percent = percent * pi

      size = params.min_size + sin(pi_percent) * max_size
      if params.fixed_size > 0:
        size = params.fixed_size
      half = size / 2

      x = point.x + 10 * i
      y = point.y + 10 * i
      if not svg_safe().contains(x - half, y - half) or not svg_safe().contains(x + half, y + half):
        continue

      if params.draw:
        draw_circ(x, y, half, group)


# Rectangle Stack Drawing

class RectStackParams:
  def __init__(self) -> None:
    self.draw = True
    self.count = 20
    self.stack_count = 15
    self.clamp_start = 10
    self.stack_range = 10
    self.size_range = RangeInt(100, 100)
    self.clamp_size = 10

def draw_rect_stack(params:RectStackParams, group:Group = None):
  # draw_border(group)

  rects = []

  x_range = RangeInt(0, svg_full().right())
  y_range = RangeInt(0, svg_full().bottom())

  for _ in range(params.count):
    x = clamp_value(x_range.rand(), params.clamp_start)
    y = clamp_value(y_range.rand(), params.clamp_start)

    for i in range(0, params.stack_count + 1):
      add_nondup_floats(x + i * params.stack_range, y + i * params.stack_range, rects)

  rects.sort()

  for point in rects:
    size = clamp_value(params.size_range.rand(), params.clamp_size)
    half = size / 2

    x = point.x - half
    y = point.y - half

    if not svg_safe().contains(x, y) or not svg_safe().contains(x + size, y + size):
      continue

    if params.draw:
      draw_rect(x, y, size, size, group)

