> [!WARNING]
> Absolutely work in progress!!

<div align="center">
  <img src="https://raw.githubusercontent.com/BrokenSource/DearLog/main/website/assets/images/logo.png" width="210">
  <h1>DearLog</h1>
  <span>🪵 A Human Logging Library 🪵</span>
  <br>
  <br>
    <a href="https://pypi.org/project/dearlog/"><img src="https://img.shields.io/pypi/v/dearlog?label=PyPI&color=blue"></a>
    <a href="https://pypi.org/project/dearlog/"><img src="https://img.shields.io/pypi/dw/dearlog?label=%E2%86%93&color=blue"></a>
    <a href="https://github.com/BrokenSource/DearLog/"><img src="https://img.shields.io/github/v/tag/BrokenSource/Dearlog?label=GitHub&color=orange"></a>
    <a href="https://github.com/BrokenSource/DearLog/stargazers/"><img src="https://img.shields.io/github/stars/BrokenSource/Dearlog?label=Stars&style=flat&color=orange"></a>
    <a href="https://discord.gg/KjqvcYwRHm"><img src="https://img.shields.io/discord/1184696441298485370?label=Discord&style=flat&color=purple"></a>
  <br>
  <br>
</div>

A simple, pretty and human-first logging library for Python.

## Goals

- **Sane defaults**: Sensible logging formats and levels out of the box

- **User-first** experience and quality of life features:
  - Logging multiple lines.. enqueues multiple logs!
  - All methods return the message for inlining

- **Levels**: Standard logging levels, plus quality of life ones:
  - `Level.OK`: For expected or successful operations
  - `Level.MINOR`: Disabled or ignored issues, features
  - `Level.SKIP`: For skipped operations, tests
  - `Level.FIXME`: May need manual workarounds
  - `Level.TODO`: For planned work or improvements
  - `Level.TIP`: Helpful hints or suggestions

- **Simple** handlers, formatters, configurations and filters
