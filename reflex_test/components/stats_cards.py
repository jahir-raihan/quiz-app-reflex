# Imports

import reflex as rx
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)

from ..backend.backend import State

# End Imports


def stats_card(
    stat_name: str,
    value: int,
    icon: str,
    icon_color: LiteralAccentColor,
    extra_char: str = "",
) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon(
                            tag=icon,
                            size=22,
                            color=rx.color(icon_color, 11),
                        ),
                        rx.text(
                            stat_name,
                            size="4",
                            weight="medium",
                            color=rx.color("gray", 11),
                        ),
                        spacing="2",
                        align="center",
                    ),

                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    rx.heading(
                        f"{extra_char}{value:,}",
                        size="7",
                        weight="bold",
                    ),

                    spacing="2",
                    align_items="end",
                ),
                align_items="start",
                justify="between",
                width="100%",
            ),
            align_items="start",
            width="100%",
            justify="between",
        ),
        size="3",
        width="100%",
        max_width="22rem",
        min_width='15rem'
    )


def stats_cards_group() -> rx.Component:
    return rx.el.div(
        rx.flex(
            stats_card(
                "Correct answers",
                State.correct_answers,
                "circle-check",
                "blue",
            ),
            stats_card(
                "Wrong Answers",
                State.wrong_answers,
                "circle-x",
                "orange",

            ),
            spacing="5",
            gap='2em',
            flex_direction=["column", "column", "row"],
            display=["flex"],
        ),
        width='100%',
        display='flex',
        align_items='center',
        justify_content='center'
    )

