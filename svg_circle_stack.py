from lib_stack import *


def loop():
  params = CircleStackParams()
  draw_circle_stack(params)
  return params


dir = "circle-stack"
test = True
seed = 0
size = SvgSize.Size9x12

def run():
  mainseed = main(dir, "main", test, seed, size, loop)

if __name__ == "__main__":
  run()

