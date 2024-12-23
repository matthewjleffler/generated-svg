from lib_worm import *


class SpiralWormRunner(Runner):
  def __init__(self) -> None:
    super().__init__("spiral-worm")

  def loop_combined(self, defaults: Defaults):
    params = SprialWormParams(defaults)
    draw_spiral_worm(params)
    return params

  def loop_main(self, defaults: Defaults):
    params = SprialWormParams(defaults)
    params.draw_highlight = False
    params.draw_highlight2 = False
    draw_spiral_worm(params)
    return params

  def loop_circle(self, defaults: Defaults):
    params = SprialWormParams(defaults)
    params.draw_worm = False
    params.draw_highlight2 = False
    draw_spiral_worm(params)
    return params

  def loop_lines(self, defaults: Defaults):
    params = SprialWormParams(defaults)
    params.draw_worm = False
    params.draw_highlight = False
    draw_spiral_worm(params)
    return params

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "combined", defaults, defaults.seed, self.loop_combined)
    main(self.dir, "main", defaults, mainseed, self.loop_main)
    main(self.dir, "circle", defaults, mainseed, self.loop_circle)
    main(self.dir, "lines", defaults, mainseed, self.loop_lines)
    return mainseed


runner = SpiralWormRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

