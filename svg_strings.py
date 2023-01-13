from lib_strings import *


def loop():
  params = StringParams()
  draw_strings(params)
  return params


dir = "strings"
seed = 0
test = True
size = SvgSize.Size9x12

def run():
  mainseed = main(dir, "main", test, seed, size, loop)

if __name__ == "__main__":
  run()

