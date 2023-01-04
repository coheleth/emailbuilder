from .base import Component
from ..utils import const, parse_style, parse_text


class Header(Component):
  def __init__(self, content: str, style=None, email=None) -> None:
    super().__init__(style, email)
    self.content = content
    self.keys.extend(["header"])
    print(issubclass(type(self), Header))

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<h1 style=\"{parse_style(_style)}\">{self.content}</h1>"

  def plain(self) -> str:
    return f"# {self.content} #\n\n"


class Paragraph(Component):
  def __init__(self, content: str, style=None, email=None) -> None:
    super().__init__(style, email)
    self.content = content
    self.keys.extend(["paragraph"])

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<p style=\"{parse_style(_style)}\">{parse_text(self.content)}</p>"

  def plain(self) -> str:
    return f"{self.content}\n"
