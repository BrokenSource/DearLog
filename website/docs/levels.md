---
title: Logging Levels
icon: material/cards
---

<!-- You can either use `logger.setlevel(str)` or env `LOGLEVEL=str` to configure levels. -->

### Custom levels

Extending or modifying levels are one of DearLog's main goals.

#### Modifying

Simply change properties of objects in `dearlog.Levels`:

```python
from dearlog import Levels

Levels.INFO.color = "bright_blue"
Levels.TODO.enabled = False
```

#### Adding

...

## Levels

!!! tip "Usage guidelines aren't strict, use your judgement and taste!"

### `trace`

Very detailed events, noisy and high volume, opt-in by default.

```python
# Examples
logger.trace(f"Resizing ShaderTexture {self.uuid} to {width}x{height}")
logger.trace(f"Calling {type(self).__name__}.update() with {dt=:.4f}s")
```

### `debug`

Detailed events near hot paths for diagnostic. Intentionally doesn't return formatted messages unless logged, opt-in by default.

```python
# Examples
logger.debug(f"Exported environment variables: {self.environ}")
logger.debug(f"Loaded dictionary from pyproject.toml: {data}")
```

### `info`

Regular informational messages about events or states, nothing out of the ordinary. Should not log actions or decisions that impact flow.

```python
# Examples
logger.info(f"Finished rendering video file ({output})")
logger.info(f"OpenGL Renderer: {self.opengl.info['GL_RENDERER']}")
```

### `note`

Noteworthy events that _may_ require user attention or cause errors, and/or actions taken to prevent them or improve user experience.

```python
# Decisions taken
logger.note("Enabling cargo-zigbuild for easier cross-compilation")
logger.note("You may opt-out of it with AUTO_ZIGBUILD=0")

# Advice Examples
logger.note("PyTorch nightly may be unstable and need updated drivers")
```

### `ok`

Successful operations, checks, basically a shorter "success"

```python
# Finished actions
logger.ok(f"Compiled binary at ({release})")
logger.ok(f"Finished rendering video ({output})")
```

### `minor`

Low-importance events that can be safely ignored in most cases, or that are echoing items/states for user awareness.

```python
# Awareness example
for asset in self.assets:
    logger.minor(f"• Asset: ({asset.name})")
    self.bundle(asset)
```

### `skip`

Events where an action was intentionally skipped or not performed.

```python
# Download manager
if Path(download).exists():
    logger.skip(f"Already downloaded file at ({download})")
    return
```

```python
# Already performed action
if Path(output).exists():
    logger.skip(f"Skip calling {command}")
    return
```

### `todo`

For unimplemented features, planned actions, or future improvements, which shouldn't/may cause disruptions, that would be nice to have.

```python
# Example
logger.todo("Multithreading contexts are not yet supported, locking usage")
logger.todo("FFmpeg isn't automatically managed, please have it externally")
```

### `tip`

Missable or uncommon knowledge to improve user experience.

```python
# Examples
logger.tip("(macOS) Use PYTORCH_ENABLE_MPS_FALLBACK=1 to enable CPU fallback")
logger.tip("Find your rust host with 'rustc --version --verbose'")
```

### `fixme`

Tell missing features, potential improvements, or less-than-ideal stuff.

Must not directly cause Exceptions (`raise` it instead), and should be actionable by the user via workarounds, configurations.

You may use it as "this is knowingly broken" too.

```python
# Examples
logger.fixme("Cross compilation to macOS needs setting an SDKROOT")
logger.fixme("Files from docker volumes may be owned by root user")
```

### `warn`

Potentially harmful situations, undesired states, or recoverable issues.

```python
# Examples
logger.warn(f"Rust doesn't guarantee a working build for Tier 2 target {target}")
logger.warn("This model is licensed under CC BY-NC 4.0 (non-commercial)")
```

### `error`

Error events that _might_ still allow the application to continue running, or that require user intervention (externally, code).

```python
# Examples
logger.error(f"Failed to download file from {url}: {error}, retrying..")
logger.error(f"Received wrong download size for {file}, redownloading..")
logger.error("Cannot symlink on Windows without Developer Mode enabled")
```

### `crit`

Cannot continue running: unrecoverable states, unsupported operations, or impossible support for the current hardware/environment, etc.

```python
# Examples
logger.crit("Failed to create OpenGL context, ensure you have EGL available")
logger.crit("Only Nvidia GPUs are supported in nvibrant")
logger.crit(f"Failed to allocate {size} of GPU memory")
```
