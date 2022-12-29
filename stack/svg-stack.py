import random
import math
import sys
import os
import re

# Setup Variables

file_name = "stack"
test = False # Whether or not to rewrite the test file only
seed = 7780133885520176573 # Whether or not to use a set seed

# Widths:
# A3(?) 1550 x 950
# 9x12 1150 x 870

svg_width = 1150
svg_height = 870

svg_border = 50
svg_left = svg_top = svg_border
svg_right = svg_width - svg_border
svg_bottom = svg_height - svg_border
svg_safe_width = svg_right - svg_left
svg_safe_height = svg_bottom - svg_top

file_name_search = re.compile(r"""^{}\D*(\d*).*svg$""".format(file_name))
text_indent = 0
text_content = ""


# Text Writing

def add_text_line(line):
  global text_content, text_indent

  for _ in range(text_indent):
    text_content += "  "
  text_content += line
  text_content += "\n"


def open_text_indent(line):
  global text_indent
  add_text_line(line)
  text_indent = text_indent + 1


def close_text_indent(line):
  global text_indent

  text_indent = max(text_indent - 1, 0)
  add_text_line(line)


def rect(x, y, w, h, color = "black"):
  add_text_line("<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\" stroke=\"{}\" fill-opacity=\"0\"/>".format(x + svg_border, y + svg_border, w, h, color))


def write_file(number):
  if number > 0:
    svg_name = "{}_{}.svg".format(file_name, number)
  else:
    svg_name = "{}.svg".format(file_name)

  f = open("./{}".format(svg_name), "w")
  f.write(text_content)
  f.close()
  print("Wrote file: {}".format(svg_name))

# Image Specific Content

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __lt__(self, other):
    if self.x == other.x:
      return self.y < other.y
    return self.x < other.x


def add_nondup_point(x, y, rects):
  for point in rects:
    if point.x == x and point.y == y:
      return
  rects.append(Point(x, y))


def loop():
  global svg_width, svg_height

  # Border
  # rect(0, 0, svg_safe_width, svg_safe_height, "red")

  count = 30
  stack_count = 15
  # count = random.randrange(20, 100)
  # print("Rectangles: {}".format(count))

  rects = []

  for _ in range(count):
    x = random.randrange(0, svg_safe_width - 100 - 10 * max(stack_count - 1, 0))
    y = random.randrange(0, svg_safe_height - 100 - 10 * max(stack_count - 1, 0))

    x = round(x / 10, 0) * 10
    y = round(y / 10, 0) * 10

    for i in range(0, stack_count):
      add_nondup_point(x + i * 10, y + i * 10, rects)

  rects.sort()

  for point in rects:
    rect(point.x, point.y, 100, 100)


# Main

def main():
  global seed

  if seed == 0:
    seed = random.randrange(sys.maxsize)
  random.seed(seed)
  print("Seed: {}".format(seed))

  open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(svg_width, svg_height))

  add_text_line("<!-- Seed: {} -->".format(seed))

  loop()
  close_text_indent("</svg>")
  # print(text_content)

  if test:
    # Only overwrite test content
    write_file(0)
  else:
    # Write numbered content
    # Consume existing file names
    max_number = 0
    existing = os.listdir(".")
    for file in existing:
      search = file_name_search.match(file)
      if search == None:
        continue
      group = search.group(1)
      if not group:
        continue
      number = int(group)
      if not number:
        continue
      max_number = max(max_number, number)

    # Pick the next number in sequence, including missing numbers
    min_available_number = max_number + 1

    write_file(min_available_number)


if __name__ == "__main__":
  main()
