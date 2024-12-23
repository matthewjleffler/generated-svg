from lib_triangle import *

class TriangleRunner(Runner):
  def __init__(self) -> None:
    super().__init__("triangle")

  def loop(self, defaults: Defaults):
    params = TriangleParams(defaults)
    draw_triangle(params)
    return params

  def run(self, defaults: Defaults) -> int:
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

