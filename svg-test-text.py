from lib import *
from text import *


def loop():
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


seed = 1
test = True
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("test-text", test, seed, size, loop)
