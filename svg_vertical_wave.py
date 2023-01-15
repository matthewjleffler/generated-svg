from lib_wave import *

def loop_main():
  params = VerticalWaveParams()
  draw_wave(params)
  return params


dir = "vertical-wave"
seed = 0
test = True
size = SvgSize.Size11x17

def run():
  mainseed = main(dir, "main", test, seed, size, loop_main)

if __name__ == "__main__":
  run()

