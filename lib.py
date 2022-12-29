import random
import sys
import os
import re
from enum import Enum

# Helper classes

class Rect:
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  def bottom(self):
    return self.y + self.h

  def right(self):
    return self.x + self.w

  def contains(self, x, y) -> bool:
    return x >= self.x and y >= self.y and x <= self.right() and y <= self.bottom()


class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __lt__(self, other):
    if self.x == other.x:
      return self.y < other.y
    return self.x < other.x


def add_nondup_point(x, y, points):
  for point in points:
    if point.x == x and point.y == y:
      return
  points.append(Point(x, y))

# Setup Variables

svg_full = Rect(0, 0, 0, 0)
svg_safe = Rect(0, 0, 0, 0)
svg_border = 50
text_indent = 0
text_content = ""


# Sizes

class SvgSize(Enum):
  SizeA3 = 1,
  Size9x12 = 2,


def setup_size(size:SvgSize):
  global svg_full, svg_safe

  if size is SvgSize.SizeA3:
    svg_full = Rect(0, 0, 1550, 950)
  elif size is SvgSize.Size9x12:
    svg_full = Rect(0, 0, 1150, 870)

  svg_safe = Rect(svg_border, svg_border, svg_full.w - svg_border * 2, svg_full.h - svg_border * 2)


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


def write_file(name, number):
  if number > 0:
    svg_name = "{}_{}.svg".format(name, number)
  else:
    svg_name = "{}.svg".format(name)

  f = open("./{}/{}".format(name, svg_name), "w")
  f.write(text_content)
  f.close()
  print("Wrote file: {}".format(svg_name))

# Shapes

def rect(x, y, w, h, color = "black"):
  add_text_line("<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\" stroke=\"{}\" fill-opacity=\"0\"/>".format(x, y, w, h, color))

def circ(x, y, r, color = "black"):
  add_text_line("<circle cx=\"{}\" cy=\"{}\" r=\"{}\" stroke=\"{}\" fill-opacity=\"0\"/>".format(x, y, r, color))

# Main

def main(name: str, test: bool, seed:int, size:SvgSize, loop:callable):
  setup_size(size)

  if seed == 0:
    seed = random.randrange(sys.maxsize)
  random.seed(seed)
  print("Seed: {}".format(seed))

  open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(svg_full.w, svg_full.h))

  add_text_line("<!-- Seed: {} -->".format(seed))

  loop()
  close_text_indent("</svg>")
  # print(text_content)

  # Make directory if necessary
  if not os.path.exists(name):
    os.makedirs(name)

  # Write content
  if test:
    # Only overwrite test content
    write_file(name, 0)
  else:
    # Write numbered content
    # Consume existing file names
    max_number = 0
    existing = os.listdir("./{}".format(name))

    file_name_search = re.compile(r"""^{}\D*(\d*).*svg$""".format(name))

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

    write_file(name, min_available_number)

