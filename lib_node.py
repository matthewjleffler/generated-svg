from lib_matrix import *

### Scene graph node

class Node:
  def __init__(self):
    self.transform = Matrix()
    self._children: List[Node] = []
    self._parent: Node = None

  def add_child(self, other: 'Node') -> 'Node':
    other._parent = self
    self._children.append(other)
    return other

  def transformation(self) -> 'Matrix':
    parents: List[Node] = []
    node = self
    while node is not None:
      parents.insert(0, node)
      node = node._parent
    result = Matrix()
    for parent in parents:
      result.multiply(parent.transform)
    return result
