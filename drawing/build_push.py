from lib import *
from perlin_noise import PerlinNoise


class PushSettings(TypedDict):
  strength: float
  start_rotation: RangeFloat
  strength_octave: float
  rotation_octave: float
  perlin_range: float


class PushOptions(TypedDict):
  debug_draw_boundary: bool
  do_push: bool
  push_settings: List[PushSettings]


def push_line(line: List[Point], options: PushOptions, seed: int, group: Group):
  push_lines([line], options, seed, group)

def push_lines(lines: List[List[Point]], options: PushOptions, seed: int, group: Group):
  reload_libs(globals())

  # Count total points just once, they're going to move not change
  total_points = 0
  for line in lines:
    total_points += len(line)

  push_settings = options.get('push_settings', [])
  len_pushers = len(push_settings)
  for i in range(0, len_pushers):
    pusher = push_settings[i]
    perlin_range = pusher.get('perlin_range', 0.7)
    perlin_delta = perlin_range * 2
    start_rotation = pusher.get('start_rotation', RangeFloat(0, 360)).rand()

    if not options.get('do_push', True):
      continue

    noise_strength = PerlinNoise(pusher.get('strength_octave', 1), seed + i)
    noise_rotation = PerlinNoise(pusher.get('rotation_octave', 1), seed + i)

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
        sample_strength = (sample_strength + perlin_range) / perlin_delta
        sample_rotation = noise_rotation((norm_x, norm_y))
        sample_rotation = (sample_rotation + perlin_range) / perlin_delta

        push_amount = sample_strength * pusher.get('strength', 50)
        angle_change = sample_rotation * 180
        point.add(Point(1, 0).rotate(start_rotation + angle_change * deg_to_rad).multiply(push_amount))

