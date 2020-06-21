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

You can pass in an array of strings to get the separated with line separators:
>>> print(box(["a multiline\\ntext\\non an area", "another \\033[34marea. \\033[0m\\nahaha"]))
┌────────────────┐
│  a multiline   │
│      text      │
│   on an area   │
├────────────────┤
│ another \033[34marea. \033[0m │
│     ahaha      │
└────────────────┘

The characters for sides connected to separators are customizable:
>>> print(box(["lorem", "ipsum"], connected_sides=("L", "R")))
┌───────┐
│ lorem │
L───────R
│ ipsum │
└───────┘
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
    text: Union[str, List[str]],
    corners: Tuple[str, str, str, str] = ("┌", "┐", "┘", "└"),
    sides: Union[Tuple[str, str, str, str], Tuple[str, str]] = ("│", "─"),
    connected_sides: Tuple[str, str] = ("├", "┤"),
    background: str = " ",
    align: str = "center",
) -> str:
    padding = 1
    if len(sides) == 2:
        sides = (sides[1], sides[0], sides[1], sides[0])

    if type(text) is str:
        lines = text.splitlines()
    else:
        lines = []
        for area in text:
            for l in area.splitlines():
                lines.append(l)
    text_width = max(strwidth(l) for l in lines)
    width = text_width + padding * 2
    res = [corners[0] + sides[0] * width + corners[1]]
    format_line = (
        lambda l: sides[3]
        + background * (width - text_width - strwidth(sides[3]))
        + align_text(l, text_width, align)
        + background * (width - text_width - strwidth(sides[1]))
        + sides[1]
    )
    if type(text) is str:
        for l in text.splitlines():
            res.append(format_line(l))
    else:
        for i, area in enumerate(text):
            for l in area.splitlines():
                res.append(format_line(l))
            # Don't add a separator if we're on the last area
            if i != len(text) - 1:
                res.append(connected_sides[0] + sides[2] * width + connected_sides[1])
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
