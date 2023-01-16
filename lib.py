import random
from sys import maxsize, argv
import os
from re import compile
from math import *
from enum import Enum
from typing import List


###
### Core SVG Drawing Library
###


# Helper classes

class Rect:
  def __init__(self, x:float, y:float, w:float, h:float):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  def __repr__(self) -> str:
    return f"[Rect] x:{self.x} y:{self.y} w:{self.w} h:{self.h} cx:{self.center_x()} cy:{self.center_y()} r:{self.right()} b:{self.bottom()}"

  def bottom(self) -> float:
    return self.y + self.h

  def right(self) -> float:
    return self.x + self.w

  def center_x(self) -> float:
    return floor(self.x + self.w / 2)

  def center_y(self) -> float:
    return floor(self.y + self.h / 2)

  def contains(self, x:float, y:float) -> bool:
    return x >= self.x and y >= self.y and x <= self.right() and y <= self.bottom()

  def shrink_xy_copy(self, amount_x:float, amount_y:float):
    return Rect(self.x + amount_x, self.y + amount_y, self.w - amount_x * 2, self.h - amount_y * 2)

  def shrink_copy(self, amount:float):
    return Rect(self.x + amount, self.y + amount, self.w - amount * 2, self.h - amount * 2)


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


def add_nondup_point(x:float, y:float, points:List[Point]):
  x = round(x, 0)
  y = round(y, 0)
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

  def __repr__(self) -> str:
    return f"[RangeInt] min: {self._min_val} max: {self._max_val}"

  def rand(self) -> int:
    return rand_int(self._min_val, self._max_val)


class RangeFloat:
  def __init__(self, min_val:float, max_val:float):
    self._min_val = min_val
    self._max_val = max_val

  def __repr__(self) -> str:
    return f"[RangeFloat] min: {self._min_val} max: {self._max_val}"

  def rand(self) -> float:
    return rand_float(self._min_val, self._max_val)


# Math

def lerp(a:float, b:float, t:float) -> float:
  return round((1 - t) * a + t * b, 2)

def ease_in_out_quad(t:float, b:float, c:float, d:float) -> float:
  return round(-c / 2 * (cos(pi * t / d) - 1) + b, 2)

def rand() -> float:
  return random.random()

def rand_bool() -> bool:
  return rand_int(0, 1) == 0

def rand_float(min:float, max:float) -> float:
  delta = max - min
  return min + random.random() * delta

def rand_int(min:int, max:int) -> int:
  return random.randint(min, max)

def rand_weight(array) -> any:
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

def clamp_value(val:float, clamp_value:float) -> float:
  return floor(val / clamp_value) * clamp_value

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

  @staticmethod
  def from_str(val:str):
    val = val.lower()
    if val == "size9x12" or val == "9x12":
      return SvgSize.Size9x12
    if val == "size11x17" or val == "11x17":
      return SvgSize.Size11x17
    print(f"Unhandled SvgSize: {val}")
    return SvgSize.Size9x12


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


# Running
class Runner:
  def __init__(self, dir:str) -> None:
    self.dir = dir

  def run(self, test:bool, seed:int, size:SvgSize):
    pass # Override


class Defaults:
  def __init__(self, test:bool, seed:int, size:SvgSize) -> None:
    self.test:bool = test
    self.seed:int = seed
    self.size:SvgSize = size


class Args:
  def __init__(self) -> None:
    self.__positional = []
    self.__args = dict()

    parse = compile(r"""--(.*?)=(.*)""")
    for i in range(1, len(argv)):
      arg = argv[i]
      parsed = parse.match(arg)
      if parsed is None:
        self.__positional.append(arg)
      else:
        self.__args[parsed.group(1)] = parsed.group(2)

  def _get_bool(self, val:str) -> bool:
    return val == "True" or val == "true" or val == "t"

  def positional_count(self) -> int:
    return len(self.__positional)

  def positional_str(self, index:int) -> str:
    return self.__positional[index]

  def positional_int(self, index:int) -> int:
    return int(self.__positional[index])

  def positional_bool(self, index:int) -> bool:
    return self._get_bool(self.__positional[index])

  def positional_float(self, index:int) -> float:
    return float(self.__positional[index])

  def get_str(self, key:str, default:str) -> str:
    if key not in self.__args:
      return default
    return self.__args[key]

  def get_int(self, key:str, default:int) -> int:
    if key not in self.__args:
      return default
    return int(self.__args[key])

  def get_bool(self, key:str, default:bool) -> bool:
    if key not in self.__args:
      return default
    return self._get_bool(self.__args[key])

  def get_float(self, key:str, default:float) -> float:
    if key not in self.__args:
      return default
    return float(self.__args[key])

  def get_svg_size(self, key:str, default:SvgSize) -> SvgSize:
    if key not in self.__args:
      return default
    return SvgSize.from_str(self.__args[key])

  def get_defaults(self, test:bool, seed:int, size:SvgSize) -> Defaults:
    test = self.get_bool("test", test)
    seed = self.get_int("seed", seed)
    size = self.get_svg_size("size", size)
    return Defaults(test, seed, size)


# Text Writing

def add_text_line(line:str):
  global _text_content, _text_indent

  for _ in range(_text_indent):
    _text_content += "  "
  _text_content += line
  _text_content += "\n"


def open_text_indent(line:str):
  global _text_indent
  add_text_line(line)
  _text_indent = _text_indent + 1


def close_text_indent(line:str):
  global _text_indent

  _text_indent = max(_text_indent - 1, 0)
  add_text_line(line)


def write_file(path:str, name:str, number:int):
  if number > 0:
    svg_name = "{}_{}.svg".format(name, number)
  else:
    svg_name = "{}.svg".format(name)

  f = open(f"{path}/{svg_name}", "w")
  f.write(_text_content)
  f.close()
  print(f"Wrote file: {path}/{svg_name}")


# SVG Management

def commit(seed:int, size:SvgSize, params:any):
  open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(_svg_full.w, _svg_full.h))
  add_text_line(f"<!-- Seed: {seed} -->")
  add_text_line(f"<!-- Size: {size} -->")
  if params is not None:
    list_params = vars(params)
    open_text_indent("<!-- Params:")
    for item in list_params:
      add_text_line(f"{item}: {list_params[item]}")
    close_text_indent("-->")
  else:
    add_text_line("<!-- No params -->")
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


def open_group(settings, parent:Group = None) -> Group:
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

def draw_rect(x:float, y:float, w:float, h:float, group:Group = None):
  if not group:
    group = _current_group
  x = round(x, 2)
  y = round(y, 2)
  w = round(w, 2)
  h = round(h, 2)
  group.children.append(f"<rect x=\"{x}\" y=\"{y}\" width=\"{w}\" height=\"{h}\"/>")


def draw_circ(x:float, y:float, r:float, group:Group = None):
  if not group:
    group = _current_group
  x = round(x, 2)
  y = round(y, 2)
  r = round(r, 2)
  group.children.append(f"<circle cx=\"{x}\" cy=\"{y}\" r=\"{r}\"/>")


def draw_path(value:str, group:Group = None):
  if not group:
    group = _current_group
  group.children.append(f"<path d=\"{value}\"/>")


def draw_border(group:Group = None):
  open_group("stroke=\"red\"", group)
  draw_rect(_svg_safe.x, _svg_safe.y, _svg_safe.w, _svg_safe.h)
  close_group()


def draw_sunburst(bursts:int, c_x:float, c_y:float, start_rad:float, ray_len:float, group:Group = None):
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


def draw_ring_of_circles(number:int, c_x:float, c_y:float, center_rad:float, circle_rad:float, group:Group = None):
  for i in range(0, number):
    t = i / number
    rad = t * pi * 2

    x = c_x + cos(rad) * center_rad
    y = c_y + sin(rad) * center_rad
    draw_circ(x, y, circle_rad, group)

# Main

def main(dir:str, layer: str, test: bool, seed:int, size:SvgSize, loop:callable) -> int:
  init()
  setup_size(size)

  if seed == 0:
    seed = random.randrange(maxsize)
  random.seed(seed)
  print("Seed: {}".format(seed))

  params = loop()
  commit(seed, size, params)
  # print(text_content)

  # Make directory if necessary
  fullpath = f"./output/{dir}/{layer}"
  if not os.path.exists(fullpath):
    os.makedirs(fullpath)

  # Write content
  if test:
    # Only overwrite test content
    write_file(fullpath, layer, 0)
  else:
    # Write numbered content
    # Consume existing file names
    max_number = 0
    existing = os.listdir(fullpath)

    file_name_search = compile(r"""^{}\D*(\d*).*svg$""".format(layer))

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

    write_file(fullpath, layer, min_available_number)

  return seed

