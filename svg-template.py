import lib

def loop():
  # Border
  lib.rect(lib.svg_safe.x, lib.svg_safe.y, lib.svg_safe.w, lib.svg_safe.h, "red")


if __name__ == "__main__":
  lib.main(
    "template",
    True,
    0,
    lib.SvgSize.Size9x12,
    loop
  )
