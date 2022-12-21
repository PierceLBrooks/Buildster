
# Author: Pierce Brooks


from .object import Object
from .username import Username
from .password import Password


class Credentials(Object):
  def __init__(self, username = None, password = None):
    super(Credentials, self).__init__()
    self.username = None
    self.password = None
    if (type(username) == Username):
      self.username = username
    if (type(password) == Password):
      self.password = password
    
  def __str__(self):
    return "<"+self.toString(self.username)+", "+self.toString(self.password)+">"
    
