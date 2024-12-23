from lib_spiral_circle import *


class SpiralCircleRunner(Runner):
  def __init__(self) -> None:
    super().__init__("spiral-circle")

  def loop(self, defaults: Defaults):
    params = SpiralCircleParams(defaults)
    draw_spiral_circle(params)
    return params

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = SpiralCircleRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

