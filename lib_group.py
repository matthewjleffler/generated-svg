from enum import StrEnum
from typing import List
from lib_math import Point


class GroupColor(StrEnum):
  black = 'black'
  blue = 'blue'
  red = 'red'
  green = 'green'
  none = 'none'


class GroupSettings:
  def __init__(
      self,
      stroke: str = None,
      fill: str = None,
      translate: tuple[float, float] = None,
      translatePoint: Point = None,
      scale: float = None,
      scaleXY: tuple[float, float] = None,
      scalePoint: Point = None,
      rotate: float = None,
      name: str = None
  ):
    self.name = name
    settings: List[str] = []

    if stroke is not None:
      settings.append(f"stroke=\"{stroke}\"")

    if fill is not None:
      settings.append(f"fill=\"{fill}\"")

    transforms: List[str] = []

    if translate is not None:
      transforms.append(f"translate({translate[0]}, {translate[1]})")
    elif translatePoint is not None:
      transforms.append(f"translate({translatePoint.x}, {translatePoint.y})")

    if scale is not None:
      transforms.append(f"scale({scale}, {scale})")
    elif scaleXY is not None:
      transforms.append(f"scale({scaleXY[0]}, {scaleXY[1]})")
    elif scalePoint is not None:
      transforms.append(f"scale({scalePoint.x}, {scalePoint.y})")

    if rotate is not None:
      transforms.append(f"rotate({rotate})")

    if len(transforms) > 0:
      settings.append(f"transform=\"{' '.join(transforms)}\"")

    self.settings = ""
    if len(settings) > 0:
      self.settings = ' '.join(settings)


class Group:
  def __init__(self, parent: 'Group', settings: GroupSettings):
    self.parent = parent
    self.settings = settings.settings
    self.groups = []
    self.children = []
    self.name = settings.name

