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

  def center_x(self):
    return self.x + self.w / 2

  def center_y(self):
    return self.y + self.h / 2

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


class Group:
  def __init__(self, parent, settings):
    self.parent = parent
    self.settings = settings
    self.groups = []
    self.children = []


# Setup Variables

svg_full = Rect(0, 0, 0, 0)
svg_safe = Rect(0, 0, 0, 0)
svg_border = 50
text_indent = 0
text_content = ""
font_styles = dict()
root_group = Group(None, "stroke=\"black\" fill=\"none\"")
current_group = root_group


def init():
  global svg_full, svg_safe, svg_border, text_indent, text_content, font_styles, root_group, current_group

  svg_full = Rect(0, 0, 0, 0)
  svg_safe = Rect(0, 0, 0, 0)
  svg_border = 50
  text_indent = 0
  text_content = ""
  font_styles = dict()
  root_group = Group(None, "stroke=\"black\" fill=\"none\"")
  current_group = root_group


# Sizes

class SvgSize(Enum):
  Size11x17 = 1,
  Size9x12 = 2,


def setup_size(size:SvgSize):
  global svg_full, svg_safe

  if size is SvgSize.Size11x17:
    svg_full = Rect(0, 0, 1630, 1060)
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


# SVG Management

def commit(seed):
  open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(svg_full.w, svg_full.h))
  add_text_line("<!-- Seed: {} -->".format(seed))
  commit_font_styles()
  commit_group(root_group)
  close_text_indent("</svg>")


def commit_group(group:Group):
  open_text_indent("<g {}>".format(group.settings))

  for child in group.children:
    add_text_line(child)
  for group in group.groups:
    commit_group(group)

  close_text_indent("</g>")


def add_font_style(name, settings):
  font_styles[name] = settings


def commit_font_styles():
  if len(font_styles) < 1:
    return

  # Write style block
  open_text_indent("<style>")

  for key in font_styles:
    open_text_indent(".{} {{".format(key))
    add_text_line("font: {};".format(font_styles[key]))
    close_text_indent("}")

  close_text_indent("</style>")


def open_group(settings):
  global current_group

  new_group = Group(current_group, settings)
  current_group.groups.append(new_group)
  current_group = new_group


def close_group():
  global current_group

  if current_group.parent == None:
    return

  current_group = current_group.parent


# Drawing

def rect(x, y, w, h):
  current_group.children.append("<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\"/>".format(x, y, w, h))


def circ(x, y, r):
  current_group.children.append("<circle cx=\"{}\" cy=\"{}\" r=\"{}\"/>".format(x, y, r))


def svg_text(x, y, name, value):
  current_group.children.append("<text x=\"{}\" y=\"{}\" class=\"{}\">{}</text>".format(x, y, name, value))


def border():
  open_group("stroke=\"red\"")
  rect(svg_safe.x, svg_safe.y, svg_safe.w, svg_safe.h)
  close_group()


# Main

def main(name: str, test: bool, seed:int, size:SvgSize, loop:callable):
  init()
  setup_size(size)

  if seed == 0:
    seed = random.randrange(sys.maxsize)
  random.seed(seed)
  print("Seed: {}".format(seed))

  loop()
  commit(seed)
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

