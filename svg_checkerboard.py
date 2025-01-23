from impl_checkerboard import *


class CheckerboardRunner(Runner):
  def __init__(self) -> None:
    super().__init__("checkerboard")

  def loop_combined(self, defaults: Defaults, group: Group, seed: int):
    params = CheckerboardParams(defaults)
    draw_checkerboard(params, group)
    return params

  def loop_main(self, defaults: Defaults, group: Group, seed: int):
    params = CheckerboardParams(defaults)
    params.draw_lines = True
    params.draw_aligned_vertical = False
    params.draw_aligned_horizontal = False
    params.draw_filled_checkers = False
    draw_checkerboard(params, group)
    return params

  def loop_vert(self, defaults: Defaults, group: Group, seed: int):
    params = CheckerboardParams(defaults)
    params.draw_lines = False
    params.draw_aligned_vertical = True
    params.draw_aligned_horizontal = False
    params.draw_filled_checkers = False
    draw_checkerboard(params, group)
    return params

  def loop_horiz(self, defaults: Defaults, group: Group, seed: int):
    params = CheckerboardParams(defaults)
    params.draw_lines = False
    params.draw_aligned_vertical = False
    params.draw_aligned_horizontal = True
    params.draw_filled_checkers = False
    draw_checkerboard(params, group)
    return params

  def loop_fill(self, defaults: Defaults, group: Group, seed: int):
    params = CheckerboardParams(defaults)
    params.draw_lines = False
    params.draw_aligned_vertical = False
    params.draw_aligned_horizontal = False
    params.draw_filled_checkers = True
    draw_checkerboard(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "combined", defaults, defaults.seed, self.loop_combined)
    main(self.dir, "main", defaults, mainseed, self.loop_main)
    main(self.dir, "vert", defaults, mainseed, self.loop_vert)
    main(self.dir, "horiz", defaults, mainseed, self.loop_horiz)
    main(self.dir, "fill", defaults, mainseed, self.loop_fill)
    return mainseed


runner = CheckerboardRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

