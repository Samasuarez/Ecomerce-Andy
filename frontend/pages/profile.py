import reflex as rx
from state import State
from components.layout import layout
from components.styles import PROFILE_ROW_STYLE, TEXT_MUTED, LABEL_STYLE

def editable_row(label: str, value: str, setter, field_key: str):
    return rx.hstack(
        rx.text(f"{label}:", **LABEL_STYLE),
        rx.cond(
            State.editing_field == field_key,
            rx.hstack(
                rx.input(
                    value=value,
                    on_change=setter,
                    size="2",
                    width="220px",
                ),
                rx.button(
                    "Guardar",
                    size="2",
                    on_click=State.stop_edit,
                ),
                spacing="2",
            ),
            rx.hstack(
                rx.text(
                    value,
                    **TEXT_MUTED,
                    min_width="200px",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                ),
                rx.button(
                    "Editar",
                    size="1",
                    variant="ghost",
                    on_click=lambda: State.start_edit(field_key),
                ),
                spacing="2",
            ),
        ),
        padding="0.5em",
        border_radius="8px",
        background_color=rx.cond(
            State.editing_field == field_key,
            "gray.100",
            "transparent",
        ),

        align="center",
        width="100%",
    )

def profile() -> rx.Component:
    return layout(
        rx.center(
            rx.container(
                rx.cond(
                 ~State.profile_completed,
                    rx.card(
                        rx.vstack(
                            rx.heading("Completá tu perfil", size="6"),

                            rx.input(
                                placeholder="Nombre",
                                value=State.first_name,
                                on_change=State.set_first_name,
                            ),
                            rx.input(
                                placeholder="Apellido",
                                value=State.last_name,
                                on_change=State.set_last_name,
                            ),
                            rx.input(
                                placeholder="Teléfono",
                                value=State.phone,
                                on_change=State.set_phone,
                            ),
                            rx.input(
                                placeholder="Dirección",
                                value=State.address,
                                on_change=State.set_address,
                            ),

                            rx.button(
                                "Guardar datos",
                                on_click=State.save_profile,
                                width="100%",
                            ),

                            spacing="4",
                        ),
                        padding="2em",
                    ),                   
                    rx.card(
                        rx.vstack(
                            rx.heading("Mi perfil", size="6"),
                            editable_row(
                                "Nombre",
                                State.first_name,
                                State.set_first_name,
                                "first_name",
                            ),
                            editable_row(
                                "Apellido",
                                State.last_name,
                                State.set_last_name,
                                "last_name",
                            ),
                            editable_row(
                                "Teléfono",
                                State.phone,
                                State.set_phone,
                                "phone",
                            ),
                            editable_row(
                                "Dirección",
                                State.address,
                                State.set_address,
                                "address",
                            ),

                            spacing="4",
                        ),
                        padding="2em",
                    ),
                ),
                max_width="480px",
            ),
            padding="4em",
        )
    )


