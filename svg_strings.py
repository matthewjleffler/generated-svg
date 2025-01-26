from lib import *
import impl.impl_strings as impl


class StringsRunner(Runner):
  def __init__(self) -> None:
    super().__init__("strings")

  def loop(self, defaults: Defaults, group: Group, seed: int):
    params = impl.StringParams(defaults)
    impl.draw_strings(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = StringsRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

