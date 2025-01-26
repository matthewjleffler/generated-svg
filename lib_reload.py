from importlib import reload


# Reloads imported libs for a module
def reload_libs(globals: dict[str, any]) -> None:
  for key, val in globals.items():
    if not key.startswith("build") and not key.startswith("impl"):
      continue
    reload(val)
