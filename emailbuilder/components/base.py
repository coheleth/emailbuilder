from ..utils import const, parse_style


class Component:
  def __init__(self, style=None, email=None) -> None:
    if style is None:
      style = {}
    self.style = style
    self.keys = ["global"]
    self.email = email

  def apply_style(self, style: dict) -> dict:
    _applied_style = {}

    for key, value in style.items():
      if key in self.keys and type(value) is dict:
        for attr, value in value.items():
          _applied_style[attr] = value

    return _applied_style

  def html(self, style) -> str:
    _style = style
    return ""

  def plain(self) -> str:
    return ""


class Container(Component):
  def __init__(self, style=None, email=None) -> None:
    super().__init__(style, email)
    self.children = []
    self.before = "<div style={style}>"
    self.after = "</div>"
    self.keys.extend(["container"])
    self.indent = ""

  def append(self, item) -> None:
    self.children.append(item)

  def render_child(self, child, style) -> str:
    if issubclass(type(child), Component):
      child.email = self.email
      return child.html(style)
    else:
      return f"{str(child)}<br/>"

  def render_children(self, style) -> str:
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
    """
    Returns the HTML code for the component

    Parameters
    ----------
    style : dict
      A dictionary containing the component's inherited style
    """
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
