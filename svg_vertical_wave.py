from lib import *
import impl.impl_wave as impl


class VerticalWaveRunner(Runner):
  def __init__(self) -> None:
    super().__init__("vertical-wave")

  def loop_main(self, defaults: Defaults, group: Group, seed: int):
    params = impl.VerticalWaveParams.create(defaults)
    impl.draw_wave(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop_main)
    return mainseed


runner = VerticalWaveRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

