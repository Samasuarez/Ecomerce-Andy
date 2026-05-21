import reflex as rx
from .nav import navbar_searchbar
from .footer import footer


def layout(content: rx.Component) -> rx.Component:
    return rx.box(
        navbar_searchbar(),
        rx.box(
            content,
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding=["1em", "1.5em", "2em"],
            min_height="70vh",
        ),
        footer(),
        background="#F1F5F9",
        width="100%",
        min_height="100vh",
    )
