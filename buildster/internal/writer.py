
# Author: Pierce Brooks


from .performer import Performer
from .destination import Destination
from .content import Content

from .utilities import *

class Writer(Performer):
  def __init__(self, destination = None, content = None):
    super(Writer, self).__init__()
    self.destination = None
    self.content = None
    if (type(destination) == Destination):
      self.destination = destination
    if (type(content) == Content):
      self.content = content
      
  def getContent(self):
    return self.destination.getContent()
    
  def perform(self, context):
    context.log(None, "Writing \""+self.toString(self.destination)+"\"...")
    if ((self.destination == None) or (self.content == None)):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    descriptor = open(content, "w")
    if not (write(descriptor, self.content.getContent())):
      return False
    descriptor.close()
    context.log(None, "Wrote \""+self.toString(self.destination)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.destination)+", "+self.toString(self.content)+">"

