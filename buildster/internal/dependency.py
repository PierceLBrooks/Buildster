
# Author: Pierce Brooks

import os

from .build import Build
from .path import Path
from .label import Label
from .export_list import ExportList
from .import_list import ImportList
from .build_instruction import BuildInstruction

from .utilities import *

class Dependency(Build):
  def __init__(self, subpath = None, label = None, instruction = None, imports = None, exports = None):
    super(Dependency, self).__init__()
    self.subpath = None
    if (type(subpath) == Path):
      self.subpath = subpath
    self.label = None
    if (type(label) == Label):
      self.label = label
    self.instruction = None
    if (type(instruction) == BuildInstruction):
      self.instruction = instruction
    self.imports = None
    if (type(imports) == ImportList):
      self.imports = imports
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
    
  def build(self, owner, variant):
    success = True
    if not (self.imports == None):
      success = self.imports.doImport(self, variant)
    if not (success):
      return False
    if not (self.exports == None):
      success = self.exports.doExport(self, variant)
    if not (success):
      return False
    success = super(Dependency, self).build(owner, variant)
    if not (success):
      return False
    return True
    
  def distribute(self, owner, distribution, variant):
    context = owner.getContext()
    exports = self.getExports(variant, self)
    if not (type(exports) == dict):
      return False
    for key in exports:
      export = exports[key]
      if (export[0] == "libraries"):
        if (os.path.isdir(export[1])):
          for root, folders, files in os.walk(export[1]):
            for name in files:
              if (context.exclude(name)):
                continue
              if not (self.move(os.path.join(root, name).replace("\\", "/"), os.path.join(distribution, variant.lower(), name).replace("\\", "/"))):
                return False
        elif (os.path.isfile(export[1])):
          if not (os.path.exists(os.path.join(distribution, variant.lower(), os.path.basename(export[1])))):
            if not (move(export[1].replace("\\", "/"), os.path.join(distribution, variant.lower(), os.path.basename(export[1])).replace("\\", "/"))):
              return False
          if (os.path.isdir(os.path.dirname(export[1]))):
            for root, folders, files in os.walk(os.path.dirname(export[1])):
              for name in files:
                if (context.exclude(name)):
                  continue
                if not (self.move(os.path.join(root, name).replace("\\", "/"), os.path.join(distribution, variant.lower(), name).replace("\\", "/"))):
                  return False
      elif (export[0] == "all"):
        if (os.path.isdir(export[1])):
          if (os.path.isdir(os.path.join(export[1], "bin"))):
            for root, folders, files in os.walk(os.path.join(export[1], "bin")):
              for name in files:
                if (context.exclude(name)):
                  continue
                if not (self.move(os.path.join(root, name).replace("\\", "/"), os.path.join(distribution, variant.lower(), name).replace("\\", "/"))):
                  return False
          if (os.path.isdir(os.path.join(export[1], "lib"))):
            for root, folders, files in os.walk(os.path.join(export[1], "lib")):
              for name in files:
                if (context.exclude(name)):
                  continue
                if not (self.move(os.path.join(root, name).replace("\\", "/"), os.path.join(distribution, variant.lower(), name).replace("\\", "/"))):
                  return False
    return True
    
  def getPath(self, owner, variant, purpose):
    return adjust(os.path.join(wd(), owner.getContext().root.directory.getContent(), owner.directory.getContent(), purpose, "dependencies", self.label.getContent()))
    
  def getLabel(self):
    return self.label.getContent()
    
  def doExport(self, key, value, export, variant, exceptions):
    return True
    
  def doImport(self, label, variant):
    return True
    
  def getExports(self, variant, need):
    return {}

