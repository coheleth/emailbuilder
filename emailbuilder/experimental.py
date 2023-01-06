from . import email
from typing import Any
import os
import tempfile


class EMail(email.EMail):
  def __init__(self, subject: str = "", sender: str = "", receiver=None, style=None) -> None:
    super().__init__(subject, sender, receiver, style)

  def outlook(self) -> Any:
    try:
      import win32com.client as w32
    except ImportError:
      w32 = None

    if w32:
      o = w32.Dispatch("Outlook.Application")
      email = o.CreateItem(0)
      email.To = self.receiver
      email.Subject = self.subject
      email.Body = self.plain()
      email.HTMLBody = self.html()
      for att in self.attachments:
        fd, path = tempfile.mkstemp(suffix=att['extension'])
        try:
          with os.fdopen(fd, 'wb') as tmp:
            tmp.write(att['content'])

          attachment = email.Attachments.Add(path)
          attachment.PropertyAccessor.SetProperty(
              "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
              att['cid']
          )
        finally:
          os.remove(path)
      return email
    else:
      return None
