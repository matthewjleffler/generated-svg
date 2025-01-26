from lib import *


class TestTextRunner(Runner):
  def __init__(self) -> None:
    super().__init__("test-text")

  def loop(self, defaults: Defaults, group: Group, seed: int):
    # draw_border(group)

    draw_text(100, 200, 10, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", group)
    draw_text(100, 300, 10, "abcdefghijklmnopqrstuvwxyz", group)
    draw_text(100, 400, 10, "0123456789 ;:'\"éÉ`~", group)
    draw_text(100, 500, 10, "!@#$%^&*()-_+={}[]\|,./<>?", group)

    group_scaled = open_group(GroupSettings(translate=(100, 600), scale=0.5), group)
    draw_text(0, 0, 10, "Test Small Text too", group_scaled)

    group_rotated = open_group(GroupSettings(translate=(100, 700), rotate=10), group)
    draw_text(0, 0, 10, "TEST ROTATED TEXT", group_rotated)

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = TestTextRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 1,
    size = (9, 12)
  )
  runner.run(defaults)

