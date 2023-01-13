from stack import *


def loop():
  # draw_border()

  params = RectStackParams()
  draw_rect_stack(params)


test = True
seed = 0
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("stack", test, seed, SvgSize.Size9x12, loop)

