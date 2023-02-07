from ..utils import const, parse_style
from typing import Any, Optional


class Component:
  """
  Base component class

  :param style: Custom style rules
  """

  def __init__(self, style: Optional[dict] = None) -> None:
    if style is None:
      style = {}
    self.style = style
    self.keys = ["global"]
    self.email = None

  def apply_style(self, style: dict) -> dict:
    """
    Concatenates the component's inherited
    style rules with its custom ones
    """
    _applied_style = {}

    for key, value in style.items():
      if key in self.keys and type(value) is dict:
        for attr, value in value.items():
          _applied_style[attr] = value

    return _applied_style

  def html(self, style) -> str:
    """
    Renders the HTML code for the component

    :param style : The component's inherited style rules

    :return: The HTML code for the component
    """
    _style = style
    return ""

  def plain(self) -> str:
    """
    Gets the component as plain text

    :return: The component as plain text
    """
    return ""


class Container(Component):
  """
  Base container component class

  :param style: Custom style rules
  """

  def __init__(self, style=None) -> None:
    super().__init__(style)
    self.children = []
    self.before = "<div style={style}>"
    self.after = "</div>"
    self.keys.extend(["container"])
    self.indent = ""

  def append(self, item: str | Component) -> None:
    """
    Appends a child component to the container

    :param item: Component or text to append
    """
    self.children.append(item)

  def render_child(self, child: Any, style: dict) -> str:
    """
    Renders a child component to HTML

    :param child: Component to render
    :param style: The style rules the child will inherit

    :return: The rendered HTML
    """
    if issubclass(type(child), Component):
      child.email = self.email
      return child.html(style)
    else:
      return f"{str(child)}<br/>"

  def render_children(self, style: dict) -> str:
    """
    Renders the container's children to HTML

    :param style: The style rules the child components will inherit

    :return: The rendered HTML
    """
    _style = {**self.apply_style(style), **self.style}
    _append_style = {}
    for key in self.keys:
      if key != "global":
        _append_style[key] = self.style
    _combined_style = {**style, **_append_style}

    _passable_attrs = ["color", "font-family", "font-size", "font-weight"]
    for attr in _passable_attrs:
      # print(f"{attr}: {attr in self.apply_style(style).keys()}")
      if attr in _style.keys():
        _combined_style["global"][attr] = _style[attr]

    _html = ""
    for i, child in enumerate(self.children):
      _html += self.render_child(child, _combined_style)
    return _html

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    return f"<div style=\"{parse_style(_style)}\">{self.render_children(style)}</div>"

  def plain(self) -> str:
    _tab = self.indent
    _plain = ""
    for child in self.children:
      if issubclass(type(child), Container):
        child.indent = self.indent
        _plain += f"{child.plain()}"
      elif issubclass(type(child), Component):
        _plain += f"{_tab}{child.plain()}\n"
      else:
        _plain += f"{_tab}{str(child)}\n"
    return _plain
