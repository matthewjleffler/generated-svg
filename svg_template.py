from lib import *
from lib_path import *
from lib_text import *
from math import *


class TemplateRunner(Runner):
  def __init__(self) -> None:
    super().__init__("template")

  def loop(self):
    draw_border()

    draw_text(200, 200, 5, "Test Text")

  def run(self, test:bool, seed:int, size:SvgSize) -> int:
    mainseed = main(self.dir, "main", test, seed, size, self.loop)
    return mainseed


runner = TemplateRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 1,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

