import random
import math
import sys
import os
import re

# Setup Variables

file_name = "template"
test = True # Whether or not to rewrite the test file only
seed = 0 # Whether or not to use a set seed

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


def write_file(number):
  if number > 0:
    svg_name = "{}_{}.svg".format(file_name, number)
  else:
    svg_name = "{}.svg".format(file_name)

  f = open("./{}".format(svg_name), "w")
  f.write(text_content)
  f.close()
  print("Wrote file: {}".format(svg_name))


def rect(x, y, w, h, color = "black"):
  add_text_line("<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\" stroke=\"{}\" fill-opacity=\"0\"/>".format(x, y, w, h, color))

def rect_safe(x, y, w, h, color = "black"):
  rect(x + svg_border, y + svg_border, w, h, color)

# Image Specific Content

def loop():

  # Border
  rect_safe(0, 0, svg_safe_width, svg_safe_height, "red")


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
