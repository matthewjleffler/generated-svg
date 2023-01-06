import lib
import text
import os
import random
from typing import List

text_file = "" # Specific override text file

def loop():
  # lib.border()

  global text_file

  # Find text file if we don't have one assigned
  if text_file == "":
    # List content of text dir
    files = os.listdir("./text-content")
    valid_files: List[str] = []
    for file in files:
      if file.endswith(".txt"):
        valid_files.append(file)

    if len(valid_files) > 0:
      valid_index = random.randint(0, len(valid_files) - 1)
      text_file = valid_files[valid_index]

  if text_file == "":
    print("No text file")
    return

  # Load content
  print(f"Loading: {text_file}")
  text_lines = []
  with open(f"./text-content/{text_file}") as f:
    text_lines = f.readlines()

  # Prune empty lines
  pruned = 0
  text_len = len(text_lines)
  while text_len > 0:
    text_len -= 1
    line = text_lines[text_len]
    if line.isspace():
      pruned += 1
      text_lines.pop(text_len)

  text_len = len(text_lines)
  print(f"Pruned {pruned} line(s), {text_len} line(s) remain.")

  if text_len < 1:
    print(f"No content loaded")
    return

  # Setup variables
  min_lines = 5
  max_lines = 15
  num_lines = random.randint(min_lines, max_lines)
  num_lines = min(num_lines, text_len)

  # Pick lines
  last_index = max(text_len - 1 - num_lines, 0)
  random_line_index = 0
  if last_index > 0:
    random_line_index = random.randint(0, text_len - 1)

  # Collect picked lines
  render_lines: List[str] = []
  max_len = 0
  for i in range(random_line_index, random_line_index + num_lines):
    line = text_lines[i].strip()
    max_len = max(len(line) + 3, max_len)
    render_lines.append(line)

  # Add ellipses to beginning and end
  render_lines[0] = f"...{render_lines[0]}"
  render_lines[-1] = f"{render_lines[-1]}..."

  # Calculate width and height of the content we found
  max_w = max_len * text.let_h_half + (max_len - 1) * 10
  scale = lib.svg_safe.w / max_w
  line_num = len(render_lines)
  height = line_num * text.line_height * scale

  # Draw text
  lib.open_group(f"transform=\"translate({lib.svg_safe.x}, {lib.svg_safe.center_y() - height / 2}) scale({scale}, {scale})\"")

  for i in range(0, line_num):
    line = render_lines[i]
    text.draw_string(0, text.line_height * (i + 1), 10, line)

  lib.close_group()

seed = 0
test = True
size = lib.SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = lib.main("text-strings", test, seed, size, loop)
