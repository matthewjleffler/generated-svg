import random
import sys
import os
import re
from enum import Enum
import math

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

  def length(self):
    return math.sqrt(self.x * self.x + self.y * self.y)

  def normalize(self):
    self_len = self.length()
    self.x /= self_len
    self.y /= self_len

  def multiply(self, scale):
    self.x *= scale
    self.y *= scale

  def multiply_copy(self, scale):
    result = Point(self.x, self.y)
    result.multiply(scale)
    return result

  def subtract(self, other):
    return Point(self.x - other.x, self.y - other.y)

  def perpendicular(self):
    length = self.length()
    angle = self.angle()
    return Point( length * math.cos(angle + math.pi / 2),
                  length * math.sin(angle + math.pi / 2))

  def angle(self):
    return math.atan2(self.y, self.x)


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


# Math

def lerp(a, b, t):
  return (1 - t) * a + t * b

def ease_in_out_quad(t, b, c, d):
  return -c / 2 * (math.cos(math.pi * t / d) - 1) + b

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
  if group.settings is not None:
    open_text_indent("<g {}>".format(group.settings))
  else:
    open_text_indent("<g>")

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


def path(value):
  current_group.children.append("<path d=\"{}\"/>".format(value))


def border():
  open_group("stroke=\"red\"")
  rect(svg_safe.x, svg_safe.y, svg_safe.w, svg_safe.h)
  close_group()


def sunburst(bursts, c_x, c_y, start_rad, ray_len):
  sunburst_points = bursts
  for i in range(0, sunburst_points):
    t = i / sunburst_points
    rad = t * math.pi * 2

    x = c_x + math.sin(rad) * (start_rad)
    y = c_y + math.cos(rad) * (start_rad)

    vec = Point(x, y)
    vec = vec.subtract(Point(c_x, c_y))
    vec.normalize()
    vec.multiply(ray_len)
    path("M {} {} L{} {}".format(x, y, x + vec.x, y + vec.y))


def ring_of_circles(number, c_x, c_y, center_rad, circle_rad):
  for i in range(0, number):
    t = i / number
    rad = t * math.pi * 2

    x = c_x + math.cos(rad) * center_rad
    y = c_y + math.sin(rad) * center_rad
    circ(x, y, circle_rad)

# Letter sizes
let_h = 50
let_h_half = let_h / 2
let_h_quart = let_h / 4
let_h_eight = let_h / 8

def letter_a(x, y) -> float:
  path("M{} {}l{} {}l{} {}M{} {}h{}"
    .format(x, y, let_h_quart, -let_h, let_h_quart, let_h, x + let_h_eight, y-let_h_half, let_h_quart))
  return let_h_half

def letter_b(x, y) -> float:
  path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}m{} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, let_h_quart, 0,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))
  return let_h_half

def letter_c(x, y) -> float:
  path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_half, y, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart))
  return let_h_half

def letter_d(x, y) -> float:
  path("M{} {}v{}h{}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))
  return let_h_half

def letter_e(x, y) -> float:
  path("M{} {}h{}v{}h{}m{} {}h{}"
    .format(x + let_h_half, y, -let_h_half, -let_h, let_h_half, -let_h_half, let_h_half, let_h_quart))
  return let_h_half

def letter_f(x, y) -> float:
  path("M{} {}v{}h{}m{} {}h{}"
    .format(x, y, -let_h, let_h_half, -let_h_half, let_h_half, let_h_quart))
  return let_h_half

# TODO
def letter_g(x, y) -> float:
  path("M{} {}h{}v{} q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_quart, y - let_h_half, let_h_quart, let_h_quart,
            0, let_h_quart,  -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart))
  return let_h_half

def letter_h(x, y) -> float:
  path("M{} {}v{}m{} {}v{}m{} {}h{}"
    .format(x, y, -let_h, let_h_half, 0, let_h, 0, -let_h_half, -let_h_half))
  return let_h_half

def letter_i(x, y) -> float:
  path("M{} {}h{}m{} {}v{}m{} {}h{}"
    .format(x, y, let_h_half, -let_h_quart, 0, -let_h, -let_h_quart, 0, let_h_half))
  return let_h_half

def letter_j(x, y) -> float:
  path("M{} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_half, y - let_h, let_h_half + let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart))
  return let_h_half

def letter_k(x, y) -> float:
  path("M{} {}v{}m{} {}l{} {}l{} {}"
    .format(x, y, -let_h, let_h_half, 0, -let_h_half, let_h_half, let_h_half, let_h_half))
  return let_h_half

def letter_l(x, y) -> float:
  path("M{} {}v{}h{}"
    .format(x, y - let_h, let_h, let_h_half))
  return let_h_half

def letter_m(x, y) -> float:
  path("M{} {}v{}l{} {}l{} {}v{}"
    .format(x, y, -let_h, let_h_quart, let_h, let_h_quart, -let_h, let_h))
  return let_h_half

def letter_n(x, y) -> float:
  path("M{} {}v{}l{} {}v{}"
    .format(x, y, -let_h, let_h_half, let_h, -let_h))
  return let_h_half

def letter_o(x, y) -> float:
  path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart))
  return let_h_half

def letter_p(x, y) -> float:
  path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))
  return let_h_half

def letter_q(x, y) -> float:
  path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}m{} {}l{} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            0, -let_h_quart, let_h_quart, let_h_quart))
  return let_h_half

def letter_r(x, y) -> float:
  path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}l{} {}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, let_h_half, let_h_half))
  return let_h_half

def letter_s(x, y) -> float:
  path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart, let_h_quart))
  return let_h_half

def letter_t(x, y) -> float:
  path("M{} {}v{}m{} {}h{}"
    .format(x + let_h_quart, y, -let_h, -let_h_quart, 0, let_h_half))
  return let_h_half

def letter_u(x, y) -> float:
  path("M{} {}v{}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y - let_h, let_h_half + let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            -let_h_half - let_h_quart))
  return let_h_half

def letter_v(x, y) -> float:
  path("M{} {}l{} {}l{} {}"
    .format(x, y - let_h, let_h_quart, let_h, let_h_quart, -let_h))
  return let_h_half

def letter_w(x, y) -> float:
  path("M{} {}l{} {}l{} {}l{} {}l{} {}"
    .format(x, y - let_h,
            let_h_eight, let_h,
            let_h_eight, -let_h_half,
            let_h_eight, let_h_half,
            let_h_eight, -let_h))
  return let_h_half

def letter_x(x, y) -> float:
  path("M{} {}l{} {}m{} {}l{} {}"
    .format(x, y - let_h, let_h_half, let_h, 0, -let_h, -let_h_half, let_h))
  return let_h_half

def letter_y(x, y) -> float:
  path("M{} {}l{} {}l{} {}m{} {}v{}"
    .format(x, y - let_h, let_h_quart, let_h_half, let_h_quart, -let_h_half,
            -let_h_quart, let_h_half, let_h_half))
  return let_h_half

def letter_z(x, y) -> float:
  path("M{} {}h{}l{} {}h{}"
    .format(x + let_h_half, y, -let_h_half, let_h_half, -let_h, -let_h_half))
  return let_h_half

def number_0(x, y) -> float:
  path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}m{} {}l{} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, -let_h_quart, let_h_half, -let_h_half))
  return let_h_half

def number_1(x, y) -> float:
  path("M{} {}h{}m{} {}v{}l{} {}"
    .format(x, y, let_h_half, -let_h_quart, 0, -let_h, -let_h_quart, let_h_quart))
  return let_h_half

def number_2(x, y) -> float:
  path("M{} {}h{}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_half, y, -let_h_half, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart))
  return let_h_half

def number_3(x, y) -> float:
  path("M{} {}h{}q{} {} {} {}q{} {} {} {}h{}m{} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_eight, let_h_eight, 0,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart))
  return let_h_half

def number_4(x, y) -> float:
  path("M{} {}v{}h{}m{} {}v{}"
    .format(x, y - let_h, let_h_half, let_h_half, 0, let_h_half, -let_h))
  return let_h_half

def number_5(x, y) -> float:
  path("M{} {}h{}v{}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + let_h_half, y - let_h, -let_h_half, let_h_half, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))
  return let_h_half

def number_6(x, y) -> float:
  path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + let_h_half, y - let_h, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart))
  return let_h_half

def number_7(x, y) -> float:
  path("M{} {}h{}l{} {}"
    .format(x, y - let_h, let_h_half, -let_h_half, let_h))
  return let_h_half

def number_8(x, y) -> float:
  path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_quart, y - let_h,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart))
  return let_h_half

def number_9(x, y) -> float:
  path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart))
  return let_h_half

def draw_letter(x, y, kern, letter:callable) -> float:
  return letter(x, y) + kern

def draw_string(x, y, kern, value:str):
  value = value.upper()
  for char in value:
    if char == " ":
      x += let_h_half + kern
    elif char == "A":
      x += draw_letter(x, y, kern, letter_a)
    elif char == "B":
      x += draw_letter(x, y, kern, letter_b)
    elif char == "C":
      x += draw_letter(x, y, kern, letter_c)
    elif char == "D":
      x += draw_letter(x, y, kern, letter_d)
    elif char == "E":
      x += draw_letter(x, y, kern, letter_e)
    elif char == "F":
      x += draw_letter(x, y, kern, letter_f)
    elif char == "G":
      x += draw_letter(x, y, kern, letter_g)
    elif char == "H":
      x += draw_letter(x, y, kern, letter_h)
    elif char == "I":
      x += draw_letter(x, y, kern, letter_i)
    elif char == "J":
      x += draw_letter(x, y, kern, letter_j)
    elif char == "K":
      x += draw_letter(x, y, kern, letter_k)
    elif char == "L":
      x += draw_letter(x, y, kern, letter_l)
    elif char == "M":
      x += draw_letter(x, y, kern, letter_m)
    elif char == "N":
      x += draw_letter(x, y, kern, letter_n)
    elif char == "O":
      x += draw_letter(x, y, kern, letter_o)
    elif char == "P":
      x += draw_letter(x, y, kern, letter_p)
    elif char == "Q":
      x += draw_letter(x, y, kern, letter_q)
    elif char == "R":
      x += draw_letter(x, y, kern, letter_r)
    elif char == "S":
      x += draw_letter(x, y, kern, letter_s)
    elif char == "T":
      x += draw_letter(x, y, kern, letter_t)
    elif char == "U":
      x += draw_letter(x, y, kern, letter_u)
    elif char == "V":
      x += draw_letter(x, y, kern, letter_v)
    elif char == "W":
      x += draw_letter(x, y, kern, letter_w)
    elif char == "X":
      x += draw_letter(x, y, kern, letter_x)
    elif char == "Y":
      x += draw_letter(x, y, kern, letter_y)
    elif char == "Z":
      x += draw_letter(x, y, kern, letter_z)
    elif char == "0":
      x += draw_letter(x, y, kern, number_0)
    elif char == "1":
      x += draw_letter(x, y, kern, number_1)
    elif char == "2":
      x += draw_letter(x, y, kern, number_2)
    elif char == "3":
      x += draw_letter(x, y, kern, number_3)
    elif char == "4":
      x += draw_letter(x, y, kern, number_4)
    elif char == "5":
      x += draw_letter(x, y, kern, number_5)
    elif char == "6":
      x += draw_letter(x, y, kern, number_6)
    elif char == "7":
      x += draw_letter(x, y, kern, number_7)
    elif char == "8":
      x += draw_letter(x, y, kern, number_8)
    elif char == "9":
      x += draw_letter(x, y, kern, number_9)
    else:
      print("Unhandled character: {}".format(char))
      x += let_h_half + kern

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

  return seed

