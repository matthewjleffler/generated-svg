from lib import *
import impl_worm as impl


class WormRunner(Runner):
  def __init__(self) -> None:
    super().__init__("worm")

  def loop_combined(self, defaults: Defaults, group: Group, seed: int):
    params = impl.WormParams(defaults)
    impl.draw_worm(params, group)
    return params

  def loop_main(self, defaults: Defaults, group: Group, seed: int):
    params = impl.WormParams(defaults)
    params.draw_innards = False
    impl.draw_worm(params, group)
    return params

  def loop_innards(self, defaults: Defaults, group: Group, seed: int):
    params = impl.WormParams(defaults)
    params.draw_worm = False
    impl.draw_worm(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "combined", defaults, defaults.seed, self.loop_combined)
    main(self.dir, "main", defaults, mainseed, self.loop_main)
    main(self.dir, "innards", defaults, mainseed, self.loop_innards)
    return mainseed


runner = WormRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

