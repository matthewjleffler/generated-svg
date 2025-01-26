from lib import *
import impl.impl_snake as impl


class SnakeRunner(Runner):
  def __init__(self) -> None:
    super().__init__("snake")

  def loop_main(self, defaults: Defaults, group: Group, seed: int):
    params = impl.SnakeParams(defaults)
    impl.draw_snake(params, group, seed)
    return params

  def loop_spine(self, defaults: Defaults, group: Group, seed: int):
    params = impl.SnakeParams(defaults)
    params.draw_ribs = False
    impl.draw_snake(params, group, seed)
    return params

  def loop_ribs(self, defaults: Defaults, group: Group, seed: int):
    params = impl.SnakeParams(defaults)
    params.draw_spine = False
    impl.draw_snake(params, group, seed)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop_main)
    if not defaults.test:
      main(self.dir, "spine", defaults, mainseed, self.loop_spine)
      main(self.dir, "ribs", defaults, mainseed, self.loop_ribs)
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

