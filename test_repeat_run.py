import importlib
import time
from lib import SvgSize, Args, Defaults, Runner
from lib_input import *
from enum import Enum

###
### Test run a given script repeatedly
###

#TODO test PC

_esc_code = 27

class _Result(Enum):
  Continue = 1
  Save = 2
  Quit = 3

def _save_output(runner:Runner, defaults:Defaults, lastseed:int):
  print("Saving last output...")
  runner.run(False, lastseed, defaults.size)

def _wait_on_input(key:KeyPoller) -> _Result:
  print("Press [s] to save last output, [esc] to quit, or any other key to re-run...\n")
  while True:
    char = key.poll()
    if char is not None:
      char = char.lower()
      code = ord(char)
      if char == "s":
        return _Result.Save
      elif code == _esc_code:
        return _Result.Quit
      else:
        return _Result.Continue

def _poll_after_wait(key:KeyPoller) -> _Result:
  char = key.poll()
  if char is not None:
    char = char.lower()
    code = ord(char)
    if char == "s":
      return _Result.Save
    elif code == _esc_code:
      return _Result.Quit
  return _Result.Continue

def _run_step(runner:Runner, wait:float, key:KeyPoller, current:Defaults, defaults:Defaults):
  lastseed = runner.run(current.test, current.seed, current.size)
  if wait <= 0:
    result = _wait_on_input(key)
    if result == _Result.Save:
      print("Saving last output...")
      return (Defaults(False, lastseed, current.size), False)
    elif result == _Result.Quit:
      return (defaults, True)
    else:
      return (defaults, False)
  else:
    print("") # Empty line between runs
    time.sleep(wait)
    result = _poll_after_wait(key)
    if result == _Result.Save:
      print("Saving last output...")
      return (Defaults(False, lastseed, current.size), False)
    elif result == _Result.Quit:
      return (defaults, True)
    else:
      return (defaults, False)

def run():
  args = Args()

  if args.positional_count() < 1:
    print("Please supply a script")
    return
  module_path = args.positional_str(0)
  if module_path.endswith(".py"):
    module_path = module_path.removesuffix(".py")
  module = importlib.import_module(module_path)
  if not module:
    print(f"Couldn't load module: {module_path}")

  defaults = args.get_defaults(True, 0, SvgSize.Size9x12)
  wait = args.get_float("wait", 0)

  with KeyPoller() as key:
    current = defaults
    while True:
      result = _run_step(module.runner, wait, key, current, defaults)
      current = result[0]
      quit = result[1]
      if quit:
        print("Escape pressed.")
        return



if __name__ == "__main__":
  run()

