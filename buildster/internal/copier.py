
# Author: Pierce Brooks

import os
import fnmatch

from .performer import Performer
from .copier_source import CopierSource
from .copier_destination import CopierDestination
from .copier_rename import CopierRename

from .utilities import *

class Copier(Performer):
  def __init__(self, source = None, destination = None, rename = None):
    super(Copier, self).__init__()
    self.source = None
    self.destination = None
    self.rename = None
    if (type(source) == CopierSource):
      self.source = string
    if (type(destination) == CopierDestination):
      self.destination = destination
    if (type(rename) == CopierRename):
      self.rename = rename
      
  def perform(self, context):
    if ((self.source == None) or (self.destination == None)):
      return False
    context.log(None, "Copying from \""+self.source.getContent().strip()+"\" to \""+self.destination.getContent().strip()+"\"...")
    source = self.source.getContent().strip()
    destination = self.destination.getContent().strip()
    rename = None
    if not (self.rename == None):
      rename = self.rename.getContent().strip()
    if ((os.path.isdir(source)) or ((os.path.isdir(os.path.join(str(context.work), source))) and not (context.work == None))):
      if not (os.path.isdir(source)):
        source = os.path.join(context.work, source)
      check = os.path.isdir(destination)
      names = []
      for root, folders, files in os.walk(source):
        for name in folders:
          names.append(os.path.join(root, name))
        for name in files:
          temp = None
          if (rename == None):
            if not (check):
              temp = os.path.join(destination, name)
            else:
              temp = os.path.join(destination, os.path.basename(os.path.abspath(source)), name)
          else:
            temp = os.path.join(destination, rename, name)
          if (os.path.exists(temp)):
            continue
          if not (move(os.path.join(root, name), temp, context, rename)):
            return False
        break
      for folder in names:
        for root, folders, files in os.walk(folder):
          for name in files:
            temp = None
            if (rename == None):
              if not (check):
                temp = os.path.join(destination, os.path.basename(folder), os.path.relpath(root, folder), name)
              else:
                temp = os.path.join(destination, os.path.basename(os.path.abspath(source)), os.path.basename(folder), os.path.relpath(root, folder), name)
            else:
              temp = os.path.join(destination, rename, os.path.basename(folder), os.path.relpath(root, folder), name)
            if (os.path.exists(temp)):
              continue
            if not (move(os.path.join(root, name), temp, context, rename)):
              return False
    else:
      if ("*" in str(os.path.basename(source))):
        if (os.path.isdir(os.path.dirname(source))):
          for root, folders, files in os.walk(os.path.dirname(source)):
            for name in files:
              if (fnmatch.fnmatch(name, str(os.path.basename(source)))):
                temp = None
                if (rename == None):
                  temp = os.path.join(destination, os.path.relpath(root, os.path.dirname(source)), name)
                else:
                  temp = os.path.join(destination, os.path.relpath(root, os.path.dirname(source)), rename)
                if (os.path.exists(temp)):
                  continue
                context.log(None, "Copying from \""+str(os.path.join(root, name))+"\" to \""+str(temp)+"\"...")
                if not (move(os.path.join(root, name), temp, context, rename)):
                  return False
                context.log(None, "Copied from \""+str(os.path.join(root, name))+"\" to \""+str(temp)+"\"!")
        else:
          if not (move(source, destination, context, rename)):
            return False
      else:
        if not (move(source, destination, context, rename)):
          return False
    context.log(None, "Copied from \""+self.source.getContent()+"\" to \""+self.destination.getContent()+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.source)+", "+self.toString(self.destination)+", "+self.toString(self.rename)+">"

