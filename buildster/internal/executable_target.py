
# Author: Pierce Brooks


from .target import Target


class ExecutableTarget(Target):
  def __init__(self, label = None, definitions = None, links = None, imports = None):
    super(ExecutableTarget, self).__init__(label, definitions, links, imports)
    self.exportsContent = {}
    self.importsContent = {}
    
  def build(self, owner, variant):
    success = super(ExecutableTarget, self).build(owner, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    if (key in self.exportsContent[variant]):
      return False
    self.exportsContent[variant][key] = [export, value, exceptions]
    return True
    
  def doImport(self, label, variant):
    if not (variant in self.importsContent):
      self.importsContent[variant] = []
    if (label in self.importsContent[variant]):
      return False
    self.importsContent[variant].append(label)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.definitions)+", "+self.toString(self.links)+", "+self.toString(self.imports)+", "+self.toString(self.arguments)+", "+self.toString(self.packages)+", "+self.toString(self.modules)+">"
    
