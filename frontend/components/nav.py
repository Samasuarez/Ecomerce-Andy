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

               
                rx.cond(
                    State.is_logged_in,

                  
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button(
                                State.user_email,
                                variant="ghost",
                                size="2",
                            )
                        ),
                        rx.menu.content(
    rx.menu.item(
        "Perfil",
        on_click=rx.redirect("/profile"),
    ),
    rx.menu.item(
        "Cerrar sesión",
        on_click=State.logout,
    ),
),
  ),

                    rx.link("Login", href="/login"),
                ),

                rx.link("Carrito", href="/cart"),
                spacing="4",
                align="center",
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
                        rx.cond(
                            State.is_logged_in,
                            rx.menu.item(
                                "Cerrar sesión",
                                on_click=State.logout,
                            ),
                            rx.menu.item(
                                "Login",
                                on_click=rx.redirect("/login"),
                            ),
                        ),
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

