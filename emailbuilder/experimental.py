from . import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EMail(email.EMail):
  def __init__(self, subject: str = "", sender: str = "", receiver=None, style=None) -> None:
    super().__init__(subject, sender, receiver, style)

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
    return _mime_mail
