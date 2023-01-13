from lib_stack import *


def loop():
  params = RectStackParams()
  draw_rect_stack(params)


dir = "rect-stack"
test = True
seed = 0
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main(dir, "main", test, seed, size, loop)

