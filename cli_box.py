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
>>> print(box('some looooooooooong text\\nshort one', corners=('1', '2', '3', '4'), sides=('|', '-')))
1--------------------------2
| some looooooooooong text |
|        short one         |
4--------------------------3

It also works with ANSI escape codes:
>>> print(box("Some \\033[33mcolored\\033[0m text."))
┌────────────────────┐
│ Some \033[33mcolored\033[0m text. │
└────────────────────┘
"""
from wcwidth import wcswidth
from strip_ansi import strip_ansi
from typing import *
import doctest


def strwidth(o: str) -> int:
    return wcswidth(strip_ansi(o))


def align_text(text: str, width: int, align: str = "left") -> str:
    textw = strwidth(text)
    if align == "left":
        return text + " " * (width - textw)
    elif align == "right":
        return " " * (width - textw) + text
    else:
        leftspaces = (width - textw) // 2
        rightspaces = width - textw - leftspaces
        return (" " * leftspaces) + text + (" " * rightspaces)


def box(
    text: str,
    corners: Tuple[str, str, str, str] = ("┌", "┐", "┘", "└"),
    sides: Union[Tuple[str, str, str, str], Tuple[str, str]] = ("│", "─"),
    background: str = " ",
    align: str = "center",
) -> str:
    padding = 1
    if len(sides) == 2:
        sides = (sides[1], sides[0], sides[1], sides[0])

    lines = text.splitlines()
    text_width = max(strwidth(l) for l in lines)
    width = text_width + padding * 2
    res = [corners[0] + sides[0] * width + corners[1]]
    alignement_char = {"left": "<", "right": ">", "center": "^"}[align]
    for l in lines:
        res.append(
            sides[3]
            + " " * (width - text_width - strwidth(sides[3]))
            + align_text(l, text_width, align)
            + " " * (width - text_width - strwidth(sides[1]))
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


if __name__ == "__main__":
    doctest.testmod()
