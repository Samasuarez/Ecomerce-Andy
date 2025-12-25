import reflex as rx
from state import State
from components.nav import navbar_searchbar
from components.footer import footer


def home() -> rx.Component:
    return rx.vstack(
        navbar_searchbar(),

        # HERO
        rx.center(
            rx.vstack(
                rx.heading(
                    "Bienvenidos a Shop Andy",
                    size="7",
                    text_align="center",
                ),
                rx.text(
                    "Tienda Online",
                    size="4",
                    color="gray",
                    text_align="center",
                ),
                 rx.text(
                    f"Usuario: {State.user_email}",
                    color="gray",
                ),
                rx.button(
                    "Ver productos",
                    on_click=rx.redirect("/products"),
                    size="3",
                ),
                spacing="4",
            ),
            height="70vh",
            padding="2em",
        ),

        footer(),
        width="100%",
        spacing="0",
    )
