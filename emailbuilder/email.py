from .components import Component
from .utils import const, parse_style, parse_text

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.message import EmailMessage
from email.utils import make_msgid

from copy import deepcopy
from warnings import warn
from typing import Any

import os
import tempfile


class EMail:
  def __init__(self, subject: str = "", sender: str = "", receiver=None, style=None):
    if style is None:
      style = {}

    default_style = {
        "global": {
            "color": "#000000",
            "font-family": "sans-serif",
            "font-size": "12px"
        },
        "body": {
            "background-color": "#FFFFFF"
        },
        "header": {
            "font-size": "48px"
        },
        "subheader": {
            "font-size": "24px"
        },
        "paragraph": {
            "margin-bottom": "12px"
        },
        "image": {
            "width": "100%"
        },
        "table": {
            "background-color": "white"
        }
    }

    self.subject = subject
    self.sender = sender
    self.receiver = receiver
    self.items = []
    self.style = {**default_style, **style}
    self.attachments = []

  def attach(self, item, type, extension, cid=None, mime=None):
    _uuid = str(hash(item))
    if cid is None:
      cid = make_msgid()[1:-1]
    for attachment in self.attachments:
      if attachment["uuid"] == _uuid:
        return

    if mime is None:
      mime = MIMEApplication(item)

    _attachment = {
        "content": item,
        "mime": mime,
        "cid": cid,
        "type": type,
        "extension": extension,
        "uuid": _uuid
    }
    self.attachments.append(_attachment)

  def append(self, item):
    self.items.append(item)

  def html(self) -> str:
    self.attachments = []
    _html = ""
    for item in self.items:
      if issubclass(type(item), Component):
        item.email = self
        _html += item.html(deepcopy(self.style))
      else:
        _html += f"{parse_text(str(item))}<br/>"
    return _html

  def plain(self) -> str:
    _plain = ""
    for item in self.items:
      if issubclass(type(item), Component):
        _plain += item.plain()
      else:
        _plain += f"{str(item)}\n"
    return _plain

  def mime(self):
    _mime_mail = MIMEMultipart('related')
    _email_content = MIMEMultipart('alternative')
    _email_content["Subject"] = self.subject
    _email_content["From"] = self.sender
    _email_content["To"] = self.receiver
    _plain_mail = MIMEText(self.plain(), "plain")
    _html_mail = MIMEText(self.html(), "html")
    _email_content.attach(_plain_mail)
    _email_content.attach(_html_mail)
    _mime_mail.attach(_email_content)
    for attachment in self.attachments:
      _attachment = attachment["mime"]
      _attachment.add_header('Content-ID', f"<{attachment['cid']}>")
      _attachment.add_header('Content-Disposition',
                             "attachment", filename=attachment['cid'])
      _mime_mail.attach(_attachment)
    warn(
        "This function is deprecated and may be removed in a future update.",
        DeprecationWarning
    )
    return _mime_mail

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

  def as_string(self):
    return self.mime().as_string()

  def message(self):
    _msg = EmailMessage()
    _msg["Subject"] = self.subject
    _msg["From"] = self.sender
    _msg["To"] = self.receiver
    _msg.set_content(self.plain())
    _msg.add_alternative(self.html(), subtype="html")
    for att in self.attachments:
      _msg.add_attachment(att["content"], att["type"],
                          att["extension"], cid=f"<{att['cid']}>", filename=att["cid"])
    return _msg
