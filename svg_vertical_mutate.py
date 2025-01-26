from lib import *
import impl.impl_vertical_lines as impl


class VerticalMutateRunner(Runner):
  def __init__(self) -> None:
    super().__init__("vertical-mutate")

  def loop_main(self, defaults: Defaults, group: Group, seed: int):
    params = impl.VerticalLineParams(defaults)
    params.mutate = True
    params.draw_highlights = False
    impl.draw_lines(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop_main)
    return mainseed


runner = VerticalMutateRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

