from lib_worm import *


class SpiralWormRunner(Runner):
  def __init__(self) -> None:
    super().__init__("spiral-worm")

  def loop_combined(self):
    params = SprialWormParams()
    draw_spiral_worm(params)
    return params

  def loop_main(self):
    params = SprialWormParams()
    params.draw_highlight = False
    params.draw_highlight2 = False
    draw_spiral_worm(params)
    return params

  def loop_circle(self):
    params = SprialWormParams()
    params.draw_worm = False
    params.draw_highlight2 = False
    draw_spiral_worm(params)
    return params

  def loop_lines(self):
    params = SprialWormParams()
    params.draw_worm = False
    params.draw_highlight = False
    draw_spiral_worm(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "combined", test, seed, size, self.loop_combined)
    main(self.dir, "main", test, mainseed, size, self.loop_main)
    main(self.dir, "circle", test, mainseed, size, self.loop_circle)
    main(self.dir, "lines", test, mainseed, size, self.loop_lines)


runner = SpiralWormRunner()

if __name__ == "__main__":
  runner.run(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )

