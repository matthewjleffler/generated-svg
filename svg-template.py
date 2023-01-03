import lib
import text

def loop():
  lib.border()

  text.draw_string(200, 200, 5, "test text")


seed = 1
test = True
size = lib.SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = lib.main("template", test, seed, size, loop)

