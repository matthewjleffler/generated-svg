import lib

def loop():
  # Add fonts first
  # lib.add_font_style("small", "24px sans-serif")
  # lib.commit_font_styles()

  # Border
  lib.rect(lib.svg_safe.x, lib.svg_safe.y, lib.svg_safe.w, lib.svg_safe.h, "red")

  # TODO Strings must be converted to paths
  # lib.svg_text(200, 200, "small", "Test String")


if __name__ == "__main__":
  lib.main(
    "template",
    True,
    1,
    lib.SvgSize.Size9x12,
    loop
  )
