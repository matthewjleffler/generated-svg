import random
import math
import sys
import os
import re

# Setup Variables

file_name = "template"

# Widths:
# A3(?) 1550 x 950
# 9x12 1150 x 870

svg_width = 1150
svg_height = 870

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


def rect(x, y, w, h, color = "black"):
  add_text_line("<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\" stroke=\"{}\" fill-opacity=\"0\"/>".format(x, y, w, h, color))


# Image Specific Content

def loop():
  global svg_width, svg_height

  # Border
  rect(50, 50, svg_width-100, svg_height-100, "red")


# Main

def main():
  global text_content, svg_width, svg_height

  seed = random.randrange(sys.maxsize)
  # seed = 1551311739248735356
  random.seed(seed)

  open_text_indent("<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\">".format(svg_width, svg_height))

  add_text_line("<!-- Seed: {} -->".format(seed))

  loop()
  close_text_indent("</svg>")
  # print(text_content)

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

  # Create file name and write file
  svg_name = "{}_{}.svg".format(file_name, min_available_number)
  f = open("./{}".format(svg_name), "w")
  f.write(text_content)
  f.close()
  print("Wrote file: {}".format(svg_name))


if __name__ == "__main__":
  main()
