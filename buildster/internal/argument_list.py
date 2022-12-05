
# Author: Pierce Brooks


from .list import List
from .argument import Argument


class ArgumentList(List):
  def __init__(self):
    super(ArgumentList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addArgument(self, argument):
    if not (isinstance(argument, Argument)):
      return False
    return super(ArgumentList, self).add(argument)
    
