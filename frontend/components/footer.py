import reflex as rx
from ..state import State


def _link(text: str, href: str) -> rx.Component:
    return rx.link(text, href=href, color="#94A3B8", font_size="0.85rem",
                   _hover={"color": "white"})


def footer() -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                # Marca
                rx.vstack(
                    rx.hstack(
                        rx.icon("cross", color="#60A5FA", size=20),
                        rx.text("EUCA by Andrea", color="white", font_weight="800", font_size="1.2rem"),
                        spacing="2", align="center",
                    ),
                    rx.text("Tu tienda de confianza en\ninsumos y uniformes clínicos.",
                            color="#94A3B8", font_size="0.85rem", white_space="pre-line"),
                    spacing="3", align_items="start",
                ),

                # Categorías
                rx.vstack(
                    rx.text("PRODUCTOS", color="white", font_weight="700", font_size="0.85rem"),
                    _link("Ambos", "/products"),
                    _link("Calzado Clínico", "/products"),
                    _link("Accesorios", "/products"),
                    _link("Equipamiento", "/products"),
                    _link("Descartables", "/products"),
                    spacing="2", align_items="start",
                ),

                # Ayuda
                rx.vstack(
                    rx.text("MI CUENTA", color="white", font_weight="700", font_size="0.85rem"),
                    _link("Iniciar sesión", "/login"),
                    _link("Mi perfil", "/profile"),
                    _link("Mis pedidos", "/profile"),
                    _link("Mi carrito", "/cart"),
                    rx.cond(
                        State.is_admin,
                        _link("Panel Admin", "/admin"),
                    ),
                    spacing="2", align_items="start",
                ),

                justify="between",
                width="100%",
                flex_wrap="wrap",
                spacing="6",
            ),
            rx.divider(border_color="#334155", margin_y="1.5em"),
            rx.hstack(
                rx.text("© 2025 EUCA by Andrea — Todos los derechos reservados.",
                        color="#64748B", font_size="0.8rem"),
                rx.hstack(
                    rx.link("Instagram", href="/#", color="#64748B", font_size="0.8rem",
                            _hover={"color": "white"}),
                    rx.link("Facebook", href="/#", color="#64748B", font_size="0.8rem",
                            _hover={"color": "white"}),
                    spacing="4",
                ),
                justify="between",
                width="100%",
                flex_wrap="wrap",
            ),
            max_width="1280px",
            margin="0 auto",
            padding="2em 1.5em",
        ),
        background="#0F172A",
        width="100%",
    )
