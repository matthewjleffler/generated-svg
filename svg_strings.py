from lib_strings import *


class StringsRunner(Runner):
  def __init__(self) -> None:
    super().__init__("strings")

  def loop(self):
    params = StringParams()
    draw_strings(params)
    return params

  def run(self, test:bool, seed:int, size:tuple[int, int]) -> int:
   mainseed = main(self.dir, "main", test, seed, size, self.loop)
   return mainseed


runner = StringsRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

