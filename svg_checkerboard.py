from lib_checkerboard import *


class CheckerboardRunner(Runner):
  def __init__(self) -> None:
    super().__init__("checkerboard")

  def loop(self):
    params = CheckerboardParams()
    draw_checkerboard(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize) -> int:
    mainseed = main(self.dir, "main", test, seed, size, self.loop)
    return mainseed


runner = CheckerboardRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

