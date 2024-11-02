import reflex as rx


def navbar():
    return rx.el.div(
        rx.el.div(
            rx.badge(
                rx.icon(tag="message-circle-question", size=28),
                rx.heading("Quiz App", size="6"),
                color_scheme="green",
                radius="large",
                align="center",
                variant="surface",
                padding="0.65rem",
            ),
            rx.spacer(),
            rx.hstack(
                rx.color_mode.button(),
                align="center",
                spacing="3",
            ),
            spacing="2",
            flex_direction="row",
            align="center",

            top="0px",
            padding_top="2em",
            display='flex',
            gap='1em'

        ),
        display='flex',
        justify_content='center',
        align_items='center',
        width='100%',
    )
