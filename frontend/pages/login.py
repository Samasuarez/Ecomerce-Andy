import reflex as rx
from state import State
from components.layout import layout

def login() -> rx.Component:
    return layout(
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Iniciar sesión", size="6"),
                    rx.input(
                        placeholder="Email",
                        on_change=State.set_login_email,
                        value=State.login_email,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Contraseña",
                        type="password",
                        on_change=State.set_login_password,
                        value=State.login_password,
                        width="100%",
                    ),
                    rx.button(
                        "Ingresar",
                        on_click=State.login,
                        width="100%",
                    ),
                    spacing="4",
                ),
                padding="2em",
                width="100%",
                max_width="400px",
            )
        )
    )
