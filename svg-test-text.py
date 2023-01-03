import lib
import text


def loop():
  # lib.border()

  text.draw_string(100, 200, 10, "abcdefghijklmnopqrstuvwxyz")
  text.draw_string(100, 300, 10, "0123456789 ;:'\"")
  text.draw_string(100, 400, 10, "!@#$%^&*()-_+={}[]\|,./<>?")

  lib.open_group("transform=\"translate(100,500) scale(0.5,0.5)\"")
  text.draw_string(0, 0, 10, "test small text too")
  lib.close_group()

  lib.open_group("transform=\"translate(100, 600) rotate(10)\"")
  text.draw_string(0, 0, 10, "test rotated text 2045")
  lib.close_group()


if __name__ == "__main__":
  lib.main(
    "test-text",
    True,
    1,
    lib.SvgSize.Size9x12,
    loop
  )