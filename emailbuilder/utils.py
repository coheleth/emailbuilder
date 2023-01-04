import re
import io

const = {
    "tab_size": 2
}


def parse_style(style: dict) -> str:
  _parsed_style = ""
  for attr, value in style.items():
    _parsed_style += f"{attr}: {value} !important; "
  return _parsed_style


def parse_text(text: str) -> str:
  _parsed_text = text

  _bold = re.compile(r"\B(?<!\*)\*\*(?![\*\s])(.+?)(?<!\*\s)\*\*(?!\*)\B")
  _parsed_text = _bold.sub(r"<b>\1</b>", _parsed_text)

  _oblique = re.compile(r"\B(?<!\*)\*(?![\*\s])(.+?)(?<!\*\s)\*(?!\*)\B")
  _parsed_text = _oblique.sub(r"<i>\1</i>", _parsed_text)

  _underlined = re.compile(r"\b(?<!\*)\_(?![\*\s])(.+?)(?<!\*\s)\_(?!\*)\b")
  _parsed_text = _underlined.sub(r"<u>\1</u>", _parsed_text)

  _strike = re.compile(r"\B(?<!\-)\-(?![\-\s])(.+?)(?<!\-\s)\-(?!\-)\B")
  _parsed_text = _strike.sub(r"<s>\1</s>", _parsed_text)

  return _parsed_text


def fig_bytes(fig, **kwargs):
  buf = io.BytesIO()
  fig.savefig(fname=buf, **kwargs)
  buf.seek(0)
  _bytes = buf.read()
  return _bytes
