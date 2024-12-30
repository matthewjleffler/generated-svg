import random
import time
from datetime import timedelta
from sys import maxsize, argv
import os
from re import compile
from math import *
from lib_math import *
from enum import StrEnum
from typing import List
from lib_rand import *


###
### Core SVG Drawing Library
###

# Helper functions

def test_type(obj: any, field: str, expected: str) -> bool:
  return type(getattr(obj, field)).__name__ == expected

def add_nondup_floats(x:float, y:float, points:List[Point]):
  points.append(Point(x, y))


def add_nondup_point(point:Point, points:List[Point]):
  points.append(point.copy())


def clamp_point_list(clamp_val:int, points:List[Point]):
  for point in points:
    point.x = round(point.x / clamp_val, 0) * clamp_val
    point.y = round(point.y / clamp_val, 0) * clamp_val

class GroupColor(StrEnum):
  black = 'black'
  blue = 'blue'
  red = 'red'
  green = 'green'
  none = 'none'


class GroupSettings:
  def __init__(
      self,
      stroke: str = None,
      fill: str = None,
      translate: tuple[float, float] = None,
      translatePoint: Point = None,
      scale: float = None,
      scaleXY: tuple[float, float] = None,
      scalePoint: Point = None,
      rotate: float = None,
  ):
    settings: List[str] = []

    if stroke is not None:
      settings.append(f"stroke=\"{stroke}\"")

    if fill is not None:
      settings.append(f"fill=\"{fill}\"")

    transforms: List[str] = []

    if translate is not None:
      transforms.append(f"translate({translate[0]}, {translate[1]})")
    elif translatePoint is not None:
      transforms.append(f"translate({translatePoint.x}, {translatePoint.y})")

    if scale is not None:
      transforms.append(f"scale({scale}, {scale})")
    elif scaleXY is not None:
      transforms.append(f"scale({scaleXY[0]}, {scaleXY[1]})")
    elif scalePoint is not None:
      transforms.append(f"scale({scalePoint.x}, {scalePoint.y})")

    if rotate is not None:
      transforms.append(f"rotate({rotate})")

    if len(transforms) > 0:
      settings.append(f"transform=\"{' '.join(transforms)}\"")

    self.settings = ""
    if len(settings) > 0:
      self.settings = ' '.join(settings)


class Group:
  def __init__(self, parent: 'Group', settings: GroupSettings):
    self.parent = parent
    self.settings = settings.settings
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
_text_lines: List[str] = []
_text_content = ""
_font_styles = dict()
_root_group = Group(None, GroupSettings(stroke=GroupColor.black, fill=GroupColor.none))
_current_group = _root_group
_pixel_per_inch = 95.8
_round_digits = 2


def init():
  global _svg_full, _svg_safe, _svg_border, _text_indent, _text_content, _font_styles, _root_group, _current_group, _text_lines

  _svg_full = Rect(0, 0, 0, 0)
  _svg_safe = Rect(0, 0, 0, 0)
  _svg_border = 50
  _text_indent = 0
  _text_lines = []
  _text_content = ""
  _font_styles = dict()
  _root_group = Group(None, GroupSettings(stroke=GroupColor.black, fill=GroupColor.none))
  _current_group = _root_group


# Sizes

def setup_size(size:tuple[float, float]):
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
class Defaults:
  def __init__(self, test:bool, seed:int, size:tuple[float, float], params:dict[str] = dict()) -> None:
    self.test:bool = test
    self.seed:int = seed
    self.size:tuple[float, float] = size
    self.params:dict[str] = params

class BaseParams:
  def __init__(self, defaults: Defaults) -> None:
    self._apply_params(defaults)

  def _apply_params(self, defaults: Defaults) -> None:
    for k, v in defaults.params.items():
      val = self.__parse(v)
      if val is not None:
        setattr(self, k, val)
        print('Applied:', k, val)
      else:
        print('Invalid param:', k, v)
    if defaults.test:
      # All params allowed
      return
    print('Disabling Debug')
    attrs = dir(self)
    for attr in attrs:
      if not attr.startswith('debug_'):
        continue
      if not test_type(self, attr, 'bool'):
        continue
      setattr(self, attr, False)

  def __parse_number(self, v: str):
    try:
      # Float
      float_res = float(v.strip())
      if float_res.is_integer():
        # Int
        return int(float_res)
      return float_res
    except ValueError:
      return None

  def __parse(self, v: str):
    lower = v.lower().strip()
    split = lower.split(":")
    if split[0] == 'w' and len(split) > 1:
      # Weights
      result: List[tuple[int, float]] = []
      for i in range(1, len(split)):
        str_weight = split[i].split(',')
        if len(str_weight) != 2:
          return None
        [str_val, str_weight] = str_weight
        val = self.__parse_number(str_val)
        weight = self.__parse_number(str_weight)
        if val is None or weight is None:
          return None
        result.append([int(val), weight])
      return result
    elif len(split) == 1:
      # Bools
      if lower == "true" or lower == "t":
        return True
      if lower == "false" or lower == "f":
        return False
      # Number
      return self.__parse_number(v)
    elif len(split) == 3:
      [r_type, r_min, r_max] = split
      if r_type == 'ri':
        ri_min = self.__parse_number(r_min)
        ri_max = self.__parse_number(r_max)
        if ri_min is None or ri_max is None:
          return None
        return RangeInt(int(ri_min), int(ri_max))
      elif r_type == 'rf':
        rf_min = self.__parse_number(r_min)
        rf_max = self.__parse_number(r_max)
        if rf_min is None or rf_max is None:
          return None
        return RangeFloat(rf_min, rf_max)
    return None


class Runner:
  def __init__(self, dir:str) -> None:
    self.dir = dir

  def run(self, defaults: Defaults) -> int:
    return 0


class Args:
  def __init__(self) -> None:
    self.__positional = []
    self.__args: dict[str] = dict()
    self.__params: dict[str] = dict()

    parse = compile(r"""--(.*?)=(.*)""")
    param_parse = compile(r"""\+\+(.*?)=(.*)""")
    for i in range(1, len(argv)):
      arg = argv[i]
      parsed = parse.match(arg)
      params = param_parse.match(arg)
      if parsed is None and params is None:
        self.__positional.append(arg)
      elif parsed is not None:
        self.__args[parsed.group(1)] = parsed.group(2)
      elif params is not None:
        self.__params[params.group(1)] = params.group(2)

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

  def get_svg_size(self, key:str, default:tuple[float, float]) -> tuple[float, float]:
    if key not in self.__args:
      return default
    stringSize: str = self.__args[key]
    split: List[str] = stringSize.split('x')
    if len(split) != 2:
      print(f"Need size in format [w]x[h]")
      return default
    [strx, stry] = split
    x = float(strx)
    y = float(stry)
    if x.is_integer():
      x = int(x)
    if y.is_integer():
      y = int(y)
    return (x, y)

  def get_defaults(self, test:bool, seed:int, size:tuple[float, float]) -> Defaults:
    test = self.get_bool("test", test)
    seed = self.get_int("seed", seed)
    size = self.get_svg_size("size", size)
    return Defaults(test, seed, size, self.__params)


# Text Writing

def _add_text_line(line:str):
  global _text_lines, _text_indent

  _text_lines.append(f"{"  " * _text_indent}{line}")


def _open_text_indent(line:str):
  global _text_indent
  _add_text_line(line)
  _text_indent = _text_indent + 1


def _close_text_indent(line:str):
  global _text_indent

  _text_indent = max(_text_indent - 1, 0)
  _add_text_line(line)


def write_file(path:str, name:str, number:int):
  if number > 0:
    svg_name = f"{name}_{number}.svg"
  else:
    svg_name = f"{name}.svg"

  final_path = f"{path}/{svg_name}"
  f = open(final_path, "w")
  f.write(_text_content)
  f.close()
  print(f"Wrote file: {final_path}")

# SVG Management

def commit(seed:int, size:tuple[float, float], params:any):
  global _text_content
  (x, y) = size
  print_overwrite("Starting commit...")
  _open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(_svg_full.w, _svg_full.h))
  _add_text_line(f"<!-- Seed: {seed} -->")
  _add_text_line(f"<!-- Size: {x}x{y} -->")
  print_overwrite("Writing params...")
  if params is not None:
    list_params = vars(params)
    _open_text_indent("<!-- Params:")
    for item in list_params:
      _add_text_line(f"{item}: {list_params[item]}")
    _close_text_indent("-->")
  else:
    _add_text_line("<!-- No params -->")
  commit_group(_root_group)
  _close_text_indent("</svg>")
  print_overwrite("Joining output...")
  _text_content = '\n'.join(_text_lines)
  print_finish_overwite()


def commit_group(group:Group):
  if group.settings is not None:
    _open_text_indent("<g {}>".format(group.settings))
  else:
    _open_text_indent("<g>")

  len_children = len(group.children)
  for i in range(0, len_children):
    print_overwrite(f"Group {group} child: {pad_max(i + 1, len_children)}")
    child = group.children[i]
    _add_text_line(child)
  for group in group.groups:
    commit_group(group)

  _close_text_indent("</g>")


def open_group(settings: GroupSettings, parent:Group = None) -> Group:
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

def pad_max(min_val: int, max_val: int) -> str:
  str_len = len(str(max_val))
  return f"{pad_text(min_val, str_len)} / {max_val}"

def pad_text(val: any, length: int) -> str:
  string = str(val)
  str_len = len(string)
  remaining = max(length - str_len, 0)
  return f"{' ' * remaining}{string}"

def print_overwrite(string: str):
  print(f"\r{string}", end="\x1b[1K")

def print_finish_overwite():
  print("\r", end="")

# Drawing

def draw_rect(x:float, y:float, w:float, h:float, group:Group = None):
  if not group:
    group = _current_group
  x = round(x, _round_digits)
  y = round(y, _round_digits)
  w = round(w, _round_digits)
  h = round(h, _round_digits)
  group.children.append(f"<rect x=\"{x}\" y=\"{y}\" width=\"{w}\" height=\"{h}\"/>")

def draw_rect_rect(rect: Rect, group: Group = None):
  draw_rect(rect.x, rect.y, rect.w, rect.h, group)

def draw_circ(x:float, y:float, r:float, group:Group = None):
  if not group:
    group = _current_group
  x = round(x, _round_digits)
  y = round(y, _round_digits)
  r = round(r, _round_digits)
  group.children.append(f"<circle cx=\"{x}\" cy=\"{y}\" r=\"{r}\"/>")

def draw_circ_point(point: Point, r:float, group:Group = None):
  draw_circ(point.x, point.y, r, group)

def draw_path(value:str, group:Group = None):
  if not group:
    group = _current_group
  group.children.append(f"<path d=\"{value}\"/>")

def draw_border(group:Group = None):
  debug = open_group(GroupSettings(), group)
  draw_rect_rect(_svg_full, debug)
  close_group()
  red = open_group(GroupSettings(stroke=GroupColor.red), group)
  draw_rect_rect(_svg_safe, red)
  close_group()

def draw_sunburst(bursts:int, c_x:float, c_y:float, start_rad:float, ray_len:float, group:Group = None):
  sunburst_points = bursts
  for i in range(0, sunburst_points):
    t = i / sunburst_points
    rad = t * pi * 2

    x = c_x + sin(rad) * (start_rad)
    y = c_y + cos(rad) * (start_rad)

    vec = Point(x, y)
    vec = vec.subtract_copy(Point(c_x, c_y))
    vec.normalize()
    vec.multiply(ray_len)
    draw_path("M{} {} L{} {}".format(
      round(x, _round_digits),
      round(y, _round_digits),
      round(x + vec.x, _round_digits),
      round(y + vec.y, _round_digits)),
      group
    )

def draw_ring_of_circles(number:int, c_x:float, c_y:float, center_rad:float, circle_rad:float, group:Group = None):
  for i in range(0, number):
    t = i / number
    rad = t * pi * 2

    x = c_x + cos(rad) * center_rad
    y = c_y + sin(rad) * center_rad
    draw_circ(x, y, circle_rad, group)

# Main

def main(dir:str, layer: str, defaults: Defaults, seed: int, loop:callable) -> int:
  start = time.time()
  init()
  setup_size(defaults.size)

  if seed == 0:
    seed = random.randrange(maxsize)
  random.seed(seed)
  print("Seed: {}".format(seed))

  params = loop(defaults)
  commit(seed, defaults.size, params)

  export_path_file = "./dir.txt"
  if not defaults.test and not os.path.exists(export_path_file):
    print("Please specify output path in dir.txt")
    return

  # Default directory
  fullpath = f"./output/{dir}/{layer}"

  # Replace fullpath with real path if saving
  if not defaults.test:
    f = open(export_path_file, "r")
    (x, y) = defaults.size
    w = min(x, y)
    h = max(x, y)
    size_text = f"{w}x{h}"
    fullpath = f"{f.readline()}/{dir}/{layer}/{size_text}"
    f.close()

  # Make directory if necessary
  if not os.path.exists(fullpath):
    os.makedirs(fullpath)

  # Write content
  if defaults.test:
    # Only overwrite test content
    write_file(fullpath, layer, 0)
  else:
    # Write numbered content
    existing = os.listdir(fullpath)
    file_name_search = compile(r""".*?_(\d*).svg""")

    numbers: List[int] = []
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
      numbers.append(number)

    # Pick the next number in sequence
    numbers.sort()
    valid_number = 1
    for i in range(0, len(numbers)):
      next_number = numbers[i]
      if next_number > valid_number:
        break
      valid_number += 1

    write_file(fullpath, layer, valid_number)

  total_time = time.time() - start
  print("Elapsed:", timedelta(seconds=total_time))

  return seed

