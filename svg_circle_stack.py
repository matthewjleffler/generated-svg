from lib_stack import *


class CircleStackRunner(Runner):
  def __init__(self) -> None:
    super().__init__("circle-stack")

  def loop(self):
    params = CircleStackParams()
    draw_circle_stack(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "main", test, seed, size, self.loop)


runner = CircleStackRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

