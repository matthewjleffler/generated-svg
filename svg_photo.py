from lib import *
import impl.impl_photo as impl


class PhotoRunner(Runner):
  def __init__(self) -> None:
    super().__init__("photo")

  def loop(self, defaults: Defaults, group: Group, seed: int):
    params = impl.CreateParams(defaults)
    impl.draw_photo(params, group, seed)
    return params

  def run(self, defaults: Defaults) -> int:
    reload_libs(globals())
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = PhotoRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 0,
    size = (9, 12)
  )
  runner.run(defaults)

