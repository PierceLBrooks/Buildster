
# Author: Pierce Brooks


from .list import List
from .functor import Functor


class FunctorList(List):
  def __init__(self):
    super(FunctorList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addFunctor(self, functor):
    if not (isinstance(functor, Functor)):
      return False
    return super(FunctorList, self).add(functor)
    
