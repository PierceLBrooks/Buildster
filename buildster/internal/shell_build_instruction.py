
# Author: Pierce Brooks


from .build_instruction import BuildInstruction


class ShellBuildInstruction(BuildInstruction):
  def __init__(self, commands = None, work = None):
    super(ShellBuildInstruction, self).__init__()
    self.commands = None
    self.work = None
      
  def build(self, owner, path, subpath, installation, imports, variant):
    if (self.commands == None):
      return False
    if not ("CommandsBuildInstruction" in str(type(self.commands))):
      return False
    if (self.work == None):
      return False
    if not ("Work" in str(type(self.work))):
      return False
    owner.getContext().work = self.work.getContent()
    if not (self.commands.build(owner, self.getPath(path, subpath), self.work.getContent(), installation, imports, variant)):
      return False
    owner.getContext().work = None
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.commands)+">"

