from . import email


class EMail(email.EMail):
  def __init__(self, subject: str = "", sender: str = "", receiver=None, style=None) -> None:
    super().__init__(subject, sender, receiver, style)
