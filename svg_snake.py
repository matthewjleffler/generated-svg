from impl_snake import *


class SnakeRunner(Runner):
  def __init__(self) -> None:
    super().__init__("snake")

  def loop_main(self, defaults: Defaults, group: Group):
    params = SnakeParams(defaults)
    draw_snake(params, group)
    return params

  def loop_spine(self, defaults: Defaults, group: Group):
    params = SnakeParams(defaults)
    params.draw_ribs = False
    draw_snake(params, group)
    return params

  def loop_ribs(self, defaults: Defaults, group: Group):
    params = SnakeParams(defaults)
    params.draw_spine = False
    draw_snake(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop_main)
    # mainseed = main(self.dir, "combined", defaults, self.loop_main)
    # main(self.dir, "spine", defaults, mainseed, self.loop_spine)
    # main(self.dir, "ribs", defaults, mainseed, self.loop_ribs)
    return mainseed


runner = SnakeRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

