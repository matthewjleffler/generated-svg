import random
from sys import maxsize
import os
from re import compile
from math import *
from enum import Enum
from typing import List


# Core SVG Drawing Library


# Helper classes

class Rect:
  def __init__(self, x:float, y:float, w:float, h:float):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  def bottom(self) -> float:
    return self.y + self.h

  def right(self) -> float:
    return self.x + self.w

  def center_x(self) -> float:
    return self.x + self.w / 2

  def center_y(self) -> float:
    return self.y + self.h / 2

  def contains(self, x:float, y:float) -> bool:
    return x >= self.x and y >= self.y and x <= self.right() and y <= self.bottom()


class Point:
  def __init__(self, x:float, y:float):
    self.x = x
    self.y = y

  def __lt__(self, other):
    if self.x == other.x:
      return self.y < other.y
    return self.x < other.x

  def length(self) -> float:
    return sqrt(self.x * self.x + self.y * self.y)

  def normalize(self):
    self_len = self.length()
    self.x /= self_len
    self.y /= self_len

  def multiply(self, scale:float):
    self.x *= scale
    self.y *= scale

  def multiply_copy(self, scale:float):
    result = Point(self.x, self.y)
    result.multiply(scale)
    return result

  def subtract_floats_copy(self, x:float,  y:float):
    return Point(self.x - x, self.y - y)

  def subtract_copy(self, other:float):
    return Point(self.x - other.x, self.y - other.y)

  def perpendicular_copy(self):
    length = self.length()
    angle = self.angle()
    return Point( length * cos(angle + pi / 2),
                  length * sin(angle + pi / 2))

  def angle(self) -> float:
    return atan2(self.y, self.x)

  def rotate_copy(self, rads:float):
    ca = cos(rads)
    sa = sin(rads)
    return Point(ca * self.x - sa * self.y,
                 sa * self.x + ca * self.y)


def add_nondup_point(x, y, points):
  for point in points:
    if point.x == x and point.y == y:
      return
  points.append(Point(x, y))


def clamp_point_list(clamp_val:int, points:List[Point]):
  for point in points:
    point.x = round(point.x / clamp_val, 0) * clamp_val
    point.y = round(point.y / clamp_val, 0) * clamp_val


class Group:
  def __init__(self, parent, settings):
    self.parent = parent
    self.settings = settings
    self.groups = []
    self.children = []


class RangeInt:
  def __init__(self, min_val:int, max_val:int):
    self._min_val = min_val
    self._max_val = max_val

  def rand(self) -> int:
    return rand_int(self._min_val, self._max_val)


class RangeFloat:
  def __init__(self, min_val:float, max_val:float):
    self._min_val = min_val
    self._max_val = max_val

  def rand(self) -> float:
    return rand_float(self._min_val, self._max_val)


# Math

def lerp(a:float, b:float, t:float) -> float:
  return (1 - t) * a + t * b

def ease_in_out_quad(t:float, b:float, c:float, d:float) -> float:
  return -c / 2 * (cos(pi * t / d) - 1) + b

def rand() -> float:
  return random.random()

def rand_float(min:float, max:float) -> float:
  delta = max - min
  return min + random.random() * delta

def rand_int(min:int, max:int) -> int:
  return random.randint(min, max)

def weighted_random(array) -> any:
  if len(array) < 1:
    return None
  sum = 0
  for item in array:
    sum += item[1]
  rand = random.random() * sum
  for item in array:
    rand -= item[1]
    if rand <= 0:
      return item[0]
  print("Error in weighted randomness")
  return None

def clamp(val:float, min_val:float, max_val:float) -> float:
  return min(max(val, min_val), max_val)

# Setup Variables

_svg_full = Rect(0, 0, 0, 0)
_svg_safe = Rect(0, 0, 0, 0)
_svg_border = 50
_text_indent = 0
_text_content = ""
_font_styles = dict()
_root_group = Group(None, "stroke=\"black\" fill=\"none\"")
_current_group = _root_group


def init():
  global _svg_full, _svg_safe, _svg_border, _text_indent, _text_content, _font_styles, _root_group, _current_group

  _svg_full = Rect(0, 0, 0, 0)
  _svg_safe = Rect(0, 0, 0, 0)
  _svg_border = 50
  _text_indent = 0
  _text_content = ""
  _font_styles = dict()
  _root_group = Group(None, "stroke=\"black\" fill=\"none\"")
  _current_group = _root_group


# Sizes

class SvgSize(Enum):
  Size11x17 = 1,
  Size9x12 = 2,


def setup_size(size:SvgSize):
  global _svg_full, _svg_safe

  if size is SvgSize.Size11x17:
    _svg_full = Rect(0, 0, 1630, 1060)
  elif size is SvgSize.Size9x12:
    _svg_full = Rect(0, 0, 1150, 870)

  _svg_safe = Rect(_svg_border, _svg_border, _svg_full.w - _svg_border * 2, _svg_full.h - _svg_border * 2)

def svg_safe() -> Rect:
  return _svg_safe

def svg_full() -> Rect:
  return _svg_full

# Text Writing

def add_text_line(line):
  global _text_content, _text_indent

  for _ in range(_text_indent):
    _text_content += "  "
  _text_content += line
  _text_content += "\n"


def open_text_indent(line):
  global _text_indent
  add_text_line(line)
  _text_indent = _text_indent + 1


def close_text_indent(line):
  global _text_indent

  _text_indent = max(_text_indent - 1, 0)
  add_text_line(line)


def write_file(name, number):
  if number > 0:
    svg_name = "{}_{}.svg".format(name, number)
  else:
    svg_name = "{}.svg".format(name)

  f = open("./{}/{}".format(name, svg_name), "w")
  f.write(_text_content)
  f.close()
  print("Wrote file: {}".format(svg_name))


# SVG Management

def commit(seed):
  open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(_svg_full.w, _svg_full.h))
  add_text_line("<!-- Seed: {} -->".format(seed))
  commit_group(_root_group)
  close_text_indent("</svg>")


def commit_group(group:Group):
  if group.settings is not None:
    open_text_indent("<g {}>".format(group.settings))
  else:
    open_text_indent("<g>")

  for child in group.children:
    add_text_line(child)
  for group in group.groups:
    commit_group(group)

  close_text_indent("</g>")


def open_group(settings, parent = None) -> Group:
  global _current_group

  if not parent:
    parent = _current_group

  new_group = Group(parent, settings)
  parent.groups.append(new_group)
  _current_group = new_group

  return new_group


def close_group():
  global _current_group

  if _current_group.parent == None:
    return

  _current_group = _current_group.parent


# Drawing

def draw_rect(x, y, w, h, group = None):
  if not group:
    group = _current_group
  group.children.append("<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\"/>".format(x, y, w, h))


def draw_circ(x, y, r, group = None):
  if not group:
    group = _current_group
  group.children.append("<circle cx=\"{}\" cy=\"{}\" r=\"{}\"/>".format(x, y, r))


def draw_path(value, group = None):
  if not group:
    group = _current_group
  group.children.append("<path d=\"{}\"/>".format(value))


def draw_border():
  open_group("stroke=\"red\"")
  draw_rect(_svg_safe.x, _svg_safe.y, _svg_safe.w, _svg_safe.h)
  close_group()


def draw_sunburst(bursts, c_x, c_y, start_rad, ray_len, group = None):
  sunburst_points = bursts
  for i in range(0, sunburst_points):
    t = i / sunburst_points
    rad = t * pi * 2

    x = round(c_x + sin(rad) * (start_rad), 2)
    y = round(c_y + cos(rad) * (start_rad), 2)

    vec = Point(x, y)
    vec = vec.subtract_copy(Point(c_x, c_y))
    vec.normalize()
    vec.multiply(ray_len)
    draw_path("M{} {} L{} {}".format(x, y, round(x + vec.x, 2), round(y + vec.y, 2)), group)


def draw_ring_of_circles(number, c_x, c_y, center_rad, circle_rad, group = None):
  for i in range(0, number):
    t = i / number
    rad = t * pi * 2

    x = c_x + cos(rad) * center_rad
    y = c_y + sin(rad) * center_rad
    draw_circ(x, y, circle_rad, group)

# Main

def main(name: str, test: bool, seed:int, size:SvgSize, loop:callable) -> int:
  init()
  setup_size(size)

  if seed == 0:
    seed = random.randrange(maxsize)
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

    file_name_search = compile(r"""^{}\D*(\d*).*svg$""".format(name))

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

  return seed

