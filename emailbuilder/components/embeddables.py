from .base import Component
from ..utils import const, parse_style, parse_text, fig_bytes
from email.mime.image import MIMEImage
from typing import Any, Optional


class Image(Component):
  """
  An image element, loaded from a file

  :param src: Source image file
  :param alt: Alternative text
  :param cid: Custom content ID
  :param style: Custom style rules
  """

  def __init__(self, src: str, alt: str = "", cid: Optional[str] = None, style: Optional[dict] = None, properties: Optional[dict] = None) -> None:
    super().__init__(style, properties)
    self.alt = alt
    self.src = src
    if cid is None:
      cid = src.split("\\")[-1].split("/")[-1]
    self.cid = cid
    self.keys.extend(["image"])

  def html(self, style: dict) -> str:
    _style = {**self.apply_style(style), **self.style}
    with open(self.src, "rb") as img:
      _image = MIMEImage(img.read())
      _extension = self.src.split(".")[-1]
      if self.email:
        self.email.attach(
            item=img.read(),
            mime=_image,
            type="image",
            extension=_extension,
            cid=self.cid
        )
      return f"<img src=\"cid:{self.cid}\" style=\"{parse_style(_style)}\" alt=\"{self.alt}\" />"

  def plain(self) -> str:
    return self.alt + "\n"


class ImageRaw(Component):
  """
  An image element, as raw bytes

  :param image: Image as bytes
  :param extension: The image's file format
  :param alt: Alternative text
  :param cid: Custom content ID
  :param style: Custom style rules
  """

  def __init__(self, image: Any, extension: str, alt: str = "", cid: Optional[str] = None, style: Optional[dict] = None,properties: Optional[dict] = None) -> None:
    super().__init__(style, properties)
    self.alt = alt
    self.image = image
    self.type = extension
    if cid is None:
      cid = str(hash(image))
    self.cid = cid
    self.keys.extend(["image"])

  def html(self, style: dict) -> str:
    _style = {**self.apply_style(style), **self.style}
    _image = MIMEImage(self.image)

    if self.email:
      self.email.attach(
          item=self.image,
          mime=_image,
          type="image",
          extension=self.type,
          cid=self.cid
      )
    return f"<img src=\"cid:{self.cid}\" style=\"{parse_style(_style)}\" alt=\"{self.alt}\" />"

  def plain(self) -> str:
    return self.alt + "\n"


class Figure(Component):
  """
  A matplotlib figure

  :param figure: The figure object
  :param alt: Alternative text
  :param style: Custom style rules
  :param kwargs: Custom kwargs
  """

  def __init__(self, figure: Any, alt: Optional[str] = None, style: Optional[dict] = None, properties: Optional[dict] = None, kwargs: Any = None) -> None:
    super().__init__(style, properties)
    if alt is None:
      alt = str(hash(figure))
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

    if self.email:
      self.email.attach(
          item=_image,
          mime=_mime_image,
          type="image",
          extension="png",
          cid=str(hash(_image))
      )

    return f"<img src=\"cid:{str(hash(_image))}\" style=\"{parse_style(_style)}\" alt=\"{self.alt}\" />"

  def plain(self) -> str:
    return self.alt + "\n"
