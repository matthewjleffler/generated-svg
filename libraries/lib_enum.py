from enum import Enum, StrEnum, IntEnum

class ReloadEnum(Enum):
  def __eq__(self, other: 'ReloadEnum'):
    if type(self).__qualname__ != type(other).__qualname__:
        return NotImplemented
    return self.name == other.name and self.value == other.value

  def __hash__(self):
      return hash((type(self).__qualname__, self.name))


class ReloadStrEnum(StrEnum):
  def __eq__(self, other: 'ReloadStrEnum'):
    if type(self).__qualname__ != type(other).__qualname__:
        return NotImplemented
    return self.name == other.name and self.value == other.value

  def __hash__(self):
      return hash((type(self).__qualname__, self.name))

class ReloadIntEnum(IntEnum):
  def __eq__(self, other: 'ReloadIntEnum'):
    if type(self).__qualname__ != type(other).__qualname__:
        return NotImplemented
    return self.name == other.name and self.value == other.value

  def __hash__(self):
      return hash((type(self).__qualname__, self.name))
