import re
import io
from html.parser import HTMLParser

const = {
    "tab_size": 2
}


def parse_style(style: dict) -> str:
  parsed_style = ""
  for attr, value in style.items():
    parsed_style += f"{attr}: {value} !important; "
  return parsed_style

def parse_properties(properties: dict) -> str:
  parsed_properties = ""
  for attr, value in properties.items():
    parsed_properties += f"{attr}=\"{value}\""
  return parsed_properties


def parse_text(text: str) -> str:
  parsed_text = text

  bold = re.compile(r"\B(?<!\*)\*\*(?![\*\s])(.+?)(?<!\*\s)\*\*(?!\*)\B")
  parsed_text = bold.sub(r"<b>\1</b>", parsed_text)

  oblique = re.compile(r"\B(?<!\*)\*(?![\*\s])(.+?)(?<!\*\s)\*(?!\*)\B")
  parsed_text = oblique.sub(r"<i>\1</i>", parsed_text)

  underlined = re.compile(r"\b(?<!\*)\_(?![\*\s])(.+?)(?<!\*\s)\_(?!\*)\b")
  parsed_text = underlined.sub(r"<u>\1</u>", parsed_text)

  strike = re.compile(r"\B(?<!\-)\-(?![\-\s])(.+?)(?<!\-\s)\-(?!\-)\B")
  parsed_text = strike.sub(r"<s>\1</s>", parsed_text)

  return parsed_text


def fig_bytes(fig, **kwargs):
  buf = io.BytesIO()
  fig.savefig(fname=buf, format='png', **kwargs)
  buf.seek(0)
  fig_bytes = buf.read()
  return fig_bytes


class TagStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = io.StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()