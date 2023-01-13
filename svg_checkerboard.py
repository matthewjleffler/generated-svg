from lib_checkerboard import *


def loop():
  params = CheckerboardParams()
  draw_checkerboard(params)
  return params


dir = "checkerboard"
seed = 0
test = True
size = SvgSize.Size9x12

def run():
  mainseed = main(dir, "main", test, seed, size, loop)

if __name__ == "__main__":
  run()
