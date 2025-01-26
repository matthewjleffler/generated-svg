import importlib
import time
from lib import Args, Defaults, Runner
from libraries.lib_input import *
from enum import Enum


###
### Test run a given script repeatedly
###

_esc_code = 27
_lock_seed = False
_last_seed = 0

class __Input(Enum):
  Continue = 1
  Save = 2
  Quit = 3
  LockSeed = 4


class __Result:
  def __init__(self, current: Defaults, quit: bool, run_next: bool):
    self.current = current
    self.quit = quit
    self.run_next = run_next


def _remove_suffix(input_string:str, suffix:str) -> str:
  if suffix and input_string.endswith(suffix):
      return input_string[:-len(suffix)]
  return input_string

def _wait_on_input(key:KeyPoller) -> __Input:
  print("Press [s] to save last output, [esc] to quit, [l] to un/lock seed, or any other key to re-run...\n")
  while True:
    char = key.poll()
    if char is not None:
      char = char.lower()
      code = ord(char)
      if char == "s":
        return __Input.Save
      if char == "l":
        return __Input.LockSeed
      elif code == _esc_code:
        return __Input.Quit
      else:
        return __Input.Continue


def _run_step(
    runner: Runner,
    key: KeyPoller,
    current: Defaults,
    defaults: Defaults,
    run_next: bool
  ) -> __Result:
  global _lock_seed, _last_seed

  if run_next:
    _last_seed = runner.run(current)

  keypress = _wait_on_input(key)
  if keypress == __Input.Save:
    print("Saving last output...")
    return __Result(Defaults(False, _last_seed, current.size, current.params), False, True)

  elif keypress == __Input.Quit:
    return __Result(None, True, False)

  elif keypress == __Input.LockSeed:
    if _lock_seed:
      _lock_seed = False
      print("Unlocked seed")
    else:
      _lock_seed = True
      print(f"Locked seed: {_last_seed}")

    next_defaults = defaults.copy()
    if _lock_seed:
      next_defaults.seed = _last_seed
    return __Result(next_defaults, False, False)

  else:
    next_defaults = defaults.copy()
    if _lock_seed:
      next_defaults.seed = _last_seed
    return __Result(next_defaults, False, True)

def run():
  args = Args()

  if args.positional_count() < 1:
    print("Please supply a script")
    return

  if args.positional_str(0).endswith('?'):
    print('\nUsage: python run_repeat.py [script_name.py]')
    print('  Args:')
    print('    size:       --size=[w]x[h]')
    print('    seed:       --seed=[seed]')
    print('    test:       --test=[true/t]')
    print('  Params:')
    print('    int/float:  ++[param name]=[val]')
    print('    bool:       ++[param name]=[t/true/f/false]')
    print('    RangeInt:   ++[param name]=ri:[min]:[max]')
    print('    RangeFloat: ++[param name]=rf:[min]:[max]')
    print('    weight:     ++[param name]=w:[val,weight]:[val,weight]:...')
    print('')
    return

  module_path = args.positional_str(0)
  if module_path.endswith(".py"):
    module_path = _remove_suffix(module_path, ".py")
  if module_path.startswith(".\\"):
    module_path = module_path[2:len(module_path)]
  module = importlib.import_module(module_path)
  if not module:
    print(f"Couldn't load module: {module_path}")
    return

  defaults = args.get_defaults(True, 0, (9, 12))

  with KeyPoller() as key:
    current = defaults
    run_next = True
    while True:
      module = importlib.reload(module)
      result = _run_step(module.runner, key, current, defaults, run_next)
      current = result.current
      run_next = result.run_next
      if result.quit:
        print("Escape pressed.")
        return


if __name__ == "__main__":
  run()

