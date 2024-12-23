from impl_wave import *


class VerticalWaveRunner(Runner):
  def __init__(self) -> None:
    super().__init__("vertical-wave")

  def loop_main(self, defaults: Defaults):
    params = VerticalWaveParams(defaults)
    draw_wave(params)
    return params

  def run(self, defaults: Defaults) -> int:
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

