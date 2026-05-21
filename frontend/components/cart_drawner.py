import reflex as rx
from ..state import State


def cart_drawer() -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon("shopping-cart", color="white", size=22),
            rx.cond(
                State.cart_count > 0,
                rx.badge(
                    State.cart_count,
                    color_scheme="red",
                    radius="full",
                    font_size="0.7rem",
                ),
            ),
            spacing="1",
            align="center",
        ),
        href="/cart",
    )
