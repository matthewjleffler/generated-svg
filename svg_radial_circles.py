from lib_radial_circle import *


class RadialCirclesRunner(Runner):
  def __init__(self) -> None:
    super().__init__("radial-circles")

  def loop_combined(self):
    params = RadialParams()
    draw_radial_circles(params)
    return params

  def loop_main(self):
    params = RadialParams()
    params.draw_border = False
    draw_radial_circles(params)
    return params

  def loop_highlights(self):
    params = RadialParams()
    params.draw_circles = False
    draw_radial_circles(params)
    return params

  def run(self, test:bool, seed:int, size:SvgSize):
    mainseed = main(self.dir, "combined", test, seed, size, self.loop_combined)
    main(self.dir, "main", test, mainseed, size, self.loop_main)
    main(self.dir, "highlights", test, mainseed, size, self.loop_highlights)


runner = RadialCirclesRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = SvgSize.Size9x12
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

