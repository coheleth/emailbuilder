from .base import Component, Container
from ..utils import const, parse_style


class OrderedList(Container):
  def __init__(self, style=None, email=None) -> None:
    super().__init__(style, email)
    self.order_prefix = ""

  def render_child(self, child, style) -> str:
    if issubclass(type(child), Component):
      return f"<li>{child.html(style)}</li>"
    else:
      return f"<li>{str(child)}</li>"

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<ol style=\"{parse_style(_style)}\">{self.render_children(style)}</ol>"

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
  def __init__(self, decorator="*", style=None, email=None) -> None:
    super().__init__(style, email)
    self.decorator = decorator + " "

  def render_child(self, child, style) -> str:
    if issubclass(type(child), Component):
      return f"<li>{child.html(style)}</li>"
    else:
      return f"<li>{str(child)}</li>"

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<ul style=\"{parse_style(_style)}\">{self.render_children(style)}</ul>"

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
