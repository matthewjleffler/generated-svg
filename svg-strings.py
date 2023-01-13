from lib_strings import *


def loop():
  params = StringParams()
  draw_strings(params)


dir = "strings"
seed = 0
test = True
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main(dir, "main", test, seed, size, loop)
