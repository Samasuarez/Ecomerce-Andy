import reflex as rx
from ..state import State
from ..components.layout import layout


def editable_field(label: str, value, setter, field_key: str) -> rx.Component:
    return rx.box(
        rx.text(label, font_size="0.78rem", color="#64748B", font_weight="600", margin_bottom="0.25em"),
        rx.cond(
            State.editing_field == field_key,
            rx.hstack(
                rx.input(
                    value=value,
                    on_change=setter,
                    size="2",
                    flex="1",
                    border="1px solid #2563EB",
                    border_radius="6px",
                ),
                rx.button(
                    "Guardar",
                    on_click=State.stop_edit,
                    size="2",
                    background="#2563EB",
                    color="white",
                    border_radius="6px",
                ),
                spacing="2",
            ),
            rx.hstack(
                rx.text(
                    rx.cond(value != "", value, "—"),
                    flex="1",
                    color="#1E293B",
                    font_size="0.95rem",
                ),
                rx.button(
                    rx.icon("pencil", size=14),
                    on_click=State.start_edit(field_key),
                    size="1",
                    variant="ghost",
                    color="#94A3B8",
                    _hover={"color": "#2563EB"},
                ),
                spacing="2",
                align="center",
            ),
        ),
        padding="0.75em 1em",
        border_bottom="1px solid #F1F5F9",
        width="100%",
    )


def profile_data_tab() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon("user", size=28, color="#2563EB"),
                width="60px",
                height="60px",
                background="#EFF6FF",
                border_radius="50%",
            ),
            rx.vstack(
                rx.text(State.user_email, font_weight="600", font_size="0.95rem"),
                rx.text("Cuenta activa", color="#16A34A", font_size="0.8rem"),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        rx.divider(border_color="#E2E8F0"),
        rx.box(
            editable_field("Nombre completo", State.full_name, State.set_full_name, "full_name"),
            editable_field("Nombre", State.first_name, State.set_first_name, "first_name"),
            editable_field("Apellido", State.last_name, State.set_last_name, "last_name"),
            editable_field("DNI", State.dni, State.set_dni, "dni"),
            editable_field("Profesión", State.profession, State.set_profession, "profession"),
            editable_field("Teléfono", State.phone, State.set_phone, "phone"),
            editable_field("Provincia", State.province, State.set_province, "province"),
            editable_field("Ciudad", State.city, State.set_city, "city"),
            editable_field("Dirección", State.address, State.set_address, "address"),
            width="100%",
            border="1px solid #E2E8F0",
            border_radius="8px",
            overflow="hidden",
        ),
        rx.cond(
            ~State.profile_completed,
            rx.box(
                rx.hstack(
                    rx.icon("triangle-alert", size=15, color="#D97706"),
                    rx.text(
                        "Completá tu nombre para poder realizar pedidos.",
                        color="#92400E",
                        font_size="0.85rem",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.button(
                    "Guardar perfil",
                    on_click=State.save_profile,
                    size="2",
                    background="#D97706",
                    color="white",
                    border_radius="6px",
                    margin_top="0.5em",
                ),
                background="#FEF9C3",
                border="1px solid #FDE68A",
                border_radius="8px",
                padding="1em",
                width="100%",
            ),
        ),
        spacing="4",
        width="100%",
    )


def order_status_badge(status: str) -> rx.Component:
    return rx.badge(status, color_scheme="blue", radius="full", font_size="0.75rem")


def order_card(order: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text("Pedido", font_size="0.75rem", color="#94A3B8", font_weight="600"),
                rx.text(order["created_at"], font_size="0.8rem", color="#64748B"),
                spacing="0",
                align="start",
            ),
            rx.badge(order["status"], color_scheme="blue", radius="full", font_size="0.75rem"),
            rx.text("$", order["total"], font_weight="700", color="#2563EB"),
            justify="between",
            align="center",
            width="100%",
        ),
        background="white",
        border="1px solid #E2E8F0",
        border_radius="8px",
        padding="1em",
        width="100%",
        _hover={"border_color": "#CBD5E1"},
        transition="border-color 0.15s ease",
    )


def orders_tab() -> rx.Component:
    return rx.vstack(
        rx.cond(
            State.my_orders.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("package", size=44, color="#CBD5E1"),
                    rx.text("Todavía no realizaste pedidos", color="#64748B"),
                    rx.button(
                        "Ir a la tienda",
                        on_click=rx.redirect("/products"),
                        variant="ghost",
                        color="#2563EB",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="3em",
                width="100%",
            ),
            rx.foreach(State.my_orders, order_card),
        ),
        spacing="3",
        width="100%",
    )


def profile() -> rx.Component:
    return layout(
        rx.cond(
            State.is_logged_in,
            rx.box(
                rx.vstack(
                    rx.heading("Mi cuenta", size="6", color="#1E293B"),
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger(
                                rx.hstack(rx.icon("user", size=15), rx.text("Mis datos"), spacing="2", align="center"),
                                value="profile",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(rx.icon("package", size=15), rx.text("Mis pedidos"), spacing="2", align="center"),
                                value="orders",
                            ),
                            mb="4",
                        ),
                        rx.tabs.content(
                            profile_data_tab(),
                            value="profile",
                        ),
                        rx.tabs.content(
                            orders_tab(),
                            value="orders",
                        ),
                        default_value="profile",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                max_width="640px",
                margin="0 auto",
                padding_y="2em",
                width="100%",
            ),
            rx.center(
                rx.vstack(
                    rx.icon("lock", size=44, color="#94A3B8"),
                    rx.heading("Iniciá sesión para ver tu perfil", size="5"),
                    rx.button(
                        "Iniciar sesión",
                        on_click=rx.redirect("/login"),
                        background="#2563EB",
                        color="white",
                        border_radius="8px",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="4em 1em",
                width="100%",
            ),
        )
    )
