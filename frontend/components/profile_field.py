import reflex as rx
from state import State

def profile_field(label: str, value: str, setter, field_key: str) -> rx.Component:
    return rx.hstack(
        rx.text(f"{label}:", font_weight="bold", width="140px"),
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
                rx.text(value or "—", color="gray"),
                rx.button(
                    "Editar",
                    size="1",
                    variant="ghost",
                    on_click=lambda: State.start_edit(field_key),
                ),
                spacing="2",
            ),
        ),
        spacing="3",
        align="center",
        width="100%",
    )
