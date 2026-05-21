import reflex as rx
from ..state import State
from ..components.nav import navbar_searchbar
from ..components.footer import footer
from ..components.product_card import product_card

CATS_HOME = [
    ("ambos", "Ambos", "layers"),
    ("calzado_clinico", "Calzado Clínico", "tag"),
    ("accesorios", "Accesorios", "star"),
    ("equipamiento", "Equipamiento", "activity"),
    ("descartables", "Descartables", "package"),
    ("ropa_clinica", "Ropa Clínica", "heart"),
]


def hero_section() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.icon("cross", color="#93C5FD", size=24),
                    rx.text("NurseShop", color="white", font_size="1.4rem", font_weight="800"),
                    spacing="2", align="center",
                ),
                rx.heading(
                    "Todo para el profesional de la salud",
                    size="8",
                    color="white",
                    text_align="center",
                ),
                rx.text(
                    "Ambos, calzado clínico, accesorios y equipamiento. Calidad garantizada.",
                    color="#CBD5E1",
                    text_align="center",
                    max_width="520px",
                    font_size="1.05rem",
                ),
                rx.hstack(
                    rx.button(
                        "Ver productos",
                        on_click=rx.redirect("/products"),
                        size="3",
                        background="#2563EB",
                        color="white",
                        border_radius="8px",
                        _hover={"background": "#1D4ED8"},
                    ),
                    rx.cond(
                        ~State.is_logged_in,
                        rx.button(
                            "Crear cuenta",
                            on_click=rx.redirect("/login"),
                            size="3",
                            variant="outline",
                            color="white",
                            border="1px solid rgba(255,255,255,0.5)",
                            background="transparent",
                            _hover={"background": "rgba(255,255,255,0.1)"},
                        ),
                    ),
                    spacing="3",
                    flex_wrap="wrap",
                    justify="center",
                ),
                spacing="5",
                align="center",
                max_width="700px",
                padding_x="1em",
            ),
            padding_y=["3em", "4em", "5em"],
        ),
        background="linear-gradient(135deg, #1E3A8A 0%, #1e2d5a 100%)",
        width="100%",
    )


def cat_card(slug: str, label: str, icon: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.icon(icon, size=28, color="#2563EB"),
            rx.text(label, font_weight="600", font_size="0.85rem", color="#1E293B", text_align="center"),
            spacing="2",
            align="center",
        ),
        background="white",
        border="1.5px solid #E2E8F0",
        border_radius="10px",
        padding="1.25em 0.5em",
        cursor="pointer",
        on_click=State.go_to_category(slug),
        _hover={"border_color": "#2563EB", "box_shadow": "0 2px 12px rgba(37,99,235,0.12)"},
        transition="all 0.15s ease",
        text_align="center",
        width="100%",
    )


def category_section() -> rx.Component:
    return rx.vstack(
        rx.text(
            "EXPLORAR POR CATEGORÍA",
            font_weight="700",
            font_size="0.75rem",
            color="#64748B",
            letter_spacing="0.1em",
        ),
        rx.heading("Nuestras categorías", size="6", color="#1E293B"),
        rx.grid(
            *[cat_card(slug, label, icon) for slug, label, icon in CATS_HOME],
            columns=rx.breakpoints(initial="2", sm="3", md="6"),
            gap="4",
            width="100%",
        ),
        spacing="3",
        align="center",
        width="100%",
    )


def featured_section() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text(
                    "LO MÁS VENDIDO",
                    font_weight="700",
                    font_size="0.75rem",
                    color="#64748B",
                    letter_spacing="0.1em",
                ),
                rx.heading("Productos destacados", size="6", color="#1E293B"),
                spacing="1",
                align="start",
            ),
            rx.link(
                rx.hstack(
                    rx.text("Ver todos", color="#2563EB", font_size="0.9rem", font_weight="600"),
                    rx.icon("arrow-right", size=16, color="#2563EB"),
                    spacing="1",
                    align="center",
                ),
                href="/products",
            ),
            justify="between",
            align="end",
            width="100%",
        ),
        rx.cond(
            State.featured_products.length() == 0,
            rx.center(rx.spinner(size="3"), padding="4em"),
            rx.grid(
                rx.foreach(State.featured_products, product_card),
                columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                gap="4",
                width="100%",
            ),
        ),
        spacing="4",
        width="100%",
    )


def benefits_strip() -> rx.Component:
    def benefit(icon: str, title: str, subtitle: str) -> rx.Component:
        return rx.vstack(
            rx.icon(icon, size=28, color="#2563EB"),
            rx.text(title, font_weight="600", font_size="0.95rem"),
            rx.text(subtitle, color="#64748B", font_size="0.82rem", text_align="center"),
            spacing="2",
            align="center",
            flex="1",
            min_width="160px",
        )

    return rx.hstack(
        benefit("truck", "Envío a todo el país", "Rápido y seguro"),
        benefit("shield-check", "Compra protegida", "Garantía en todos los productos"),
        benefit("star", "Calidad profesional", "Para profesionales de la salud"),
        background="white",
        border_radius="12px",
        border="1px solid #E2E8F0",
        padding="2em",
        width="100%",
        justify="between",
        flex_wrap="wrap",
        spacing="4",
    )


def home() -> rx.Component:
    return rx.box(
        navbar_searchbar(),
        hero_section(),
        rx.box(
            rx.vstack(
                category_section(),
                featured_section(),
                benefits_strip(),
                spacing="8",
                width="100%",
            ),
            max_width="1280px",
            margin="0 auto",
            padding=["1.5em 1em", "2em 1.5em"],
            width="100%",
        ),
        footer(),
        background="#F1F5F9",
        width="100%",
        min_height="100vh",
        spacing="0",
    )
