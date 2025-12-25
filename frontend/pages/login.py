import reflex as rx
from state import State
from components.nav import navbar_searchbar
from components.footer import footer


def login() -> rx.Component:
    return rx.vstack(
        navbar_searchbar(),

        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Iniciar sesión", size="6"),

                    rx.input(
                        placeholder="Email",
                        type="email",
                        value=State.login_email,
                        on_change=State.set_login_email,
                        width="100%",
                    ),

                    rx.input(
                        placeholder="Contraseña",
                        type="password",
                        value=State.login_password,
                        on_change=State.set_login_password,
                        width="100%",
                    ),

                    rx.button(
                        "Ingresar",
                        size="3",
                        width="100%",
                        on_click=State.login,
                    ),

                    spacing="4",
                ),
                width="100%",
                max_width="400px",
                padding="2em",
            ),
            height="70vh",
        ),

        footer(),
        width="100%",
        spacing="0",
    )
