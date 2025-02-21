from lib import *
import impl.impl_worm as impl


class LongWormRunner(Runner):
  def __init__(self) -> None:
    super().__init__("long-worm")

  def loop_combined(self, defaults: Defaults, group: Group, seed: int):
    params = impl.LongWormParams.create(defaults)
    impl.draw_long_worm(params, group)
    return params

  def loop_main(self, defaults: Defaults, group: Group, seed: int):
    params = impl.LongWormParams.create(defaults)
    params['draw_highlight'] = False
    impl.draw_long_worm(params, group)
    return params

  def loop_highlight(self, defaults: Defaults, group: Group, seed: int):
    params = impl.LongWormParams.create(defaults)
    params['draw_worm'] = False
    impl.draw_long_worm(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "combined", defaults, defaults.seed, self.loop_combined)
    main(self.dir, "main", defaults, mainseed, self.loop_main)
    main(self.dir, "highlight", defaults, mainseed, self.loop_highlight)
    return mainseed


runner = LongWormRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

