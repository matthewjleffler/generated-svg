import importlib
import time
from lib import SvgSize, Args

###
### Test run a given script repeatedly
###

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

  while True:
    module.runner.run(defaults.test, defaults.seed, defaults.size)
    if wait <= 0:
      input("Press enter...")
    else:
      time.sleep(wait)

if __name__ == "__main__":
  run()

