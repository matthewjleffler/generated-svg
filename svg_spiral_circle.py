from lib_spiral_circle import *


class SpiralCircleRunner(Runner):
  def __init__(self) -> None:
    super().__init__("spiral-circle")

  def loop(self):
    params = SpiralCircleParams()
    draw_spiral_circle(params)
    return params

  def run(self, test:bool, seed:int, size:tuple[int, int]) -> int:
    mainseed = main(self.dir, "main", test, seed, size, self.loop)
    return mainseed


runner = SpiralCircleRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

