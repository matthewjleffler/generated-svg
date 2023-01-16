from lib_checkerboard import *


class CheckerboardRunner(Runner):
  def __init__(self) -> None:
    super().__init__("checkerboard")

  def loop(self):
    params = CheckerboardParams()
    draw_checkerboard(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "main", test, seed, size, self.loop)


runner = CheckerboardRunner()

if __name__ == "__main__":
  runner.run(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )

