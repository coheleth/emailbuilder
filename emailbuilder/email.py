from .components import Element
from .utils import const, parse_style, parse_text, TagStripper

from email.mime.application import MIMEApplication
from email.message import EmailMessage
from email.utils import make_msgid

from copy import deepcopy
from typing import Any, Optional

import os
import tempfile


class EMail:
  def __init__(
      self, 
      subject: str = "",
      sender: str = "",
      receiver: Optional[str | list] = None,
      copy: Optional[str | list] = None,
      blind_copy: Optional[str | list] = None,
      style: Optional[dict] = None
    ) -> None:
    """
    E-Mail Object

    :param subject: E-Mail subject
    :param sender: Sender's address
    :param receiver: Receiver(s)'s address(es)
    :param style: Custom style rules
    """
    if style is None:
      style = {}

    default_style = {
        "global": {
            "color": "#000000",
            "font-family": "sans-serif",
            "font-size": "12px"
        },
        "root": {
            "background-color": "#FFFFFF"
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
    self.copy = copy
    self.blind_copy = blind_copy
    self.items = []
    self.style = {**default_style, **style}
    self.attachments = []

  def attach(self, item: Any, type: str, extension: str, cid: Optional[str] = None, mime: Optional[Any] = None, src: Optional[str] = None) -> None:
    """
    Add attachment

    :param item: Item to be attached
    :param type: Attachment's mime tipe
    :param extension: Attachment's file extension
    :param cid: Attachment's content id
    :param mime:  Attachment as MIME object
    """
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
        "uuid": _uuid,
        "src": src
    }
    self.attachments.append(_attachment)

  def append(self, item: Element) -> None:
    """
    Append Element

    :param item: Element to append
    """
    self.items.append(item)

  def html(self) -> str:
    """
    Get the e-mail's body as HTML

    :return: String containing e-mail's body as HTML
    """
    self.attachments = []
    html = ""
    for item in self.items:
      if issubclass(type(item), Element):
        item.email = self
        html += item.html(deepcopy(self.style))
      else:
        html += f"{parse_text(str(item))}<br/>"
    root_style = parse_style(self.style["root"])
    body_style = parse_style(self.style["body"])
    return f"""
    <body style=\"{root_style}\">
      <table border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"{body_style}\">
        {html}
      </table>
    </body>
    """

  def plain(self) -> str:
    """
    Get the e-mail's content as plain-text (W.I.P.)

    :return: String containing e-mail's content
    """
    s = TagStripper()
    s.feed(self.html())
    return s.get_data()

  def to_outlook(self) -> Any:
    """
    Get the e-mail as a win32com Outlook email object

    :return: win32com Outlook email object, or None
    """
    try:
      import win32com.client as w32
    except ImportError:
      w32 = None

    if w32:
      o = w32.Dispatch("Outlook.Application")
      email = o.CreateItem(0)
      if self.receiver is not None:
          email.To = self.receiver
      if self.copy is not None:
          email.CC = self.copy
      if self.blind_copy is not None:
          email.BCC = self.blind_copy
      if self.subject is not None:
          email.Subject = self.subject
      email.Body = self.plain()
      email.HTMLBody = self.html()
      for att in self.attachments:
        if att['src'] is None:
          fd, path = tempfile.mkstemp(suffix="." + att['extension'])
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
        else:
            attachment = email.Attachments.Add(att['src'])
            attachment.PropertyAccessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                att['cid']
            )
      return email
    else:
      return None

  def message(self) -> EmailMessage:
    """
    Get the e-mail as an EmailMessage object

    :return: The e-mail as an EmailMessage object
    """
    _msg = EmailMessage()
    _msg["Subject"] = self.subject
    _msg["From"] = self.sender
    _msg["To"] = self.receiver
    _msg["CC"] = self.copy
    _msg["BCC"] = self.blind_copy
    _msg.set_content(self.plain())
    _msg.add_alternative(self.html(), subtype="html")
    for att in self.attachments:
      _msg.add_attachment(att["content"], att["type"],
                          att["extension"], cid=f"<{att['cid']}>", filename=att["cid"])
    return _msg
