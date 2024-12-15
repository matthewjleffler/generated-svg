import random
from sys import maxsize, argv
import os
from re import compile
from math import *
from lib_math import *
from enum import Enum
from typing import List
from lib_rand import *


###
### Core SVG Drawing Library
###

# Helper functions

def add_nondup_floats(
    x:float,
    y:float,
    points:List[Point],
    deltaRange: int = 1
  ):
  if len(points) > 0 and deltaRange > 0:
    item = points[-1]
    delta = item.subtract_floats_copy(x, y).length()
    if delta < deltaRange:
      return
  points.append(Point(x, y))


def add_nondup_point(
    point:Point,
    points:List[Point],
    deltaRange: int = 1
  ):
  if len(points) > 0 and deltaRange > 0:
    item = points[-1]
    delta = item.subtract_copy(point).length()
    if delta < deltaRange:
      return
  points.append(point.copy())


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
_pixel_per_inch = 95.8


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

def setup_size(size:tuple[int, int]):
  global _svg_full, _svg_safe
  (x, y) = size
  w = max(x, y)
  h = min(x, y)
  _svg_full = Rect(0, 0, floor(w * _pixel_per_inch), floor(h * _pixel_per_inch))
  _svg_safe = Rect(_svg_border, _svg_border, _svg_full.w - _svg_border * 2, _svg_full.h - _svg_border * 2)

def svg_safe() -> Rect:
  return _svg_safe

def svg_full() -> Rect:
  return _svg_full


# Running
class Runner:
  def __init__(self, dir:str) -> None:
    self.dir = dir

  def run(self, test:bool, seed:int, size:tuple[int, int]) -> int:
    return 0


class Defaults:
  def __init__(self, test:bool, seed:int, size:tuple[int, int]) -> None:
    self.test:bool = test
    self.seed:int = seed
    self.size:tuple[int, int] = size


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

  def get_svg_size(self, key:str, default:tuple[int, int]) -> tuple[int, int]:
    if key not in self.__args:
      return default
    stringSize: str = self.__args[key]
    split: List[str] = stringSize.split('x')
    if len(split) != 2:
      print(f"Need size in format [w]x[h]")
      return default
    [strx, stry] = split
    return (int(strx), int(stry))

  def get_defaults(self, test:bool, seed:int, size:tuple[int, int]) -> Defaults:
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

def commit(seed:int, size:tuple[int, int], params:any):
  (x, y) = size
  open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(_svg_full.w, _svg_full.h))
  add_text_line(f"<!-- Seed: {seed} -->")
  add_text_line(f"<!-- Size: {x}x{y} -->")
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

def draw_rect_rect(rect: Rect, group: Group = None):
  draw_rect(rect.x, rect.y, rect.w, rect.h, group)

def draw_circ(x:float, y:float, r:float, group:Group = None):
  if not group:
    group = _current_group
  x = round(x, 2)
  y = round(y, 2)
  r = round(r, 2)
  group.children.append(f"<circle cx=\"{x}\" cy=\"{y}\" r=\"{r}\"/>")

def draw_circ_point(point: Point, r:float, group:Group = None):
  draw_circ(point.x, point.y, r, group)

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

def main(dir:str, layer: str, test: bool, seed:int, size:tuple[int, int], loop:callable) -> int:
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

