import random
from typing import List, TypeVar
T = TypeVar('T')
Weights = List[tuple[T, float]]

###
### Random Lib
###

class RangeInt:
  def __init__(self, min_val:int, max_val:int):
    self._min_val = min_val
    self._max_val = max_val

  def __repr__(self) -> str:
    return f"[RangeInt] min: {self._min_val} max: {self._max_val}"

  def rand(self) -> int:
    return rand_int(self._min_val, self._max_val)


class RangeFloat:
  def __init__(self, min_val:float, max_val:float):
    self._min_val = min_val
    self._max_val = max_val

  def __repr__(self) -> str:
    return f"[RangeFloat] min: {self._min_val} max: {self._max_val}"

  def rand(self) -> float:
    return rand_float(self._min_val, self._max_val)


# Random

def rand() -> float:
  return random.random()

def rand_bool() -> bool:
  return rand_int(0, 1) == 0

def rand_float(min:float, max:float) -> float:
  delta = max - min
  return min + random.random() * delta

def rand_int(min:int, max:int) -> int:
  return random.randint(min, max)

def rand_weight[T](array: Weights[T]) -> T:
  if len(array) < 1:
    return None
  sum = 0
  for (_, weight) in array:
    sum += weight
  rand = random.random() * sum
  for (item, weight) in array:
    rand -= weight
    if rand <= 0:
      return item
  print("Error in weighted randomness")
  return None