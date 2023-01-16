from lib_vertical_lines import *


class VerticalMutateRunner(Runner):
  def __init__(self) -> None:
    super().__init__("vertical-mutate")

  def loop_main(self):
    params = VerticalLineParams()
    params.mutate = True
    params.draw_highlights = False
    draw_lines(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "main", test, seed, size, self.loop_main)


runner = VerticalMutateRunner()

if __name__ == "__main__":
  runner.run(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )

