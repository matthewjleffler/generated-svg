from lib_vertical_lines import *


def loop_combined():
  params = VerticalLineParams()
  draw_lines(params)
  return params

def loop_main():
  params = VerticalLineParams()
  params.draw_highlights = False
  draw_lines(params)
  return params

def loop_highlight():
  params = VerticalLineParams()
  params.draw_lines = False
  draw_lines(params)
  return params


dir = "vertical-lines"
seed = 0
test = True
size = SvgSize.Size9x12

def run():
  mainseed = main(dir, "combined", test, seed, size, loop_combined)
  main(dir, "main", test, mainseed, size, loop_main)
  main(dir, "highlight", test, mainseed, size, loop_highlight)

if __name__ == "__main__":
  run()

