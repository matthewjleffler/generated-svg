from lib_vertical_lines import *


def loop_main():
  params = VerticalLineParams()
  params.mutate = True
  params.draw_highlights = False
  draw_lines(params)


dir = "vertical-mutate"
seed = 0
test = True
size = SvgSize.Size11x17

if __name__ == "__main__":
  mainseed = main(dir, "main", test, seed, size, loop_main)

