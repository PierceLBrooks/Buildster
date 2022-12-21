
# Author: Pierce Brooks


from .list import List
from .native import Native


class NativeList(List):
  def __init__(self):
    super(NativeList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addNative(self, native):
    if not (isinstance(native, Native)):
      return False
    return super(NativeList, self).add(native)
    
