import reflex as rx
from state import State   

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
                height=["220px", "260px", "300px"],
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
                width="100%",
            ),  
            spacing="2",
            padding="3",
        ),
        width="100%",
        max_width="360px",
        transition="transform 0.2s ease, box-shadow 0.2s ease",
        _hover={
            "transform": "translateY(-6px)",
            "boxShadow": "0 12px 28px rgba(0,0,0,0.12)",
        },
    )







def index() -> rx.Component:
    return rx.vstack(
        navbar_searchbar(),

        rx.box(
            rx.grid(
                *[product_card(product) for product in PRODUCTS],
                columns=rx.breakpoints(
      initial="1fr",              # mobile
     sm="repeat(2, 1fr)",         # tablet
     md="repeat(3, 1fr)",         # laptop
     lg="repeat(4, 1fr)",         # desktop
),

                gap=["1rem", "1.5rem", "2rem"],
            ), 
            max_width="1400px",
            margin="0 auto",
            padding=["1em", "1.5em", "2em"],
            width="100%",
            # justify_items="center",

        ),

        footer(),
        width="100%",
        spacing="0",
    )



app = rx.App()
app.add_page(index)
app.add_page(cart, route="/cart")





