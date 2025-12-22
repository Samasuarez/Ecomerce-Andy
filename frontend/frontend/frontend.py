import reflex as rx
from state import State   # ← ESTE MISMO State

from data import PRODUCTS
from components.nav import navbar_searchbar
from components.footer import footer
from pages.cart import cart

def product_card(product: dict) -> rx.Component:
    return rx.card(
        rx.inset(
            rx.image(
                src=product["image"],
                width="100%",
                height="300px",
                object_fit="cover",
            ),
            side="top",
            pb="current",
        ),
        rx.vstack(
            rx.heading(product["name"], size="4"),
            rx.text(f"${product['price']:.2f}", weight="bold"),
           rx.button(
    "Agregar al carrito",
    on_click=lambda: State.add_to_cart(product["id"]),
),
            spacing="2",
            padding="3",
        ),
        max_width="360px",   # CLAVE
        width="100%",
    )





def index() -> rx.Component:
    return rx.vstack(
        navbar_searchbar(),

        rx.box(

            rx.grid(
                *[product_card(product) for product in PRODUCTS],
                columns="repeat(4, 1fr)",
                gap="2rem",
            ),
            max_width="1400px",
            margin="0 auto",
            padding="2em",
            width="100%",
        ),

        footer(),
        width="100%",
        spacing="0",
    )


app = rx.App()
app.add_page(index)
app.add_page(cart, route="/cart")





