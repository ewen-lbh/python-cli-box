"""
Adds a box around `text`.
    
`corners` controls the characters for the corners of the box,
it takes a 4-tuple of strings in the form 
`(top_left, top_right, bottom_right, bottom_left)`

`sides` controls the characters for the sides of the box,
it takes a 4-tuple of strings in the form
`(top, right, bottom, left) (à la CSS)`
or a 2-tuple of strings n the form
`(vertical, horizontal)`

For example:
```
>>> box.box('some looooooooooong text\nshort one', corners=('1', '2', '3', '4'), sides=('|', '-'))
"1--------------------------2
 | some looooooooooong text |
 |        short one         |
 4--------------------------3"
```
"""
from wcwidth import wcswidth
from typing import *


def box(
    text: str,
    corners: Tuple[str, str, str, str] = ("┌", "┐", "┘", "└"),
    sides: Union[Tuple[str, str, str, str], Tuple[str, str]] = ("│", "─"),
    background: str = " ",
    align: Union[Literal["left"], Literal["center"], Literal["bottom"]] = "center",
) -> str:
    padding = 1
    """
    Adds a box around `text`.
    
    `corners` controls the characters for the corners of the box,
    it takes a 4-tuple of strings in the form 
    `(top_left, top_right, bottom_right, bottom_left)`
    
    `sides` controls the characters for the sides of the box,
    it takes a 4-tuple of strings in the form
    `(top, right, bottom, left) (à la CSS)`
    or a 2-tuple of strings n the form
    `(vertical, horizontal)`
    
    For example:
    ```
    >>> box.box('some looooooooooong text\nshort one', corners=('1', '2', '3', '4'), sides=('|', '-'))
    "1--------------------------2
     | some looooooooooong text |
     |        short one         |
     4--------------------------3"
    ```
    """
    if len(sides) == 2:
        sides = (sides[1], sides[0], sides[1], sides[0])

    lines = text.splitlines()
    text_width = max(wcswidth(s) for s in lines)
    width = text_width + padding * 2
    res = [corners[0] + sides[0] * width + corners[1]]
    alignement_char = {"left": "<", "right": ">", "center": "^"}[align]
    for l in lines:
        res.append(
            sides[3]
            + " " * (width - text_width - wcswidth(sides[3]))
            + (f"{l:{alignement_char}{text_width}}")[:text_width]
            + " " * (width - text_width - wcswidth(sides[1]))
            + sides[1]
        )
    res.append(corners[3] + sides[2] * width + corners[2])
    return "\n".join(res)


def rounded(text: str, **kwargs) -> str:
    """
    Uses a rounded-style box.
    See `box.box` for parameters.
    This just calls `box.box` with
    
    ```
    corners=("╭", "╮", "╯", "╰")
    ```
    
    but what you specify in `**kwargs` overrides
    `corners` and is passed to `box.box`
    """
    return box(
        text,
        **{
            "corners": ("╭", "╮", "╯", "╰"),
            # 'sides': '',
            **kwargs,
        },
    )
