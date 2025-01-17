from lib import *
from lib_path import *
from lib_text import *
from math import *


class TemplateRunner(Runner):
  def __init__(self) -> None:
    super().__init__("template")

  def loop(self, defaults: Defaults, group: Group):
    draw_border(group)

    draw_text(200, 200, 5, "Test Text")

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = TemplateRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 1,
    size = (9, 12)
  )
  runner.run(defaults)

