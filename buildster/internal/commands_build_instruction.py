
# Author: Pierce Brooks


from .build_instruction import BuildInstruction


class CommandsBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(CommandsBuildInstruction, self).__init__(arguments)
    self.commands = []
      
  def build(self, owner, path, subpath, installation, imports, variant):
    length = len(self.commands)
    for i in range(length):
      if ("CommandBuildInstruction" in str(type(self.commands[i]))):
        if not (self.commands[i].build(owner, path, subpath, installation, imports, variant)):
          return False
      else:
        owner.getContext().log(self.node, str(type(self.commands[i])))
        return False
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.commands)+">"
    
