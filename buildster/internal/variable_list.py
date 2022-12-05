
# Author: Pierce Brooks


from .list import List
from .variable import Variable


class VariableList(List):
  def __init__(self):
    super(VariableList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addVariable(self, variable):
    if not (isinstance(variable, Variable)):
      return False
    return super(VariableList, self).add(variable)
    
