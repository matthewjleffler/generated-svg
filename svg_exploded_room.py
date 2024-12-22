from lib_exploded_room import *


class ExplodedRoomRunner(Runner):
  def __init__(self) -> None:
    super().__init__("exploded-room")

  def loop_main(self):
    params = ExplodedRoomParams()
    draw_exploded_room(params)
    return params

  def run(self, test:bool, seed:int, size:tuple[int, int]) -> int:
    mainseed = main(self.dir, "main", test, seed, size, self.loop_main)
    return mainseed


runner = ExplodedRoomRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

