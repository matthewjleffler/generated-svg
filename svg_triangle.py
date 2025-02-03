from lib import *
import impl.impl_triangle as impl


class TriangleRunner(Runner):
  def __init__(self) -> None:
    super().__init__("triangle")

  def loop(self, defaults: Defaults, group: Group, seed: int):
    params = impl.TriangleParams.create(defaults)
    impl.draw_triangle(params, seed, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = TriangleRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

