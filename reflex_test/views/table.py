# Imports

import reflex as rx
from ..backend.backend import State


# End Imports

def quiz_container() -> rx.Component:

    """
    Quiz main container
    """

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon('circle-help', size=26),
                rx.markdown(
                    State.question_text
                ),

                display='flex',
                gap='.5em',
                align_items='center'
            ),
            rx.el.div(
                rx.markdown(
                    State.question_code_part
                )
            ),
            rx.radio_group(
                items=State.question_options,
                on_change=State.set_option,
                direction='column',
                value=State.selected_option,
                spacing='4',
                padding="10px",
                border_radius="8px",
                margin=".5em 0",
                box_shadow="rgba(151, 65, 252, 0.8) 0 5px 15px -5px",
                background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                color="white",
                _hover={
                    "opacity": 0.8,
                },

            ),

            # Display the selected option
            rx.text(
                rx.cond(
                    State.selected_option,
                    rx.el.b(f"Selected option: {State.selected_option}"),
                ),
                margin="1em 0"
            ),
            rx.text(
                rx.el.b(f"{State.message}"),
                margin="1em 0"
            ),
            rx.flex(
                rx.button(
                    "Submit",
                    on_click=lambda: State.submit_selection()
                ),
                rx.button(
                    "Next Question",

                    rx.icon(
                        "arrow-right", size=16
                    ),
                    color_scheme='cyan',
                    on_click=lambda: State.fetch_question()
                ),
                justify_content='space-between',
                margin_top='1em',
                gap='2em'
            ),

            align="center"
        ),
        width=rx.breakpoints(
            {
                "initial": "100%",
                "sm": "600px",
                "md": "600px",
                "lg": "600px",
                "xl": "600px",
            }
        ),
        border_radius='4px',
        background_color='#147d94',
        color='white',
        display='flex',
        justify_content='center',
        align_items='center',
        padding='1em',
        margin='1em 0'
    )


def start_quiz_button() -> rx.Component:

    """
    Template codes for starting quiz
    """

    return rx.el.div(

        rx.button(
            rx.cond(
                State.start_quiz,
                rx.icon("pause", size=20),
                rx.icon("play", size=20)
            ),
            rx.text(State.player_button_text, size='4'),
            on_click=lambda: State.enable_quiz(),
            size='3',
            color_scheme=rx.cond(State.start_quiz, "orange", "blue"),
            cursor='pointer',
            width='fit-content'
        ),
        width='fit-content',
        margin='auto'

    )


def main_table():
    return rx.el.div(
        rx.el.div(
            start_quiz_button(),
            rx.cond(
                State.start_quiz,
                rx.cond(
                    State.question_loading,
                    rx.text("Loading question ..."),
                    quiz_container()
                )

            )
        ),
        width='100%',
        display='flex',
        justify_content='center',
        align_items='center',
        margin='1em 0'

    )
