from lib_triangle import *

class TriangleRunner(Runner):
  def __init__(self) -> None:
    super().__init__("triangle")

  def loop(self):
    params = TriangleParams()
    draw_triangle(params)
    return params

  def run(self, test:bool, seed:int, size:tuple[int, int]) -> int:
    mainseed = main(self.dir, "main", test, seed, size, self.loop)

    return mainseed


runner = TriangleRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

