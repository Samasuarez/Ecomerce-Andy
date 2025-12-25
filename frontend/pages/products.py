import reflex as rx
from data import PRODUCTS
from components.nav import navbar_searchbar
from components.footer import footer
from components.product_card import product_card


def products() -> rx.Component:
    return rx.vstack(
        navbar_searchbar(),

        rx.box(
            rx.grid(
                *[product_card(product) for product in PRODUCTS],
                columns=rx.breakpoints(
                    initial="1fr",
                    sm="repeat(2, 1fr)",
                    md="repeat(3, 1fr)",
                    lg="repeat(4, 1fr)",
                ),
                gap=["1rem", "1.5rem", "2rem"],
                justify_items="center",
            ),
            max_width="1400px",
            margin="0 auto",
            padding=["1em", "1.5em", "2em"],
            width="100%",
        ),

        footer(),
        width="100%",
        spacing="0",
    )
