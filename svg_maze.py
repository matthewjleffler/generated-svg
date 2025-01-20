from impl_maze import *


class MazeRunner(Runner):
  def __init__(self) -> None:
    super().__init__("maze")

  def loop_main(self, defaults: Defaults, group: Group):
    params = MazeParams(defaults)
    draw_maze(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop_main)
    return mainseed


runner = MazeRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

