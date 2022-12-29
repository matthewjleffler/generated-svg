import lib

def loop():
  # Border
  lib.rect_safe(0, 0, lib.svg_safe_width, lib.svg_safe_height, "red")


if __name__ == "__main__":
  lib.main(
    "template",
    True,
    0,
    lib.SvgSize.Size9x12,
    loop
  )
