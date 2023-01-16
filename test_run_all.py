import types
import svg_checkerboard
import svg_circle_stack
import svg_long_worm
import svg_rect_stack
import svg_radial_circles
import svg_spiral_circle
import svg_spiral_worm
import svg_strings
import svg_template
import svg_test_text
import svg_vertical_lines
import svg_vertical_mutate
import svg_vertical_wave
import svg_worm


def run():
  print("Running all SVG scripts...")

  count = 0
  for name, val in globals().items():
    if isinstance(val, types.ModuleType):
      if not name.startswith("svg_"):
        continue
      print(f"\nRunning {name}")
      count += 1
      val.run()

  print(f"\nFinished running {count} script(s)")


if __name__ == "__main__":
  run()
