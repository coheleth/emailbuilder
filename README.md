# EMailBuilder

> Simple HTML e-mail template builder python library. Allows for embedded images and matplotlib charts.

## Table of Contents

- [EMailBuilder](#emailbuilder)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [The EMail Class/Object](#the-email-classobject)
    - [Attributes](#attributes)
      - [Subject](#subject)
      - [Sender](#sender)
      - [Receiver](#receiver)
      - [Style](#style)
    - [Methods](#methods)
      - [email.append()](#emailappend)
      - [email.attach()](#emailattach)
      - [email.html()](#emailhtml)
      - [email.plain() (W.I.P.)](#emailplain-wip)
      - [email.message()](#emailmessage)
  - [Components](#components)
    - [Basic Elements](#basic-elements)
      - [Header](#header)
      - [Paragraph](#paragraph)
    - [Embedabbles](#embedabbles)
      - [Image](#image)
      - [ImageRaw](#imageraw)
      - [Figure](#figure)
    - [Containers](#containers)
      - [Container](#container)
  - [To-Do](#to-do)

---

## Installation

You can install it with pip:

```bash
pip install emailbuilder
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

This object is used for setting the information relating to the e-mail, and provides methods to render the e-mail contents.

### Attributes

#### Subject

The e-mail's subject, as a string

#### Sender

The sender's e-mail, as a string

#### Receiver

The receiver(s)'s e-mail(s), as either a string or a list

#### Style

A dictionary containing the basic style rules for the e-mail.
(More information concerning styling to be added)

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

#### email.plain() (W.I.P.)

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

### Basic Elements

#### Header

```python
eb.Header(
    content: str,
    style: dict = {}
)
```

An `<h1>` element, with the text from the `content` parameter.

#### Paragraph

```python
eb.Paragraph(
    content: str,
    style: dict = {}
)
```

A single paragraph, with the text from the `content` parameter.

### Embedabbles

#### Image

```python
eb.Image(
    src: str,
    alt: str = "",
    cid: str = <file name>,
    style: dict = {}
)
```

An embedded image, loaded from the `src` path. Alternative text, used for text-only e-mails is passed through the `alt` parameter.

#### ImageRaw

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

#### Figure

```python
eb.Figure(
    figure: matplotlib figure,
    alt: str,
    style: dict = {},
    kwargs: dict = {}
)
```

An embedded MatPlotLib figure. Custom arguments for the `savefig` function can be passed through the `kwargs` parameter.

### Containers

#### Container

```python
eb.Container(
    style: dict = {}
)
```

A `<div>` element. Items can be appended with the `append(item)` method, just like with the `EMail` object.

---

## To-Do

- [x] Write basic usage guide
- [ ] Add table components
- [ ] Document `style` argument
- [ ] Improve plain text function
