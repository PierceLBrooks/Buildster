
# Author: Pierce Brooks


from .list import List
from .namespace import Namespace


class NamespaceList(List):
  def __init__(self):
    super(NamespaceList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addNamespace(self, namespace):
    if not (isinstance(namespace, Namespace)):
      return False
    return super(NamespaceList, self).add(namespace)
    
