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

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "main", test, seed, size, self.loop)


runner = TemplateRunner()

if __name__ == "__main__":
  runner.run(
    test = True,
    seed = 1,
    size = SvgSize.Size9x12
  )

