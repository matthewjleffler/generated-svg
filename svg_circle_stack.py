from lib import *
import impl.impl_stack as impl


class CircleStackRunner(Runner):
  def __init__(self) -> None:
    super().__init__("circle-stack")

  def loop(self, defaults: Defaults, group: Group, seed: int):
    params = impl.CircleStackParams.create(defaults)
    impl.draw_circle_stack(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = CircleStackRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

