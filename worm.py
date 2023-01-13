from lib import *

class WormParams:
  def __init__(self) -> None:
    self.padding = 50
    self.stack_count = 50
    self.size_range = RangeInt(5, 100)
    self.stack_spread = 3
    self.fixed_size = 0
    self.max_row = self.max_col = self.worm_size = 0


def _draw_worm_set(params:WormParams):
  for row in range(0, params.max_row):
    origin_y = params.worm_size * row * 1.5

    for col in range(0, params.max_col):
      max_size = params.size_range.rand()
      origin_x = params.worm_size * col

      # Debug bounds
      # draw_rect(svg_safe().x + origin_x, svg_safe().y + origin_y, params.worm_size, params.worm_size)

      for i in range(0, params.stack_count + 1):
        percent = i / params.stack_count
        pi_percent = percent * pi
        pi_half_percent = percent * pi * .25

        size = sin(pi_percent) * max_size
        if params.fixed_size != 0:
          size = min(params.fixed_size, size)

        half = size / 2

        x = svg_safe().x + origin_x + sin(pi_half_percent) * params.stack_spread * i
        y = svg_safe().y + origin_y + cos(pi_half_percent) * params.stack_spread * i

        draw_circ(x, y, half)

def draw_worm(params:WormParams):
  params.worm_size = params.stack_count * params.stack_spread * .75
  worm_row_size = params.worm_size * 1.55

  pad_x = svg_safe().w - params.padding
  pad_y = svg_safe().h - params.padding

  params.max_col = floor(pad_x / params.worm_size)
  params.max_row = floor(pad_y / worm_row_size)

  offset_x = (svg_safe().w - (params.max_col * params.worm_size)) / 2
  offset_y = (svg_safe().h - (params.max_row * worm_row_size)) / 2

  open_group("transform=\"translate({},{})\"".format(offset_x, offset_y))
  _draw_worm_set(params)
  close_group()
  open_group("transform=\"translate({},{}) scale(-1,1)\""
    .format(svg_full().w - offset_x + params.worm_size * .1, offset_y + params.worm_size * .75))
  _draw_worm_set(params)
  close_group()