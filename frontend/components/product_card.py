import reflex as rx
from ..state import State

DEFAULT_BG = "linear-gradient(135deg,#F1F5F9,#E2E8F0)"


def product_card(product: dict) -> rx.Component:
    return rx.box(
        # Imagen placeholder
        rx.box(
            rx.center(
                rx.icon("package", color="#94A3B8", size=40),
                width="100%",
                height="100%",
            ),
            background=DEFAULT_BG,
            width="100%",
            height="180px",
            overflow="hidden",
            border_radius="10px 10px 0 0",
            cursor="pointer",
            on_click=State.go_to_product(product["id"]),
        ),

        rx.vstack(
            # Badge envío gratis
            rx.cond(
                product["price"].to(float) > 40,
                rx.hstack(
                    rx.icon("truck", size=12, color="#16A34A"),
                    rx.text("Envío gratis", color="#16A34A", font_size="0.72rem", font_weight="600"),
                    spacing="1",
                    align="center",
                ),
            ),

            # Nombre
            rx.text(
                product["name"],
                font_weight="600",
                font_size="0.9rem",
                color="#1E293B",
                cursor="pointer",
                on_click=State.go_to_product(product["id"]),
                overflow="hidden",
                display="-webkit-box",
                style={"-webkit-line-clamp": "2", "-webkit-box-orient": "vertical"},
                min_height="2.5em",
            ),

            # Precio
            rx.text(
                "$", product["price"],
                font_size="1.25rem",
                font_weight="700",
                color="#1E293B",
            ),

            # Botones
            rx.vstack(
                rx.button(
                    rx.hstack(
                        rx.icon("shopping-cart", size=14),
                        rx.text("Agregar al carrito"),
                        spacing="2",
                        align="center",
                    ),
                    on_click=State.add_to_cart(product["id"]),
                    width="100%",
                    background="#2563EB",
                    color="white",
                    border_radius="6px",
                    font_size="0.82rem",
                    font_weight="600",
                    _hover={"background": "#1D4ED8"},
                ),
                rx.button(
                    "Ver detalle",
                    on_click=State.go_to_product(product["id"]),
                    width="100%",
                    variant="outline",
                    border="1px solid #E2E8F0",
                    color="#475569",
                    border_radius="6px",
                    font_size="0.82rem",
                    background="transparent",
                    _hover={"background": "#F1F5F9", "border_color": "#CBD5E1"},
                ),
                spacing="2",
                width="100%",
            ),

            spacing="2",
            padding="0.85em",
            align="start",
            width="100%",
        ),

        background="white",
        border_radius="10px",
        border="1px solid #E2E8F0",
        width="100%",
        transition="box-shadow 0.2s ease",
        _hover={"box_shadow": "0 4px 20px rgba(0,0,0,0.10)"},
        overflow="hidden",
    )
