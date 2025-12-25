import reflex as rx
from state import State
from components.nav import navbar_searchbar
from components.footer import footer


def profile() -> rx.Component:
    return rx.vstack(
        navbar_searchbar(),

        rx.center(
            rx.container(
                rx.vstack(
                    rx.heading("Mi perfil", size="6"),

                    rx.text(
                        f"Email: {State.user_email}",
                        color="gray",
                    ),

                    rx.divider(),

                    rx.input(
                        placeholder="Nombre",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Apellido",
                        width="100%",
                    ),

                    rx.button(
                        "Guardar cambios",
                        width="100%",
                    ),

                    spacing="4",
                ),
                max_width="480px",
                padding="2em",
            ),
        ),

        footer(),
        width="100%",
        spacing="0",
    )
