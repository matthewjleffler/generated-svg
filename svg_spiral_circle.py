from lib import *
import impl.impl_spiral_circle as impl


class SpiralCircleRunner(Runner):
  def __init__(self) -> None:
    super().__init__("spiral-circle")

  def loop(self, defaults: Defaults, group: Group, seed: int):
    params = impl.SpiralCircleParams(defaults)
    impl.draw_spiral_circle(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = SpiralCircleRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

