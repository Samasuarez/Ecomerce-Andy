import reflex as rx
from state import State
from pages.cart import cart_drawer


def navbar_searchbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading("Shop", size="5"),
            rx.spacer(),

         
            rx.hstack(
                rx.link("Inicio", href="/"),
                rx.link(
                    rx.hstack(
                        rx.text("Carrito"),
                        rx.cond(
                            State.cart_count > 0,
                            rx.badge(
                                State.cart_count,
                                color_scheme="red",
                                radius="full",
                            ),
                        ),
                        spacing="1",
                        align="center",
                    ),
                    href="/cart",
                ),
                spacing="4",
                display=["none", "flex"],
            ),

            rx.hstack(
                cart_drawer(), 
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(
                            rx.icon("menu"),
                            variant="ghost",
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item("Inicio", on_click=rx.redirect("/")),
                        rx.menu.item("Carrito", on_click=rx.redirect("/cart")),
                    ),
                ),
                spacing="2",
                display=["flex", "none"],
            ),

            width="100%",
            align="center",
        ),
        padding=["1em", "1.5em", "2em"],
        border_bottom="1px solid #eee",
        width="100%",
    )

