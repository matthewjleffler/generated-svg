from lib_worm import *


class LongWormRunner(Runner):
  def __init__(self) -> None:
    super().__init__("long-worm")

  def loop_combined(self):
    params = LongWormParams()
    draw_long_worm(params)
    return params

  def loop_main(self):
    params = LongWormParams()
    params.draw_highlight = False
    draw_long_worm(params)
    return params

  def loop_highlight(self):
    params = LongWormParams()
    params.draw_worm = False
    draw_long_worm(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "combined", test, seed, size, self.loop_combined)
    main(self.dir, "main", test, mainseed, size, self.loop_main)
    main(self.dir, "highlight", test, mainseed, size, self.loop_highlight)


runner = LongWormRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

