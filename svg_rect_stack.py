from lib_stack import *


class RectStackRunner(Runner):
  def __init__(self) -> None:
    super().__init__("rect-stack")

  def loop(self, defaults: Defaults):
    params = RectStackParams(defaults)
    draw_rect_stack(params)
    return params

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = RectStackRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

