from lib_snake import *


class SnakeRunner(Runner):
  def __init__(self) -> None:
    super().__init__("snake")

  def loop_main(self):
    params = SnakeParams()
    draw_snake(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize) -> int:
    mainseed = main(self.dir, "main", test, seed, size, self.loop_main)
    return mainseed


runner = SnakeRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

