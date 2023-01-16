from lib_spiral_circle import *


def loop():
  params = SpiralCircleParams()
  draw_spiral_circle(params)
  return params


dir = "spiral-circle"
seed = 0
test = True
image_size = SvgSize.Size9x12

def run():
  mainseed = main(dir, "main", test, seed, image_size, loop)

if __name__ == "__main__":
  run()

