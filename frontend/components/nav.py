import reflex as rx
from state import State
from components.cart_drawner import cart_drawer

def navbar_searchbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading("Shop", size="5", color="white"),
            rx.spacer(),

            rx.hstack(
                rx.link("Inicio", href="/", color="gray.200"),
                rx.link("Productos", href="/products", color="gray.200"),

                rx.cond(
                    State.is_logged_in,
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button(
                                State.user_email,
                                variant="ghost",
                                color="gray.200",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item("Perfil", on_click=rx.redirect("/profile")),
                            rx.menu.item("Cerrar sesión", on_click=State.logout),
                        ),
                    ),
                    rx.link("Login", href="/login", color="gray.200"),
                ),

                rx.link(
    rx.hstack(
        rx.text("Carrito", color="gray.200"),
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
     rx.color_mode.button(),


                

                spacing="5",
                align="center",
                display=["none", "flex"],
            ),

            rx.hstack(
                cart_drawer(),
                display=["flex", "none"],
            ),

            width="100%",
            align="center",
        ),
        padding="1.5em",
        background_color="#0f172a",
        width="100%",
    )

