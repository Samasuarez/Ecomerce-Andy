import reflex as rx
from state import State


def cart_drawer() -> rx.Component:
    return rx.drawer.root(
        rx.drawer.trigger(
            rx.icon_button(
                rx.icon("shopping-cart"),
                variant="ghost",
            )
        ),

        rx.drawer.content(
            rx.vstack(
                rx.heading("Tu carrito", size="5"),

                rx.cond(
                    State.cart_count == 0,
                    rx.text("Tu carrito está vacío 🛍️"),
                    rx.vstack(
                        rx.text(f"Productos: {State.cart_count}"),
                        rx.text(
                            f"Total: ${State.cart_total:.2f}",
                            font_weight="bold",
                        ),
                        rx.button(
                            "Ver carrito",
                            on_click=rx.redirect("/cart"),
                            width="100%",
                        ),
                        spacing="3",
                    ),
                ),

                spacing="4",
                padding="1em",
            ),
            width=["100%", "420px"],
        ),

        open=State.cart_drawer_open,
        on_open_change=State.toggle_cart_drawer,
    )


