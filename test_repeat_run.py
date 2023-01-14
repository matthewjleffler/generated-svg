import sys
import importlib
import time

###
### Test run a given script repeatedly
###

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
    module.run()
    time.sleep(1)

if __name__ == "__main__":
  run()

