from lib import *
from lib_text import *


class TestTextRunner(Runner):
  def __init__(self) -> None:
    super().__init__("test-text")

  def loop(self):
    # draw_border()

    draw_text(100, 200, 10, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    draw_text(100, 300, 10, "abcdefghijklmnopqrstuvwxyz")
    draw_text(100, 400, 10, "0123456789 ;:'\"éÉ`~")
    draw_text(100, 500, 10, "!@#$%^&*()-_+={}[]\|,./<>?")

    open_group("transform=\"translate(100,600) scale(0.5,0.5)\"")
    draw_text(0, 0, 10, "Test Small Text too")
    close_group()

    open_group("transform=\"translate(100, 700) rotate(10)\"")
    draw_text(0, 0, 10, "TEST ROTATED TEXT")
    close_group()

  def run(self, test:bool, seed:int, size:tuple[int, int]) -> int:
    mainseed = main(self.dir, "main", test, seed, size, self.loop)
    return mainseed


runner = TestTextRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 1,
    size = (9, 12)
  )
  runner.run(defaults.test, defaults.seed, defaults.size)

