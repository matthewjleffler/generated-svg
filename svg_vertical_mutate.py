from lib_vertical_lines import *


def loop_main():
  params = VerticalLineParams()
  params.mutate = True
  params.draw_highlights = False
  draw_lines(params)
  return params


dir = "vertical-mutate"
seed = 0
test = True
size = SvgSize.Size11x17

def run():
  mainseed = main(dir, "main", test, seed, size, loop_main)

if __name__ == "__main__":
  run()

