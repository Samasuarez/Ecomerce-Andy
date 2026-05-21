import reflex as rx
from ..state import State
from ..components.layout import layout
from ..components.product_card import product_card

CATS_FILTER = [
    ("", "Todos"),
    ("ambos", "Ambos"),
    ("calzado_clinico", "Calzado Clínico"),
    ("accesorios", "Accesorios"),
    ("equipamiento", "Equipamiento"),
    ("descartables", "Descartables"),
    ("ropa_clinica", "Ropa Clínica"),
]


def cat_pill(slug: str, label: str) -> rx.Component:
    active = State.selected_category == slug
    return rx.button(
        label,
        on_click=State.set_category_filter(slug),
        background=rx.cond(active, "#2563EB", "white"),
        color=rx.cond(active, "white", "#475569"),
        border=rx.cond(active, "1px solid #2563EB", "1px solid #E2E8F0"),
        border_radius="999px",
        font_size="0.82rem",
        font_weight=rx.cond(active, "600", "400"),
        padding="0.35em 1em",
        cursor="pointer",
        _hover={"background": rx.cond(active, "#1D4ED8", "#F1F5F9")},
        white_space="nowrap",
        height="auto",
    )


def products() -> rx.Component:
    return layout(
        rx.vstack(
            # Category pills — always visible
            rx.hstack(
                *[cat_pill(slug, label) for slug, label in CATS_FILTER],
                spacing="2",
                flex_wrap="wrap",
                width="100%",
            ),

            # Sort row
            rx.hstack(
                rx.hstack(
                    rx.text(
                        State.filtered_products.length(),
                        " productos encontrados",
                        color="#64748B",
                        font_size="0.9rem",
                    ),
                    rx.cond(
                        State.selected_category != "",
                        rx.button(
                            rx.hstack(rx.icon("x", size=12), rx.text("Limpiar filtro"), spacing="1", align="center"),
                            on_click=State.clear_category_filter,
                            size="1",
                            variant="ghost",
                            color="#2563EB",
                            padding="0.2em 0.5em",
                        ),
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.select.root(
                    rx.select.trigger(placeholder="Ordenar"),
                    rx.select.content(
                        rx.select.item("Relevancia", value="relevancia"),
                        rx.select.item("Precio: menor a mayor", value="price_asc"),
                        rx.select.item("Precio: mayor a menor", value="price_desc"),
                    ),
                    on_change=State.set_sort_order,
                    size="2",
                ),
                justify="between",
                align="center",
                width="100%",
            ),

            # Grid
            rx.cond(
                State.products_list.length() == 0,
                rx.center(rx.spinner(size="3"), padding="6em"),
                rx.cond(
                    State.filtered_products.length() == 0,
                    rx.center(
                        rx.vstack(
                            rx.icon("search", size=40, color="#94A3B8"),
                            rx.text(
                                "No hay productos en esta categoría",
                                color="#64748B",
                                font_size="1rem",
                            ),
                            rx.button(
                                "Ver todos los productos",
                                on_click=State.clear_category_filter,
                                variant="ghost",
                                color="#2563EB",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        padding="4em",
                        width="100%",
                    ),
                    rx.grid(
                        rx.foreach(State.filtered_products, product_card),
                        columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                        gap="4",
                        width="100%",
                    ),
                ),
            ),

            spacing="4",
            width="100%",
        )
    )
