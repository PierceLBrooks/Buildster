
# Author: Pierce Brooks


from .performer import Performer
from .url import URL

from .utilities import *

class Downloader(Performer):
  def __init__(self, url = None):
    super(Downloader, self).__init__()
    self.url = None
    if (type(url) == URL):
      self.url = url
      
  def getContent(self):
    if (self.url == None):
      return ""
    return self.url.getContent()
    
  def perform(self, context):
    context.log(None, "Downloading \""+self.toString(self.url)+"\"...")
    if (self.url == None):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    if not (retrieve(context, content)):
       return False
    context.log(None, "Downloaded \""+self.toString(self.url)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.url)+">"
    
