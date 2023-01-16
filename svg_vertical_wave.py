from lib_wave import *


class VerticalWaveRunner(Runner):
  def __init__(self) -> None:
    super().__init__("vertical-wave")

  def loop_main(self):
    params = VerticalWaveParams()
    draw_wave(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "main", test, seed, size, self.loop_main)


runner = VerticalWaveRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

