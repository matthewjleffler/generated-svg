import random
import sys
import os
import re
from enum import Enum

# Setup Variables

svg_width = svg_height = svg_safe_width = svg_safe_height = 0
svg_left = svg_top = svg_right = svg_bottom = 0
svg_border = 50
text_indent = 0
text_content = ""


# Widths

class SvgSize(Enum):
  SizeA3 = 1,
  Size9x12 = 2,


def setup_size(size:SvgSize):
  global svg_width, svg_height, svg_safe_width, svg_safe_height
  global svg_left, svg_top, svg_right, svg_bottom

  if size is SvgSize.SizeA3:
    svg_width = 1550
    svg_height = 950
  elif size is SvgSize.Size9x12:
    svg_width = 1150
    svg_height = 870

  svg_left = svg_top = svg_border
  svg_right = svg_width - svg_border
  svg_bottom = svg_height - svg_border
  svg_safe_width = svg_right - svg_left
  svg_safe_height = svg_bottom - svg_top


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

  f = open("./{}".format(svg_name), "w")
  f.write(text_content)
  f.close()
  print("Wrote file: {}".format(svg_name))

# Shapes

def rect(x, y, w, h, color = "black"):
  add_text_line("<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\" stroke=\"{}\" fill-opacity=\"0\"/>".format(x, y, w, h, color))

def rect_safe(x, y, w, h, color = "black"):
  rect(x + svg_border, y + svg_border, w, h, color)

# Main

def main(name: str, test: bool, seed:int, size:SvgSize, loop:callable):
  setup_size(size)

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
    write_file(name, 0)
  else:
    # Write numbered content
    # Consume existing file names
    max_number = 0
    existing = os.listdir(".")

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

