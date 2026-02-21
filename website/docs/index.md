---
title: Documentation
---

Welcome to **🪵 DearLog**'s documentation!

## Getting Started

Simply import it and start logging:

```python
from dearlog import logger  # isort: split

logger.info("Hello, DearLog!")
logger.note("• Colored by default")
logger.todo("• Plan your work")

logger.ok("✔ Quickstart complete!")
```

!!! tip "Always import dearlog first"
    First thing it does is getting a [`time.monotonic()`](https://docs.python.org/3/library/time.html#time.monotonic) instant for stopwatch accuracy.

    - The isort statement ensures formatters don't move it below other imports.

Oh, and [`rich`](https://pypi.org/project/rich/) formatting is enabled by default

```python
logger.minor((
    "[bold red]Consider "
    "[link=https://github.com/sponsors/Tremeschin/]Supporting[/link][/] "
    "me on GitHub!"
))
```
