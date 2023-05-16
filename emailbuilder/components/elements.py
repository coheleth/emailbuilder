from .base import Component
from ..utils import const, parse_style, parse_text, parse_properties
from typing import Optional


class Header(Component):
  """
  A level 1 header element
  <h1 />

  :param content: Text content
  :param style: Custom style rules
  """

  def __init__(self, content: str, style: Optional[dict] = None, properties: Optional[dict] = None) -> None:
    super().__init__(style, properties)
    self.content = content
    self.keys.extend(["header"])

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<h1 style=\"{parse_style(_style)}\" {parse_properties(self.properties)}>{self.content}</h1>"

  def plain(self) -> str:
    return f"# {self.content} #\n\n"


class Paragraph(Component):
  """
  A paragraph element
  <p />

  :param content: Text content
  :param style: Custom style rules
  """

  def __init__(self, content: str, style: Optional[dict] = None, properties: Optional[dict] = None) -> None:
    super().__init__(style, properties)
    self.content = content
    self.keys.extend(["paragraph"])

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<p style=\"{parse_style(_style)}\" {parse_properties(self.properties)}>{parse_text(self.content)}</p>"

  def plain(self) -> str:
    return f"{self.content}\n"
