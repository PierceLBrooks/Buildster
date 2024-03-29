
# Author: Pierce Brooks

import os
import shlex

from .build_instruction import BuildInstruction

from .utilities import *

class CommandBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(CommandBuildInstruction, self).__init__(arguments)
    self.string = None
    self.extracts = []
    self.copies = []
    self.deletes = []
    self.writes = []
    self.setters = []
    self.downloads = []
    
  def build(self, owner, path, subpath, installation, imports, variant):
    mature = False
    try:
      if not (os.path.isdir(subpath)):
        if (contains(wd(), subpath)):
          os.makedirs(subpath)
    except:
      pass
    if not (len(self.extracts) == 0):
      for i in range(len(self.extracts)):
        extract = self.extracts[i]
        if (extract == None):
          continue
        if not (extract.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.copies) == 0):
      for i in range(len(self.copies)):
        copy = self.copies[i]
        if (copy == None):
          continue
        if not (copy.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.deletes) == 0):
      for i in range(len(self.deletes)):
        delete = self.deletes[i]
        if (delete == None):
          continue
        if not (delete.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.writes) == 0):
      for i in range(len(self.writes)):
        wrote = self.writes[i]
        if (wrote == None):
          continue
        if not (wrote.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.setters) == 0):
      for i in range(len(self.setters)):
        setter = self.setters[i]
        if (setter == None):
          continue
        if not (setter.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.downloads) == 0):
      for i in range(len(self.downloads)):
        download = self.downloads[i]
        if (download == None):
          continue
        if not (download.perform(owner.getContext())):
          return False
      mature = True
    if (mature):
      return True
    if (self.string == None):
      return False
    command = self.string.getContent().strip()
    if (len(command) == 0):
      return True
    command = shlex.split(self.string.getContent().replace("\\", "/"))
    owner.getContext().log(self.node, self.string.getContent())
    owner.getContext().log(self.node, str(command))
    owner.getContext().log(self.node, subpath)
    cwd = os.getcwd()
    os.chdir(subpath)
    result = execute_command(command, owner.getContext().environment)
    os.chdir(cwd)
    #owner.getContext().log(self.node, result)
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.string)+", "+self.toString(self.extracts)+", "+self.toString(self.copies)+", "+self.toString(self.deletes)+", "+self.toString(self.writes)+", "+self.toString(self.setters)+">"
    
