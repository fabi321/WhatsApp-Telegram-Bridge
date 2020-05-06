# Contributing

## Structure

The source code of `wat-bridge` is not very intuitive, so here is a list of
what each file is in charge of:

- `TODO`: program launcher, connects signals with handlers and
  initializes configuration
- `DBModels`: generally, database classes used for different types of storage
- `Attachments`: yet more database classes, dedicated to attachment files
- `TODO`: the main loops for the WhatsApp and Telegram bots
- `Pipes`: signal handlers for terminating the program and message
  relaying between WhatsApp and Telegram
- `TODO/remove`: settings and static stuff used across all modules
- `TODO`: Telegram bot implementation using
  [python-telegram](https://github.com/alexander-akhmetov/python-telegram)
- `TODO`: WhatsApp bot implementation using
  [yowsup](https://github.com/tgalal/yowsup)


Usually, each component is well isolated, which allows for easier modifications
and maintenance.


## Documentation

I tend to use Google style docstrings where appropriate as shown here:
<http://www.sphinx-doc.org/es/stable/ext/napoleon.html>, as I find these are
easy to read at a glance when viewing the source code.
