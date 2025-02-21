import random
import time
from datetime import timedelta
from sys import maxsize, argv
import os
from os import listdir
from libraries.lib_group import *
from re import compile
from math import *
from typing import List, TypedDict
import datetime
from libraries.lib_draw import *
from libraries.lib_rand import *
from libraries.lib_math import *
from libraries.lib_reload import *
from libraries.lib_path import *
from libraries.lib_text import *
from libraries.lib_node import *
from libraries.lib_poly import *
from libraries.lib_enum import *


###
### Core SVG Drawing Library
###

# Helper functions

def clamp_point_list(clamp_val:int, points:List[Point]):
  for point in points:
    point.x = round(point.x / clamp_val, 0) * clamp_val
    point.y = round(point.y / clamp_val, 0) * clamp_val

def create(dict: dict) -> any:
  return type('', (), dict)

def test_type(obj: any, expected: str) -> bool:
  return type(obj).__name__ == expected

def apply_defaults[T](params: dict[str, any], defaults: 'Defaults') -> T:
  if defaults.test:
    # Nothing to apply
    return params
  print("Disabling debug params")
  for k, v in params.items():
    if k.startswith("debug_") and test_type(v, "bool"):
      params[k] = False
  return params

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
_root_group = Group(None, GroupSettings(name="root", stroke=GroupColor.black, fill=GroupColor.none))
_group_count = 0
_groups: dict[str, Group] = dict()
_pixel_per_inch = 95.8


def init():
  global _svg_full, _svg_safe, _svg_border, _text_indent, _text_content, _font_styles, _root_group, _text_lines, _groups, _group_count

  _svg_full = Rect(0, 0, 0, 0)
  _svg_safe = Rect(0, 0, 0, 0)
  _svg_border = 50
  _text_indent = 0
  _text_lines = []
  _text_content = ""
  _font_styles = dict()
  _root_group = Group(None, GroupSettings(name="root", stroke=GroupColor.black, fill=GroupColor.none))
  _group_count = 0
  _groups = dict()


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
  def __init__(self, test:bool, seed:int, size:tuple[float, float]) -> None:
    self.test:bool = test
    self.seed:int = seed
    self.size:tuple[float, float] = size
    self.throw_on_fail:bool = False

  def copy(self) -> 'Defaults':
    result = Defaults(self.test, self.seed, self.size)
    result.throw_on_fail = self.throw_on_fail
    return result


class Runner:
  def __init__(self, dir:str) -> None:
    self.dir = dir

  def run(self, defaults: Defaults) -> int:
    return 0


class Args:
  def __init__(self) -> None:
    self.__positional = []
    self.__args: dict[str] = dict()

    parse = compile(r"""--(.*?)=(.*)""")
    for i in range(1, len(argv)):
      arg = argv[i]
      parsed = parse.match(arg)
      if parsed is None:
        self.__positional.append(arg)
      elif parsed is not None:
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
    return Defaults(test, seed, size)


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

def commit(seed:int, size:tuple[float, float], params:dict):
  global _text_content
  (x, y) = size
  print_overwrite("Starting commit...")
  _open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(_svg_full.w, _svg_full.h))
  _add_text_line(f"<!-- Seed: {seed} -->")
  _add_text_line(f"<!-- Size: {x}x{y} -->")
  print_overwrite("Writing params...")
  if params is not None:
    _open_text_indent("<!-- Params:")
    for k, v in params.items():
      _add_text_line(f"{k}: {v}")
    _close_text_indent("-->")
  else:
    _add_text_line("<!-- No params -->")
  commit_group(_root_group)
  _close_text_indent("</svg>")
  print_overwrite("Joining output...")
  _text_content = '\n'.join(_text_lines)
  print_finish_overwite()


def commit_group(group:Group):
  if group.settings is not None and group.settings != "":
    _open_text_indent(f"<g {group.settings}> <!-- {group.name} -->")
  else:
    _open_text_indent(f"<g> <!-- {group.name} -->")

  len_children = len(group.children)
  for i in range(0, len_children):
    print_overwrite(f"Group '{group.name}' child: {pad_max(i + 1, len_children)}")
    child = group.children[i]
    _add_text_line(child)
  for group in group.groups:
    commit_group(group)

  _close_text_indent("</g>")


def open_group(settings: GroupSettings, parent: Group) -> Group:
  global _group_count

  original_name = settings.name
  if original_name is not None:
    existing = _groups.get(settings.name, None)
    if existing is not None:
      return existing
  else:
    _group_count += 1
    settings.name = f"group_{_group_count}"

  new_group = Group(parent, settings)
  parent.groups.append(new_group)
  if original_name is not None:
    _groups[settings.name] = new_group

  return new_group


def pad_max(min_val: int, max_val: int) -> str:
  str_len = len(str(max_val))
  percent = floor((min_val / max_val) * 100)
  return f"{pad_text(min_val, str_len)} / {max_val} ({percent}%)"

def pad_text(val: any, length: int) -> str:
  string = str(val)
  str_len = len(string)
  remaining = max(length - str_len, 0)
  return f"{' ' * remaining}{string}"

def print_overwrite(string: str):
  print(f"\r{string}", end="\x1b[1K")

def print_finish_overwite():
  print("\r", end="")

def draw_border(group:Group):
  debug = open_group(GroupSettings(name="debug"), _root_group)
  draw_rect_rect(_svg_full, debug)
  red = open_group(GroupSettings(name="debug_red", stroke=GroupColor.red), _root_group)
  draw_rect_rect(_svg_safe, red)


# Common log for repeat output
class RunningLog:
  def __init__(self, label: str, max_val: int, count: bool = True, freq: int = 1):
    self.__label = label
    self.__max_val = max_val
    self.__start = self.__last = time.time()
    self.__count = count
    self.__freq = freq
    self.__time_deltas = []
    self.__time_total_count = 1000

  def log(self, current: int) -> None:
    time_remaining_estimate = ""
    if self.__count:
      now = time.time()
      total_time = now - self.__start
      self.__time_deltas.append(now - self.__last)
      self.__last = now
      avg_time = 0
      len_avg = len(self.__time_deltas)
      for delta in self.__time_deltas:
        avg_time += delta
      avg_time /= len_avg
      if len_avg == self.__time_total_count:
        self.__time_deltas.pop(0)
      total_estimate = max((avg_time * self.__max_val) - total_time, 0)
      time_remaining_estimate = str(datetime.timedelta(seconds=floor(total_estimate)))
    if current % self.__freq == 0:
      print_overwrite(f"{self.__label}: {pad_max(current, self.__max_val)} {time_remaining_estimate}")


# Main

def main(dir:str, layer: str, defaults: Defaults, seed: int, loop:callable) -> int:
  start = time.time()
  init()
  setup_size(defaults.size)

  if seed == 0:
    seed = random.randrange(maxsize)
  random.seed(seed)
  print("Seed: {}".format(seed))

  try:
    params = loop(defaults, _root_group, seed)
  except Exception as e:
    if defaults.throw_on_fail:
      raise
    print('An error occurred when running the script')
    print(e)
    return seed

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
    existing = listdir(fullpath)
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

