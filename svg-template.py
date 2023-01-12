from lib import *
from path import *
from text import *
from math import *

def loop():
  draw_border()

  draw_text(200, 200, 5, "Test Text")


seed = 0
test = True
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("template", test, seed, size, loop)

