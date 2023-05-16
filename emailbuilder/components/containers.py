from .base import Component, Container
from ..utils import const, parse_style, parse_properties
from typing import Any, Optional


class OrderedList(Container):
  """
  An ordered list element
  <OL />

  :param style: Custom style rules
  """

  def __init__(self, style: Optional[dict] = None, properties: Optional[dict] = None, kwargs: Optional[dict] = None) -> None:
    super().__init__(style, properties)
    self.order_prefix = ""

  def render_child(self, child: Any, style: dict) -> str:
    if issubclass(type(child), Component):
      return f"<li>{child.html(style)}</li>"
    else:
      return f"<li>{str(child)}</li>"

  def html(self, style: dict) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<ol style=\"{parse_style(_style)}\" {parse_properties(self.properties)}>{self.render_children(style)}</ol>"

  def plain(self) -> str:
    _tab = self.indent + ' ' * const["tab_size"]
    _plain = ""
    for i, child in enumerate(self.children):
      _prefix = f"{self.order_prefix}{i+1}."
      if issubclass(type(child), OrderedList):
        child.indent = _tab
        child.order_prefix = _prefix
        _plain += f"{child.plain()}"
      elif issubclass(type(child), Container):
        child.indent = _tab + (" " * (len(_prefix) + 1))
        _plain += f"{_tab}{_prefix} {child.plain()[(len(_tab + _prefix) + 1):]}"
      elif issubclass(type(child), Component):
        _plain += f"{_tab}{_prefix} {child.plain()}\n"
      else:
        _plain += f"{_tab}{_prefix} {str(child)}\n"
    return _plain


class UnorderedList(Container):

  """
  An unordered list element
  <UL />

  :param style: Custom style rules
  """

  def __init__(self, decorator: str = "*", style: Optional[dict] = None, properties: Optional[dict] = None, kwargs: Optional[dict] = None) -> None:
    super().__init__(style, properties)
    self.decorator = decorator + " "


  def render_child(self, child: Any, style: dict) -> str:
    if issubclass(type(child), Component):
      return f"<li>{child.html(style)}</li>"
    else:
      return f"<li>{str(child)}</li>"

  def html(self, style: dict) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<ul style=\"{parse_style(_style)}\" {parse_properties(self.properties)}>{self.render_children(style)}</ul>"

  def plain(self) -> str:
    _tab = self.indent + ' ' * const["tab_size"]
    _plain = ""
    for i, child in enumerate(self.children):
      if issubclass(type(child), UnorderedList):
        child.indent = _tab
        _plain += child.plain()
      elif issubclass(type(child), Container):
        child.indent = _tab + (" " * len(self.decorator))
        _plain += _tab + self.decorator + \
            child.plain()[len(_tab + self.decorator):]
      elif issubclass(type(child), Component):
        _plain += _tab + self.decorator + child.plain() + "\n"
      else:
        _plain += _tab + self.decorator + str(child) + "\n"
    return _plain


class Table(Container):

  """
  A table element (W.I.P.)
  <TABLE />

  :param style: Custom style rules
  """

  def render_child(self, child: Any, style: dict,  kwargs: Optional[dict] = None) -> str:
    if issubclass(type(child), Component):
      return child.html(style)
    else:
      return str(child)

  def html(self, style: dict) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<table style=\"{parse_style(_style)}\" {parse_properties(self.properties)}>{self.render_children(style)}</table>"

  def plain(self) -> str:
    _tab = self.indent + ' ' * const["tab_size"]
    _plain = ""
    for i, child in enumerate(self.children):
      if issubclass(type(child), UnorderedList):
        child.indent = _tab
        _plain += child.plain()
      elif issubclass(type(child), Container):
        child.indent = _tab
        _plain += _tab + \
            child.plain()[len(_tab):]
      elif issubclass(type(child), Component):
        _plain += _tab + child.plain() + "\n"
      else:
        _plain += _tab + str(child) + "\n"
    return _plain
