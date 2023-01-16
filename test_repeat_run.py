import sys
import importlib
import time
from lib import SvgSize

###
### Test run a given script repeatedly
###

wait_time = 0

def run():
  if len(sys.argv) < 2:
    print("Please supply a script")
    return
  module_path = sys.argv[1]
  if module_path.endswith(".py"):
    module_path = module_path.removesuffix(".py")
  module = importlib.import_module(module_path)
  if not module:
    print(f"Couldn't load module: {module_path}")

  while True:
    module.runner.run(True, 0, SvgSize.Size9x12)
    if wait_time <= 0:
      input("Press enter...")
    else:
      time.sleep(wait_time)

if __name__ == "__main__":
  run()

