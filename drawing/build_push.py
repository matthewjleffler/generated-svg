from lib import *
from perlin_noise import PerlinNoise


class PushSettings:
  strength: float
  start_rotation: RangeFloat
  strength_octave: float
  rotation_octave: float
  perlin_range: float

class PushOptions:
  debug_draw_boundary: bool
  do_push: bool
  push_settings: List[PushSettings]

def __apply_options_defaults(params: PushOptions) -> PushOptions:
  params.do_push = try_get(params, 'do_push', True)
  params.push_settings = try_get(params, 'push_settings', [])
  return params

def __apply_setting_defaults(params: PushSettings) -> PushSettings:
  params.strength = try_get(params, 'strength', 50)
  params.start_rotation = try_get(params, 'start_rotation', RangeFloat(0, 360))
  params.strength_octave = try_get(params, 'strength_octave', 1)
  params.rotation_octave = try_get(params, 'strength_octave', 1)
  params.perlin_range = try_get(params, 'perlin_range', 0.7)
  return params


def push_line(line: List[Point], params: PushOptions, seed: int, group: Group):
  push_lines([line], params, seed, group)

def push_lines(lines: List[List[Point]], params: PushOptions, seed: int, group: Group):
  reload_libs(globals())

  # Count total points just once, they're going to move not change
  total_points = 0
  for line in lines:
    total_points += len(line)

  params = __apply_options_defaults(params)
  len_pushers = len(params.push_settings)
  for i in range(0, len_pushers):
    pusher = params.push_settings[i]
    pusher = __apply_setting_defaults(pusher)
    perlin_delta = pusher.perlin_range * 2
    start_rotation = pusher.start_rotation.rand()

    if not params.do_push:
      continue

    noise_strength = PerlinNoise(pusher.strength_octave, seed + i)
    noise_rotation = PerlinNoise(pusher.rotation_octave, seed + i)

    # Recalculate bounds
    volume = ExpandingVolume()
    volume.add_lists(lines)
    rect = volume.to_rect()
    rect_max = max(rect.w, rect.h)

    # Push points
    current_point = 0
    push_log = RunningLog(f"Push {pad_max(i + 1, len_pushers)} point", total_points)
    for line in lines:
      for point in line:
        current_point += 1
        push_log.log(current_point)
        norm_x = (point.x - rect.x) / rect_max
        norm_y = (point.y - rect.y) / rect_max
        sample_strength = noise_strength((norm_x, norm_y))
        sample_strength = (sample_strength + pusher.perlin_range) / perlin_delta
        sample_rotation = noise_rotation((norm_x, norm_y))
        sample_rotation = (sample_rotation + pusher.perlin_range) / perlin_delta

        push_amount = sample_strength * pusher.strength
        angle_change = sample_rotation * 180
        point.add(Point(1, 0).rotate(start_rotation + angle_change * deg_to_rad).multiply(push_amount))

