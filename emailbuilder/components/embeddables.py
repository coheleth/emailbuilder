from .base import Component
from ..utils import const, parse_style, parse_text, fig_bytes
from email.mime.image import MIMEImage


class Image(Component):
  def __init__(self, src: str, alt: str = "", cid=None, style=None, email=None) -> None:
    super().__init__(style, email)
    self.alt = alt
    self.src = src
    if cid is None:
      cid = src.split("\\")[-1].split("/")[-1]
    self.cid = cid
    self.keys.extend(["image"])

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    with open(self.src, "rb") as img:
      _image = MIMEImage(img.read())
      _extension = self.src.split(".")[-1]
      self.email.attach(img.read(), _image, "image", _extension, self.cid)
      return f"<img src=\"cid:{self.cid}\" style=\"{parse_style(_style)}\" alt=\"{self.alt}\" />"

  def plain(self) -> str:
    return self.alt + "\n"


class ImageRaw(Component):
  def __init__(self, image, extension, alt: str = "", cid=None, style=None, email=None) -> None:
    super().__init__(style, email)
    self.alt = alt
    self.image = image
    self.type = extension
    if cid is None:
      cid = str(hash(image))
    self.cid = cid
    self.keys.extend(["image"])

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    _image = MIMEImage(self.image)
    self.email.attach(self.image, _image, "image", self.type, self.cid)
    return f"<img src=\"cid:{self.cid}\" style=\"{parse_style(_style)}\" alt=\"{self.alt}\" />"

  def plain(self) -> str:
    return self.alt + "\n"


class Figure(Component):
  def __init__(self, figure, alt=None, style=None, kwargs=None, email=None) -> None:
    super().__init__(style, email)
    if alt is None:
      alt = str(hash(self.figure))
    if kwargs is None:
      kwargs = {}
    self.figure = figure
    self.alt = alt
    self.kwargs = kwargs
    self.keys.extend(["image"])

  def html(self, style) -> str:
    _style = {**self.apply_style(style), **self.style}
    _image = fig_bytes(self.figure, **self.kwargs)
    _mime_image = MIMEImage(_image)
    self.email.attach(_image, _mime_image, "image", "png", self.alt)
    return f"<img src=\"cid:{self.alt}\" style=\"{parse_style(_style)}\" alt=\"{self.alt}\" />"

  def plain(self) -> str:
    return self.alt + "\n"
