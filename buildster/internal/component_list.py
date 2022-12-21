
# Author: Pierce Brooks


from .list import List
from .component import Component


class ComponentList(List):
  def __init__(self):
    super(ComponentList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addComponent(self, component):
    if not (isinstance(component, Component)):
      return False
    return super(ComponentList, self).add(component)
    
