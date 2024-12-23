from lib_vertical_lines import *


class VerticalMutateRunner(Runner):
  def __init__(self) -> None:
    super().__init__("vertical-mutate")

  def loop_main(self, defaults: Defaults):
    params = VerticalLineParams(defaults)
    params.mutate = True
    params.draw_highlights = False
    draw_lines(params)
    return params

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop_main)
    return mainseed


runner = VerticalMutateRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

