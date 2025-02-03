from lib import *
import impl.impl_radial_circle as impl


class RadialCirclesRunner(Runner):
  def __init__(self) -> None:
    super().__init__("radial-circles")

  def loop_combined(self, defaults: Defaults, group: Group, seed: int):
    params = impl.RadialParams.create(defaults)
    impl.draw_radial_circles(params, group)
    return params

  def loop_main(self, defaults: Defaults, group: Group, seed: int):
    params = impl.RadialParams.create(defaults)
    params['draw_border'] = False
    impl.draw_radial_circles(params, group)
    return params

  def loop_highlights(self, defaults: Defaults, group: Group, seed: int):
    params = impl.RadialParams.create(defaults)
    params['draw_circles'] = False
    impl.draw_radial_circles(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "combined", defaults, defaults.seed, self.loop_combined)
    main(self.dir, "main", defaults, mainseed, self.loop_main)
    main(self.dir, "highlights", defaults, mainseed, self.loop_highlights)
    return mainseed


runner = RadialCirclesRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

