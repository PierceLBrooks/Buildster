
# Author: Pierce Brooks


from .list import List
from .parent import Parent


class ParentList(List):
  def __init__(self):
    super(ParentList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addParent(self, parent):
    if not (isinstance(parent, Parent)):
      return False
    return super(ParentList, self).add(parent)
    
