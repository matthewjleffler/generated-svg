from lib import *
import drawing.build_maze as build_maze
from perlin_noise import PerlinNoise


class PushType(ReloadEnum):
  Random = 0
  Maze = 1
  Perlin = 2


# A 'type definition'
class PushOptions:
  debug_draw_boundary: bool
  do_push: bool
  push_type: PushType
  push_pad_range_max: float
  push_pad_range_offset: float
  push_num: RangeInt
  push_line_cell_size: RangeFloat
  push_line_step_size: float
  push_range: RangeFloat
  push_strength: RangeFloat
  perlin_cell_size: float
  perlin_octave: float


class _Pusher:
  def __init__(self, origin: Point, range: float, strength: float):
    self.origin = origin
    self.range = range
    self.strength = strength

  def apply_params(self, params: PushOptions) -> '_Pusher':
    self.range = try_get(params, 'push_range', RangeFloat(400, 800)).rand()
    self.strength = try_get(params, 'push_strength', RangeFloat(0.5, 2.5)).rand()
    return self


def push_line(line: List[Point], rect: Rect, params: PushOptions, seed: int, group: Group) -> Rect:
  return push_lines([line], rect, params, seed, group)

def push_lines(lines: List[List[Point]], rect: Rect, params: PushOptions, seed: int, group: Group) -> Rect:
  reload_libs(globals())

  debug_draw_boundary = try_get(params, 'debug_draw_boundary', False)
  push_type = try_get(params, 'push_type', PushType.Random)
  do_push = try_get(params, 'do_push', True)
  push_pad_range_max = try_get(params, 'push_pad_range_max', 0)

  if do_push:
    print(push_type)

  # Do push randomization independent of draw
  pushers: List[_Pusher] = []
  pad_x = rect.w * push_pad_range_max
  pad_y = rect.h * push_pad_range_max
  push_pad_x = RangeFloat(-pad_x, 0)
  push_pad_y = RangeFloat(-pad_y, 0)
  push_rect = rect.shrink_xy_copy(push_pad_x.rand(), push_pad_y.rand())

  if push_type == PushType.Random:
    num_pushers = params.push_num.rand()
    for _ in range(0, num_pushers):
      origin = Point(RangeFloat(push_rect.x, push_rect.right()).rand(), RangeFloat(push_rect.y, push_rect.bottom()).rand())
      pushers.append(_Pusher(origin, 0, 0).apply_params(params))
      if debug_draw_boundary:
        draw_circ_point(origin, 5, group)

  if push_type == PushType.Maze:
    push_cell = try_get(params, 'push_line_cell_size', RangeFloat(100, 200)).rand()
    push_size = build_maze.MazeSize(push_cell, push_rect)
    push_options = build_maze.MazeOptions()
    push_options.close_path = True
    push_options.do_inset = False
    push_line = build_maze.make_maze_line(push_size, push_options)
    push_center = generate_centerpoints(push_line)
    push_divisions = generate_final_points(push_line, push_center, params.push_line_step_size)

    # Draw debug
    # new_group = open_group(GroupSettings(stroke=GroupColor.red), group)
    # draw_point_circles(push_divisions, new_group)
    # close_group()

    for point in push_divisions:
      pushers.append(_Pusher(point, 0, 0).apply_params(params))

  if push_type == PushType.Perlin:
    perlin_cell_size = try_get(params, 'perlin_cell_size', 20)
    push_x = floor(push_rect.w / perlin_cell_size)
    push_w = push_rect.w / push_x
    push_y = floor(push_rect.h / perlin_cell_size)
    push_h = push_rect.h / push_y
    perlin_octave = try_get(params, 'perlin_octave', 3)

    noise = PerlinNoise(perlin_octave, seed)
    samples: List[float] = []
    min_sample = maxsize
    max_sample = -maxsize
    sample_w = push_y + 1
    for x in range(0, push_x + 1):
      for y in range(0, push_y + 1):
        p_x = x / push_x
        p_y = y / push_y
        sample = noise((p_x, p_y))
        samples.append(sample)
        min_sample = min(sample, min_sample)
        max_sample = max(sample, max_sample)

    sample_delta = max_sample - min_sample
    #TODOML these hard coded values are referenced twice
    push_range = try_get(params, 'push_range', RangeFloat(400, 800)).rand()
    push_strength = try_get(params, 'push_strength', RangeFloat(0.5, 2.5)).rand()
    for x in range(0, push_x + 1):
      for y in range(0, push_y + 1):
        sample = (-min_sample + samples[x * sample_w + y]) / sample_delta
        point = Point(push_rect.x + x * push_w, push_rect.y + y * push_h)
        pushers.append(_Pusher(point, push_range, push_strength * sample))
        # draw_circ(
        #   push_rect.x + x * push_w,
        #   push_rect.y + y * push_h,
        #   5 * sample, group)

  # Draw push
  if do_push:
    push_index = 0
    print_overwrite('Pushing...')
    for push in pushers:
      push_index += 1
      print_overwrite(f"Running push {pad_max(push_index, len(pushers))} ...")
      for line in lines:
        for point in line:
          delta = point.subtract_copy(push.origin)
          delta_len = delta.length()
          if delta_len > push.range:
            continue
          t = 1 - (delta_len / push.range)
          push_amount = ease_in_out_quad(t, 0, push.strength, 1)
          point.add(delta.normalize().multiply(push_amount))
    print_finish_overwite()

  return push_rect
