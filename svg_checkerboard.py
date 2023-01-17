from lib_checkerboard import *


class CheckerboardRunner(Runner):
  def __init__(self) -> None:
    super().__init__("checkerboard")

  def loop_combined(self):
    params = CheckerboardParams()
    draw_checkerboard(params)
    return params

  def loop_main(self):
    params = CheckerboardParams()
    params.draw_lines = True
    params.draw_aligned_vertical = False
    params.draw_aligned_horizontal = False
    params.draw_filled_checkers = False
    draw_checkerboard(params)
    return params

  def loop_vert(self):
    params = CheckerboardParams()
    params.draw_lines = False
    params.draw_aligned_vertical = True
    params.draw_aligned_horizontal = False
    params.draw_filled_checkers = False
    draw_checkerboard(params)
    return params

  def loop_horiz(self):
    params = CheckerboardParams()
    params.draw_lines = False
    params.draw_aligned_vertical = False
    params.draw_aligned_horizontal = True
    params.draw_filled_checkers = False
    draw_checkerboard(params)
    return params

  def loop_fill(self):
    params = CheckerboardParams()
    params.draw_lines = False
    params.draw_aligned_vertical = False
    params.draw_aligned_horizontal = False
    params.draw_filled_checkers = True
    draw_checkerboard(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize) -> int:
    mainseed = main(self.dir, "combined", test, seed, size, self.loop_combined)
    main(self.dir, "main", test, mainseed, size, self.loop_main)
    main(self.dir, "vert", test, mainseed, size, self.loop_vert)
    main(self.dir, "horiz", test, mainseed, size, self.loop_horiz)
    main(self.dir, "fill", test, mainseed, size, self.loop_fill)
    return mainseed


runner = CheckerboardRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

