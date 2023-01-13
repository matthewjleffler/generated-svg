from lib import *
from lib_path import *
from lib_text import *
from math import *


def loop():
  draw_border()

  draw_text(200, 200, 5, "Test Text")


dir = "template"
test = True
seed = 0
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main(dir, "main", test, seed, size, loop)

