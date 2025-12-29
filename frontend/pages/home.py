import reflex as rx
from state import State
from data import PRODUCTS
from components.layout import layout



def hero_section() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading(
                    "Bienvenidos a Shop Andy",
                    size="8",
                    text_align="center",
                ),
                rx.text(
                    "Comprá productos seleccionados con una experiencia simple y moderna.",
                    size="4",
                    color="gray",
                    text_align="center",
                    max_width="600px",
                ),
                rx.button(
                    "Ver productos",
                    on_click=rx.redirect("/products"),
                    size="4",
                    _hover={"transform": "scale(1.05)"},
                ),
                spacing="5",
            ),
        ),
        padding_y="6em",
        width="100%",
    )



def promo_banners() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.vstack(
                rx.text("Nueva colección", font_weight="bold"),
                rx.text("Hasta 30% OFF", color="gray"),
            ),
            padding="2em",
            border_radius="14px",
            background="linear-gradient(135deg, #e5e7eb, #f9fafb)",
            width="100%",
            _hover={"transform": "scale(1.04)"},
            transition="all 0.2s ease",
        ),
        rx.box(
            rx.vstack(
                rx.text("Envíos rápidos", font_weight="bold"),
                rx.text("A todo el país", color="gray"),
            ),
            padding="2em",
            border_radius="14px",
            background="linear-gradient(135deg, #f1f5f9, #ffffff)",
            width="100%",
            _hover={"transform": "scale(1.04)"},
            transition="all 0.2s ease",
        ),
        rx.box(
            rx.vstack(
                rx.text("Pagos seguros", font_weight="bold"),
                rx.text("Tarjeta o transferencia", color="gray"),
            ),
            padding="2em",
            border_radius="14px",
            background="linear-gradient(135deg, #e5e7eb, #f9fafb)",
            width="100%",
            _hover={"transform": "scale(1.04)"},
            transition="all 0.2s ease",
        ),
        spacing="4",
        width="100%",
    )




def product_card(product: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.box(
                height="140px",
                width="100%",
                background_color="gray.200",
                border_radius="10px",
            ),
            rx.text(product["name"], font_weight="bold"),
            rx.text(f"${product['price']}", color="gray"),
            rx.button(
                "Agregar al carrito",
                on_click=lambda: State.add_to_cart(product["id"]),
                size="2",
                width="100%",
            ),
            spacing="3",
        ),
        padding="1.5em",
        _hover={
            "transform": "translateY(-6px)",
            "boxShadow": "0 12px 30px rgba(0,0,0,0.08)",
        },
        transition="all 0.2s ease",
    )



def featured_products() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Productos destacados",
            size="6",
            text_align="center",
        ),

        rx.grid(
            rx.foreach(PRODUCTS[:4], product_card),

            columns=rx.breakpoints(
                initial="1",   
                sm="2",        
                md="4",      
            ),

            gap="6",
            width="100%",
            justify_items="center",
        ),

        spacing="5",
        width="100%",
    )




def benefits_section() -> rx.Component:
    return rx.grid(
        rx.vstack(
            rx.icon("truck", size=32),
            rx.heading("Envíos rápidos", size="4"),
            rx.text("Recibí tus productos en tiempo récord."),
            align="center",
            spacing="2",
        ),
        rx.vstack(
            rx.icon("shield-check", size=32),
            rx.heading("Pagos seguros", size="4"),
            rx.text("Tus datos siempre protegidos."),
            align="center",
            spacing="2",
        ),
        rx.vstack(
            rx.icon("star", size=32),
            rx.heading("Calidad garantizada", size="4"),
            rx.text("Productos seleccionados."),
            align="center",
            spacing="2",
        ),
        columns=rx.breakpoints(
            initial="1",
            md="3",
        ),
        gap="4",
        width="100%",
        padding="4em 0",
        text_align="center",
    )

def section_container(content: rx.Component) -> rx.Component:
    return rx.box(
        content,
        width="100%",
        max_width="1100px",
        margin="0 auto",
        padding_x="1.5em",
    )


def home() -> rx.Component:
    return layout(
        rx.vstack(
            hero_section(),

            section_container(
                rx.vstack(
                    promo_banners(),
                    featured_products(),
                    benefits_section(),
                    spacing="6",
                )
            ),

            spacing="0",
            width="100%",
        )
    )

