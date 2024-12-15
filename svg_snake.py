from lib_snake import *


class SnakeRunner(Runner):
  def __init__(self) -> None:
    super().__init__("snake")

  def loop_main(self):
    params = SnakeParams()
    draw_snake(params)
    return params

  def loop_spine(self):
    params = SnakeParams()
    params.draw_ribs = False
    draw_snake(params)
    return params

  def loop_ribs(self):
    params = SnakeParams()
    params.draw_spine = False
    draw_snake(params)
    return params

  def run(self, test:bool, seed:int, size:tuple[int, int]) -> int:
    mainseed = main(self.dir, "main", test, seed, size, self.loop_main)
    # mainseed = main(self.dir, "combined", test, seed, size, self.loop_main)
    # main(self.dir, "spine", test, mainseed, size, self.loop_spine)
    # main(self.dir, "ribs", test, mainseed, size, self.loop_ribs)
    return mainseed


runner = SnakeRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

