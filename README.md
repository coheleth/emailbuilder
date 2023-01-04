# EMailBuilder

> Simple HTML e-mail template builder python library. Allows for embedded images and matplotlib charts.

## Table of Contens

- [EMailBuilder](#emailbuilder)
  - [Table of Contens](#table-of-contens)
  - [Installation](#installation)
  - [Usage](#usage)
  - [The `EMail` Class/Object](#the-email-classobject)
    - [Attributes](#attributes)
      - [`Subject`](#subject)
      - [`Sender`](#sender)
      - [`Receiver`](#receiver)
      - [`Style`](#style)
    - [Methods](#methods)
      - [`email.append(component)`](#emailappendcomponent)
      - [`email.attach(item, mime, type, extension, cid)`](#emailattachitem-mime-type-extension-cid)
      - [`email.html()`](#emailhtml)
      - [`email.plain()` (W.I.P.)](#emailplain-wip)
      - [`email.message()`](#emailmessage)
      - [`email.mime()` (W.I.P.)](#emailmime-wip)
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

&nbsp;

---

## Installation

You can install it with pip:

```bash
pip install emailbuilder
```

&nbsp;

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

&nbsp;

---

## The `EMail` Class/Object

This object is used for setting the information relating to the e-mail, and provides methods to render the e-mail contents.

&nbsp;

### Attributes

&nbsp;

#### `Subject`

The e-mail's subject, as a string

&nbsp;

#### `Sender`

The sender's e-mail, as a string

&nbsp;

#### `Receiver`

The receiver(s)'s e-mail(s), as either a string or a list

&nbsp;

#### `Style`

A dictionary containing the basic style rules for the e-mail.
(More information concerning styling to be added)

&nbsp;

### Methods

&nbsp;

#### `email.append(component)`

Appends a component to the end of the e-mail

&nbsp;

#### `email.attach(item, mime, type, extension, cid)`

Adds an attachment to the e-mail.

&nbsp;

#### `email.html()`

Returns the e-mail as HTML.

&nbsp;

#### `email.plain()` (W.I.P.)

Returns the e-mail as plain text.

&nbsp;

#### `email.message()`

Returns the e-mail as a `EmailMessage` object.

&nbsp;

#### `email.mime()` (W.I.P.)

Returns the e-mail as a `MIMEMultipart` object, for legacy purposes.
(May be deprecated in the future.)

&nbsp;

---

## Components

Below are the included components in the emailbuilder library.

&nbsp;

### Basic Elements

&nbsp;

#### Header

```python
eb.Header(
    content: str,
    style: dict = {}
)
```

An `<h1>` element, with the text from the `content` parameter.

&nbsp;

#### Paragraph

```python
eb.Paragraph(
    content: str,
    style: dict = {}
)
```

A single paragraph, with the text from the `content` parameter.

&nbsp;

### Embedabbles

&nbsp;

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

&nbsp;

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

&nbsp;

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

&nbsp;

### Containers

&nbsp;

#### Container

```python
eb.Container(
    style: dict = {}
)
```

A `<div>` element. Items can be appended with the `append(item)` method, just like with the `EMail` object.

&nbsp;

---

## To-Do

- [x] Write basic usage guide
- [ ] Add table components
- [ ] Document `style` argument
- [ ] Improve plain text function
