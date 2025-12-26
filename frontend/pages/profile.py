import reflex as rx
from state import State
from components.layout import layout

def profile() -> rx.Component:
    return layout(
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Mi perfil", size="6"),
                    rx.text(f"Email: {State.user_email}"),
                    rx.input(placeholder="Nombre"),
                    rx.input(placeholder="Apellido"),
                    rx.button("Guardar"),
                    spacing="4",
                ),
                padding="2em",
                max_width="400px",
                width="100%",
            )
        )
    )

