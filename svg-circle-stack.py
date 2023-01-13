from stack import *


def loop():
  # draw_border()

  params = CircleStackParams()
  draw_circle_stack(params)


test = True
seed = 0
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("circle-stack", test, seed, size, loop)

