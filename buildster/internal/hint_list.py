
# Author: Pierce Brooks


from .list import List
from .hint import Hint


class HintList(List):
  def __init__(self):
    super(HintList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addHint(self, hint):
    if not (isinstance(hint, Hint)):
      return False
    return super(HintList, self).add(hint)
    
