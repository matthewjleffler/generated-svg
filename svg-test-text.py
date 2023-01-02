import lib


def loop():
  lib.border()

  lib.draw_string(100, 200, 10, "abcdefghijklmnopqrstuvwxyz")
  lib.draw_string(100, 300, 10, "0123456789")

  lib.open_group("transform=\"translate(100,400) scale(0.5,0.5)\"")
  lib.draw_string(0, 0, 10, "test small text too")
  lib.close_group()

  lib.open_group("transform=\"translate(100, 500) rotate(15)\"")
  lib.draw_string(0, 0, 10, "test rotated text 2045")
  lib.close_group()


if __name__ == "__main__":
  lib.main(
    "test-text",
    True,
    1,
    lib.SvgSize.Size9x12,
    loop
  )
