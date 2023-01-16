from lib_worm import *


class WormRunner(Runner):
  def __init__(self) -> None:
    super().__init__("worm")

  def loop_combined(self):
    params = WormParams()
    draw_worm(params)
    return params

  def loop_main(self):
    params = WormParams()
    params.draw_innards = False
    draw_worm(params)
    return params

  def loop_innards(self):
    params = WormParams()
    params.draw_worm = False
    draw_worm(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize) -> int:
    mainseed = main(self.dir, "combined", test, seed, size, self.loop_combined)
    main(self.dir, "main", test, mainseed, size, self.loop_main)
    main(self.dir, "innards", test, mainseed, size, self.loop_innards)
    return mainseed


runner = WormRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

