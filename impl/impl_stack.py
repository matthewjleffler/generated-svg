from lib import *


###
### Stack Drawing
###


# Circle Stack Drawing

class CircleStackParams(TypedDict):
  draw: bool
  count: int
  clamp_start: int
  stack_count: RangeInt
  fixed_size: int
  min_size: int
  max_size_range: RangeInt

  @classmethod
  def create(cls, defaults: Defaults) -> 'CircleStackParams':
    result: CircleStackParams = {
      'draw': True,
      'count': 20,
      'clamp_start': 50,
      'stack_count': RangeInt(35, 35),
      'fixed_size': 0,
      'min_size': 10,
      'max_size_range': RangeInt(50, 150),
    }
    return apply_defaults(result, defaults)


def draw_circle_stack(params: CircleStackParams, group: Group):
  reload_libs(globals())

  # draw_border(group)

  circles = []
  x_range = RangeInt(svg_safe().x, svg_safe().right())
  y_range = RangeInt(svg_safe().y, svg_safe().bottom())

  count = params['count']
  clamp_start = params['clamp_start']
  for _ in range(count):
    x = clamp_value(x_range.rand(), clamp_start)
    y = clamp_value(y_range.rand(), clamp_start)

    add_nondup_floats(x, y, circles)

    # Debug show origins
    # draw_rect(x, y, 10, 10, group)

  circles.sort()

  stack_count_range = params['stack_count']
  max_size_range = params['max_size_range']
  min_size = params['min_size']
  fixed_size = params['fixed_size']
  for point in circles:
    stack_count = stack_count_range.rand()
    max_size = max_size_range.rand()

    for i in range(0, stack_count + 1):
      percent = i / stack_count
      pi_percent = percent * pi

      size = min_size + sin(pi_percent) * max_size
      if fixed_size > 0:
        size = fixed_size
      half = size / 2

      x = point.x + 10 * i
      y = point.y + 10 * i
      if not svg_safe().contains(x - half, y - half) or not svg_safe().contains(x + half, y + half):
        continue

      if params['draw']:
        draw_circ(x, y, half, group)


# Rectangle Stack Drawing

class RectStackParams(TypedDict):
  draw: bool
  count: int
  stack_count: int
  clamp_start: int
  stack_range: int
  size_range: RangeInt
  clamp_size: int

  @classmethod
  def create(cls, defaults: Defaults) -> 'RectStackParams':
    result: RectStackParams = {
      'draw': True,
      'count': 20,
      'stack_count': 15,
      'clamp_start': 10,
      'stack_range': 10,
      'size_range': RangeInt(100, 100),
      'clamp_size': 10,
    }
    return apply_defaults(result, defaults)


def draw_rect_stack(params: RectStackParams, group: Group):
  reload_libs(globals())

  # draw_border(group)

  rects = []

  x_range = RangeInt(0, svg_full().right())
  y_range = RangeInt(0, svg_full().bottom())

  count = params['count']
  clamp_start = params['clamp_start']
  stack_count = params['stack_count']
  stack_range = params['stack_range']
  size_range = params['size_range']
  clamp_size = params['clamp_size']
  for _ in range(count):
    x = clamp_value(x_range.rand(), clamp_start)
    y = clamp_value(y_range.rand(), clamp_start)

    for i in range(0, stack_count + 1):
      add_nondup_floats(x + i * stack_range, y + i * stack_range, rects)

  rects.sort()

  for point in rects:
    size = clamp_value(size_range.rand(), clamp_size)
    half = size / 2

    x = point.x - half
    y = point.y - half

    if not svg_safe().contains(x, y) or not svg_safe().contains(x + size, y + size):
      continue

    if params['draw']:
      draw_rect(x, y, size, size, group)

