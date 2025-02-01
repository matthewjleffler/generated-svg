from lib import *
from perlin_noise import PerlinNoise


# A 'type definition'
class PushOptions:
  debug_draw_boundary: bool
  do_push: bool
  push_strength: float
  push_start_rotation: float
  push_strength_octave: float
  push_rotation_octave: float
  push_perlin_max: float


def push_line(line: List[Point], rect: Rect, params: PushOptions, seed: int, group: Group):
  push_lines([line], rect, params, seed, group)

def push_lines(lines: List[List[Point]], rect: Rect, params: PushOptions, seed: int, group: Group):
  reload_libs(globals())

  do_push = try_get(params, 'do_push', True)
  push_strength = try_get(params, 'push_strength', 50)
  push_start_rotation = try_get(params, 'push_start_rotation', RangeFloat(0, 360)).rand()
  push_strength_octave = try_get(params, 'push_strength_octave', 3)
  push_rotation_octave = try_get(params, 'push_rotation_octave', 5)
  perlin_max = try_get(params, 'push_perlin_max', 0.7)

  perlin_delta = perlin_max * 2
  noise_strength = PerlinNoise(push_strength_octave, seed)
  noise_rotation = PerlinNoise(push_rotation_octave, seed)

  if not do_push:
    return

  total_points = 0
  for line in lines:
    total_points += len(line)

  current_point = 0
  push_log = RunningLog("Pushing point", total_points)
  for line in lines:
    for point in line:
      current_point += 1
      push_log.log(current_point)
      norm_x = (point.x - rect.x) / rect.w
      norm_y = (point.y - rect.y) / rect.w
      sample_strength = noise_strength((norm_x, norm_y))
      sample_strength = (sample_strength + perlin_max) / perlin_delta
      sample_rotation = noise_rotation((norm_x, norm_y))
      sample_rotation = (sample_rotation + perlin_max) / perlin_delta

      push_amount = sample_strength * push_strength
      angle_change = sample_rotation * 180
      point.add(Point(1, 0).rotate(push_start_rotation + angle_change * deg_to_rad).multiply(push_amount))

