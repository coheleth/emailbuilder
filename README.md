# EMailBuilder

> Simple python library that makes creating emails easier. Features tables, embedded images and matplotlib charts.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [The EMail Class/Object](#the-email-classobject)
  - [Attributes](#attributes)
    - [Subject](#subject)
    - [Sender](#sender)
    - [Receiver, Copy and Blind Copy](#receiver-copy-and-blind-copy)
    - [Style](#style)
  - [Methods](#methods)
    - [email.append()](#emailappend)
    - [email.attach()](#emailattach)
    - [email.html()](#emailhtml)
    - [email.plain()](#emailplain)
    - [email.message()](#emailmessage)
- [Components](#components)
  - [Header](#header)
  - [Paragraph](#paragraph)
  - [Container](#container)
  - [Table](#table)
  - [Image](#image)
  - [ImageRaw](#imageraw)
  - [Figure](#figure)
- [To-Do](#to-do)

---

## Installation

You can install the latest release with pip:

```bash
pip install emailbuilder
```

Or build and install the development version yourself:

```bash
git clone https://github.com/coheleth/emailbuilder &&\
pip install ./emailbuilder
```

---

## Usage

Import EmailBuilder:

```python
import emailbuilder as eb
```

Create an `emailbuilder.EMail` object and append elements to it:

```python
# Create eb.EMail object
# (see the "EMail class" section for more details)
email = eb.EMail(
    "EMail Subject",
    "sender@example.com",
    "receiver@example.com"
)

#  Append components to the eb.EMail object
# (see the "Components" section for more details)
email.append(eb.Header("Hello World!"))
email.append(eb.Paragraph("Lorem ipsum dolor sit amet consectetur"))
```

You can also append matplotlib figures:

```python
plt.figure()
plt.plot([1, 2])
plt.title("Example")

email.append(eb.Figure(plt.gcf(), "example-figure"))
```

Then, you can send the e-mail via your preferred method. For instance:

```python
s = smtplib.SMTP(...)

...

s.send_message(email.message())
s.quit()
```

---

## The EMail Class/Object

This object is used for setting the e-mail information, and provides methods to render the e-mail contents.

### Attributes

#### Subject

The e-mail's subject, as a string

#### Sender

The sender's e-mail, as a string

#### Receiver, Copy and Blind Copy

The receiver(s)'s e-mail(s), as either a string or a list

#### Style

A dictionary containing the basic style rules for the e-mail.
`global` applies to all elements, `root` applies to the table element wrapping the emails contents, and `body`, `header`, `subheader`, `paragraph`, `image` and `table` apply to their respective elements.

### Methods

#### email.append()

```python
email.append(component)
```

Appends a component to the end of the e-mail

#### email.attach()

```python
with open("file.png", "rb") as f:
  email.attach(
      item = f.read(),
      type = "image",
      extension = "png",
      cid = "my_image",
      mime = MIMEImage(f.read()) # Optional
  )
```

Adds an attachment to the e-mail.

#### email.html()

```python
print(email.html())
```

Returns the e-mail as HTML.

#### email.plain()

```python
print(email.plain())
```

Returns the e-mail as plain text.

#### email.message()

```python
s.send_message(email.message())
```

Returns the e-mail as a `EmailMessage` object.

---

## Components

Below are the included components in the emailbuilder library.

### Header

```python
eb.Header(
    content: str,
    style: dict = {}
)
```

An `<h1>` element, with the text from the `content` parameter.

### SubHeader

```python
eb.SubHeader(
    content: str,
    style: dict = {}
)
```

An `<h2>` element, with the text from the `content` parameter.

### Paragraph

```python
eb.Paragraph(
    content: str,
    style: dict = {}
)
```

A single paragraph, with the text from the `content` parameter.

### Container

```python
eb.Container(
    style: dict = {}
)
```

A `<div>` element. Items can be appended with the `append(item)` method, just like with the `EMail` object.

### Table

```python
eb.Table(
  content: dict,
  style: dict = {}
)
```

A simple table, created from a dictionary of arrays, the keys' names being the columns, and the values, the rows.

##### Usage with pandas dataframes

If used with pandas dataframes, convert the dataframe to a dictionary with the default 'dict' orientation, eg.:

```python
df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30]
})

table = pd.to_dict(orient='dict')

email.append(eb.Table(table))
```

##### Usage with other components

Other components, such as `eb.Header`, can be passed via de dictionary, eg.:

```python
table = {
  'Attribute': ['personality', 'voice'],
  'Alice': ['calm', 'soft'],
  'Bob': ['nervous', eb.Header('LOUD')]
}
```

### Image

```python
eb.Image(
    src: str,
    alt: str = "",
    cid: str = <file name>,
    style: dict = {}
)
```

An embedded image, loaded from the `src` path. Alternative text, used for text-only e-mails is passed through the `alt` parameter.

### ImageRaw

```python
eb.ImageRaw(
    image: bytes,
    extension: str,
    alt: str = "",
    cid: str = <hashed bytes>,
    style: dict = {}
)
```

An embedded image, loaded as bytes from the `image` parameter. An image format must be provided through the `extension` parameter.

### Figure

```python
eb.Figure(
    figure: matplotlib figure,
    alt: str,
    style: dict = {},
    kwargs: dict = {}
)
```

An embedded MatPlotLib figure. Custom arguments for the `savefig` function can be passed through the `kwargs` parameter.
