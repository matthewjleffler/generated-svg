from impl_exploded_room import *


class ExplodedRoomRunner(Runner):
  def __init__(self) -> None:
    super().__init__("exploded-room")

  def loop_main(self, defaults: Defaults, group: Group, seed: int):
    params = ExplodedRoomParams(defaults)
    draw_exploded_room(params, group)
    return params

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop_main)
    return mainseed


runner = ExplodedRoomRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

