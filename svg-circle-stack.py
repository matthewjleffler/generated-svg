from lib_stack import *


def loop():
  params = CircleStackParams()
  draw_circle_stack(params)


dir = "circle-stack"
test = True
seed = 0
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main(dir, "main", test, seed, size, loop)

