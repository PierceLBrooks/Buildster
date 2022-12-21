
# Author: Pierce Brooks


from .url import URL
from .dependency import Dependency


class RemoteDependency(Dependency):
  def __init__(self, url = None):
    super(RemoteDependency, self).__init__()
    self.url = None
    if (type(url) == URL):
      self.url = url
      
  def build(self, owner, variant):
    success = super(RemoteDependency, self).build(owner, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    return True
    
  def doImport(self, label, variant):
    return True
    
  def getExports(self, variant, need):
    return {}

