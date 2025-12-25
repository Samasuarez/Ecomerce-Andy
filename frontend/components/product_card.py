import reflex as rx
from state import State

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

