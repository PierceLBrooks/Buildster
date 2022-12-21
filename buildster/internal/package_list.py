
# Author: Pierce Brooks


from .list import List
from .package import Package


class PackageList(List):
  def __init__(self):
    super(PackageList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addPackage(self, package):
    if not (isinstance(package, Package)):
      return False
    return super(PackageList, self).add(package)
    
