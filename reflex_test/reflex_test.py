# Imports

import reflex as rx

from .backend.backend import State
from .components.stats_cards import stats_cards_group
from .views.navbar import navbar
from .views.table import main_table

# End Imports


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(
            rx.markdown(f"**Your ip address:** ```{State.router.session.client_ip}```"),
            display='flex',
            width='100%',
            align_items='center',
            justify_content='center'
        ),

        stats_cards_group(),
        rx.box(
            main_table(),
            width="100%",
        ),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="grass"
    ),
)

app.add_page(
    index,
    title="Simple Quiz App",
    description="A simple quiz app to test your python / programming knowledge.",
)
