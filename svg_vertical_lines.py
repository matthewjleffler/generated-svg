from lib_vertical_lines import *


class VerticalLineRunner(Runner):
  def __init__(self) -> None:
    super().__init__("vertical-lines")

  def loop_combined(self):
    params = VerticalLineParams()
    draw_lines(params)
    return params

  def loop_main(self):
    params = VerticalLineParams()
    params.draw_highlights = False
    draw_lines(params)
    return params

  def loop_highlight(self):
    params = VerticalLineParams()
    params.draw_lines = False
    draw_lines(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "combined", test, seed, size, self.loop_combined)
    main(self.dir, "main", test, mainseed, size, self.loop_main)
    main(self.dir, "highlight", test, mainseed, size, self.loop_highlight)


runner = VerticalLineRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

