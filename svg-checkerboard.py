from lib_checkerboard import *

def loop():
  params = CheckerboardParams()
  draw_checkerboard(params)

dir = "checkerboard"
seed = 0
test = True
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main(dir, "main", test, seed, size, loop)

