from lib import *
from lib_path import *
from lib_text import *
from math import *
from typing import List


class CalibrateRunner(Runner):
  def __init__(self) -> None:
    super().__init__("calibrate")

  def loop(self, defaults: Defaults, group: Group):
    # draw_border(group)

    split = 5
    pad = svg_safe().copy()

    line: List[Point] = []

    half_w = pad.w / 2
    vert_count = floor(half_w / split)
    if vert_count % 2 != 0:
      vert_count -= 1
    vert_space = half_w / vert_count
    for i in range(0, vert_count):
      x = pad.x + i * vert_space
      top = Point(x, pad.y)
      bottom = Point(x, pad.bottom())
      if i % 2 == 0:
        line.append(top)
        line.append(bottom)
      else:
        line.append(bottom)
        line.append(top)

    horiz_count = floor(pad.h / split)
    horiz_space = pad.h / horiz_count
    for i in range(0, horiz_count + 1):
      y = pad.y + i * horiz_space
      left = Point(pad.x + half_w, y)
      right = Point(pad.right(), y)
      if i % 2  == 0:
        line.append(left)
        line.append(right)
      else:
        line.append(right)
        line.append(left)

    draw_point_path(line)


  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = CalibrateRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 1,
    size = (9, 12)
  )
  runner.run(defaults)

