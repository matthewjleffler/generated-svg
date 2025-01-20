from lib import *
from lib_node import *


class TestNodeRunner(Runner):
  def __init__(self) -> None:
    super().__init__("test_node")

  def loop(self, defaults: Defaults, group: Group):
    pad = svg_safe().copy()
    draw_border(group)

    root = Node()
    root.transform.translate(pad.x, pad.y)
    root.transform.scale(1, 1)
    root.transform.rotate_degree(45)

    offset = root.add_child()
    offset.transform.translate(100, 100)

    point = Point(0, 0)
    draw_circ_point(point, 10)

    root_transformation = root.transformation()
    root_transformed = root_transformation.apply_to_point(point)
    draw_circ_point(root_transformed, 10)

    offset_transformation = offset.transformation()
    offset_transformed = offset_transformation.apply_to_point(point)
    draw_circ_point(offset_transformed, 10)

  def run(self, defaults: Defaults) -> int:
    mainseed = main(self.dir, "main", defaults, defaults.seed, self.loop)
    return mainseed


runner = TestNodeRunner()

if __name__ == "__main__":
  args = Args()
  defaults = args.get_defaults(
    test = True,
    seed = 1,
    size = (9, 12)
  )
  runner.run(defaults)

