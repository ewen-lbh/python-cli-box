# box

> Add a box around your text for prettier CLIs

## Installation

```sh-session
pip install cli-box
```

## Usage

```python
>>> import cli_box
>>> print(cli_box.rounded("""Lorem ipsum
... dolor sit amet.
... """))
╭─────────────────╮
│   Lorem ipsum   │
│ dolor sit amet. │
╰─────────────────╯
```
