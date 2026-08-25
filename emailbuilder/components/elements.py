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

class Table(Component):

  """
  A table element (W.I.P.)
  <TABLE />

  :param style: Custom style rules
  """

  def __init__(self, content: dict, style: dict | None = None, properties: dict | None = None) -> None:
    super().__init__(style, properties)
    self.content = content
    self.keys.extend(["table"])

    self.columns = self.content.keys()
    self.rows = []
    self.length = 0

    for column in self.content.values():
      if isinstance(column, list):
        self.length = max(self.length, len(column))
      else:
        raise TypeError("Table must be made from a dictionary of arrays.")

    for i in range(self.length):
      row = []
      for column in self.content.values():
        item = ""
        if len(column) > i:
          item = column[i]
        if isinstance(item, Component):
          row.append(item)
        else:
          row.append(str(item))
      self.rows.append(row)

      
  def html(self, style: dict) -> str:
    _style = {**self.apply_style(style), **self.style}
    header_items = []
    for column in self.columns:
      header_items.append(f"<th>{column}</th>")
    header = f"<tr>{"".join(header_items)}</tr>"

    rows = []
    for row in self.rows:
      row_items = []
      for item in row:
        if isinstance(item, Component):
          _style = {**self.apply_style(style), **self.style}
          row_items.append(f"<td>{item.html(style)}</td>")
        else:
          row_items.append(f"<td>{item}</td>")
      rows.append(f"<tr>{"".join(row_items)}</tr>")

    return f"<table style=\"{parse_style(_style)}\" {parse_properties(self.properties)}>{header}{"".join(rows)}</table>"

  def plain(self) -> str:
    _plain = ""
    return _plain
