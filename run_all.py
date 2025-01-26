from lib import Args
from os import listdir
from typing import List
import importlib


def _remove_suffix(input_string:str, suffix:str) -> str:
  if suffix and input_string.endswith(suffix):
      return input_string[:-len(suffix)]
  return input_string

def run():
  print("Running all SVG scripts...")

  args = Args()
  defaults = args.get_defaults(True, 0, (9, 12))

  scripts = listdir('.')
  module_paths: List[str] = []
  for script in scripts:
    if not script.startswith("svg_"):
      continue
    if not script.endswith(".py"):
      continue
    script = _remove_suffix(script, ".py")
    module_paths.append(script)

  module_paths = sorted(module_paths)

  run: List[str] = []
  skipped: List[str] = []
  for path in module_paths:
    module = importlib.import_module(path)
    if not module:
      print(f"Couldn't load module: {path}")
      skipped.append(path)
      continue
    if not module.runner:
      print(f"No Runner present in {path}")
      skipped.append(path)
      continue
    print(f"\nRunning {path}")
    run.append(path)
    module.runner.run(defaults)

  print(f"\nFinished running {len(run)} script(s)")
  for val in run:
    print(f"  {val}")
  print(f"\nSkipped {len(skipped)} script(s)")
  for val in skipped:
    print(f"  {val}")


if __name__ == "__main__":
  run()
