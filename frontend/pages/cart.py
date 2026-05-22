import reflex as rx
from ..state import State
from ..components.layout import layout


def cart_item_row(item: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon("package", color="#94A3B8", size=26),
                width="64px",
                height="64px",
                background="#F1F5F9",
                border_radius="8px",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(item["name"], font_weight="600", font_size="0.95rem", color="#1E293B"),
                rx.text("$", item["price"], color="#2563EB", font_weight="600", font_size="0.95rem"),
                spacing="1",
                align="start",
                flex="1",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("minus", size=13),
                    on_click=State.decrease_qty(item["id"]),
                    size="1",
                    variant="soft",
                    radius="full",
                ),
                rx.text(
                    item["qty"],
                    font_weight="700",
                    min_width="24px",
                    text_align="center",
                    font_size="0.95rem",
                ),
                rx.icon_button(
                    rx.icon("plus", size=13),
                    on_click=State.increase_qty(item["id"]),
                    size="1",
                    variant="soft",
                    radius="full",
                ),
                spacing="2",
                align="center",
            ),
            rx.vstack(
                rx.text("$", item["total"], font_weight="700", color="#1E293B"),
                rx.button(
                    rx.icon("trash-2", size=14),
                    on_click=State.remove_from_cart(item["id"]),
                    size="1",
                    variant="ghost",
                    color_scheme="red",
                ),
                align="end",
                spacing="1",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        background="white",
        border="1px solid #E2E8F0",
        border_radius="8px",
        padding="1em",
        width="100%",
    )


def order_summary_box() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Resumen del pedido", font_weight="700", font_size="1.05rem", color="#1E293B"),
            rx.divider(border_color="#E2E8F0"),
            rx.hstack(
                rx.text("Subtotal", color="#475569"),
                rx.text(State.cart_total_fmt, font_weight="600"),
                justify="between",
                width="100%",
            ),
            rx.hstack(
                rx.text("Envío", color="#475569"),
                rx.hstack(
                    rx.icon("truck", size=14, color="#16A34A"),
                    rx.text("Gratis", color="#16A34A", font_weight="600"),
                    spacing="1", align="center",
                ),
                justify="between",
                width="100%",
            ),
            rx.divider(border_color="#E2E8F0"),
            rx.hstack(
                rx.text("Total", font_weight="700", font_size="1.1rem"),
                rx.text(State.cart_total_fmt, font_weight="700", font_size="1.1rem", color="#2563EB"),
                justify="between",
                width="100%",
            ),
            rx.cond(
                State.order_error != "",
                rx.hstack(
                    rx.icon("triangle-alert", size=15, color="#DC2626"),
                    rx.text(State.order_error, color="#DC2626", font_size="0.85rem"),
                    spacing="1",
                ),
            ),
            rx.cond(
                State.mp_checkout_error != "",
                rx.hstack(
                    rx.icon("triangle-alert", size=15, color="#DC2626"),
                    rx.text(State.mp_checkout_error, color="#DC2626", font_size="0.85rem"),
                    spacing="1",
                ),
            ),
            rx.button(
                rx.cond(
                    State.mp_checkout_loading,
                    rx.hstack(rx.spinner(size="2"), rx.text("Redirigiendo..."), spacing="2", align="center"),
                    rx.hstack(
                        rx.icon("credit-card", size=16),
                        rx.text("Pagar con MercadoPago"),
                        spacing="2",
                        align="center",
                    ),
                ),
                on_click=State.go_to_mp_checkout,
                width="100%",
                size="3",
                background="#009EE3",
                color="white",
                border_radius="8px",
                font_weight="600",
                _hover={"background": "#0081C2"},
                disabled=State.mp_checkout_loading,
            ),
            rx.button(
                rx.cond(
                    State.order_placing,
                    rx.hstack(rx.spinner(size="2"), rx.text("Procesando..."), spacing="2", align="center"),
                    rx.text("Confirmar sin pagar"),
                ),
                on_click=State.place_order,
                width="100%",
                size="2",
                variant="outline",
                border_radius="8px",
                font_weight="500",
                color="#64748B",
                disabled=State.order_placing,
            ),
            spacing="3",
            width="100%",
        ),
        background="white",
        border="1px solid #E2E8F0",
        border_radius="12px",
        padding="1.5em",
        min_width="260px",
        max_width=["100%", "100%", "320px"],
        position=["static", "static", "sticky"],
        top="90px",
        align_self="flex-start",
    )


def cart() -> rx.Component:
    return layout(
        rx.cond(
            State.is_logged_in,
            rx.cond(
                State.order_success,
                rx.center(
                    rx.vstack(
                        rx.icon("circle-check", size=60, color="#16A34A"),
                        rx.heading("¡Pedido confirmado!", size="6", color="#1E293B"),
                        rx.text(
                            "Tu pedido fue procesado correctamente.",
                            color="#64748B",
                            text_align="center",
                        ),
                        rx.text(
                            "ID: ", State.last_order_id,
                            color="#94A3B8",
                            font_size="0.8rem",
                            text_align="center",
                        ),
                        rx.hstack(
                            rx.button(
                                "Mis pedidos",
                                on_click=rx.redirect("/profile"),
                                background="#2563EB",
                                color="white",
                                border_radius="8px",
                            ),
                            rx.button(
                                "Seguir comprando",
                                on_click=[State.reset_order_success, rx.redirect("/products")],
                                variant="outline",
                                border_radius="8px",
                            ),
                            spacing="3",
                            flex_wrap="wrap",
                            justify="center",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    padding="4em 1em",
                    width="100%",
                ),
                rx.cond(
                    State.cart_count == 0,
                    rx.center(
                        rx.vstack(
                            rx.icon("shopping-cart", size=52, color="#94A3B8"),
                            rx.heading("Tu carrito está vacío", size="5", color="#1E293B"),
                            rx.text("Agregá productos para comenzar", color="#64748B"),
                            rx.button(
                                "Ver productos",
                                on_click=rx.redirect("/products"),
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
                    rx.hstack(
                        rx.vstack(
                            rx.hstack(
                                rx.heading("Mi carrito", size="5", color="#1E293B"),
                                rx.badge(State.cart_count, color_scheme="blue", radius="full"),
                                spacing="2",
                                align="center",
                            ),
                            rx.foreach(State.cart, cart_item_row),
                            spacing="3",
                            width="100%",
                            flex="1",
                            min_width="0",
                        ),
                        order_summary_box(),
                        spacing="5",
                        align="start",
                        flex_wrap="wrap",
                        width="100%",
                    ),
                ),
            ),
            rx.center(
                rx.vstack(
                    rx.icon("lock", size=44, color="#94A3B8"),
                    rx.heading("Iniciá sesión para ver tu carrito", size="5", color="#1E293B"),
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
