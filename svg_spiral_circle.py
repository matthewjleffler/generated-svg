from lib_spiral_circle import *


class SpiralCircleRunner(Runner):
  def __init__(self) -> None:
    super().__init__("spiral-circle")

  def loop(self):
    params = SpiralCircleParams()
    draw_spiral_circle(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "main", test, seed, size, self.loop)


runner = SpiralCircleRunner()

if __name__ == "__main__":
  runner.run(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )

