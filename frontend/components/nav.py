import reflex as rx
from ..state import State
from .cart_drawner import cart_drawer

NAV_BG = "#1E3A8A"
NAV_SUB = "#1e2d5a"

CATEGORIES = [
    ("ambos", "Ambos"),
    ("calzado_clinico", "Calzado Clínico"),
    ("accesorios", "Accesorios"),
    ("equipamiento", "Equipamiento"),
    ("descartables", "Descartables"),
    ("ropa_clinica", "Ropa Clínica"),
]


def _cat_link(slug: str, label: str) -> rx.Component:
    return rx.text(
        label,
        on_click=State.go_to_category(slug),
        color=rx.cond(State.selected_category == slug, "#93C5FD", "#CBD5E1"),
        font_weight=rx.cond(State.selected_category == slug, "700", "400"),
        font_size="0.85rem",
        cursor="pointer",
        padding_x="0.75em",
        padding_y="0.4em",
        border_radius="4px",
        _hover={"color": "#FFFFFF", "background": "rgba(255,255,255,0.1)"},
        white_space="nowrap",
    )


def navbar_searchbar() -> rx.Component:
    return rx.box(
        # ── Fila superior ──────────────────────────────────────────────── #
        rx.hstack(
            # Logo
            rx.hstack(
                rx.icon("cross", color="#93C5FD", size=20),
                rx.text(
                    "NurseShop",
                    color="white",
                    font_weight="800",
                    font_size="1.25rem",
                    letter_spacing="-0.5px",
                ),
                on_click=rx.redirect("/"),
                cursor="pointer",
                spacing="2",
                align="center",
            ),

            # Barra de búsqueda (desktop)
            rx.hstack(
                rx.input(
                    placeholder="Buscar productos de enfermería...",
                    value=State.search_query,
                    on_change=State.set_search_query,
                    on_key_up=rx.cond(
                        State.search_query != "",
                        rx.redirect("/products"),
                        rx.redirect("/products"),
                    ),
                    border="none",
                    outline="none",
                    background="white",
                    flex="1",
                    padding="0.5em 1em",
                    font_size="0.9rem",
                    border_radius="6px 0 0 6px",
                    _focus={"outline": "none"},
                ),
                rx.button(
                    rx.icon("search", size=16),
                    on_click=rx.redirect("/products"),
                    background="#2563EB",
                    color="white",
                    border="none",
                    padding="0.5em 1em",
                    border_radius="0 6px 6px 0",
                    cursor="pointer",
                    _hover={"background": "#1D4ED8"},
                ),
                flex="1",
                max_width="600px",
                display=["none", "none", "flex"],
            ),

            # Iconos derecha
            rx.hstack(
                # Usuario
                rx.cond(
                    State.is_logged_in,
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.hstack(
                                rx.icon("user", color="white", size=18),
                                rx.text(
                                    State.user_email,
                                    color="#CBD5E1",
                                    font_size="0.8rem",
                                    max_width="120px",
                                    overflow="hidden",
                                    text_overflow="ellipsis",
                                    white_space="nowrap",
                                    display=["none", "none", "block"],
                                ),
                                spacing="1",
                                cursor="pointer",
                                align="center",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item("Mi perfil", on_click=rx.redirect("/profile")),
                            rx.menu.item("Mis pedidos", on_click=rx.redirect("/profile")),
                            rx.cond(
                                State.is_admin,
                                rx.menu.item(
                                    "Panel Admin",
                                    on_click=rx.redirect("/admin"),
                                    color="#2563EB",
                                ),
                            ),
                            rx.menu.separator(),
                            rx.menu.item("Cerrar sesión", on_click=State.logout, color="red"),
                        ),
                    ),
                    rx.link(
                        rx.hstack(
                            rx.icon("user", color="white", size=18),
                            rx.text("Ingresar", color="white", font_size="0.85rem",
                                    display=["none", "none", "block"]),
                            spacing="1", align="center",
                        ),
                        href="/login",
                    ),
                ),

                # Carrito (desktop → link, mobile → drawer)
                rx.link(
                    rx.hstack(
                        rx.icon("shopping-cart", color="white", size=20),
                        rx.cond(
                            State.cart_count > 0,
                            rx.badge(
                                State.cart_count,
                                color_scheme="red",
                                radius="full",
                                font_size="0.7rem",
                            ),
                        ),
                        spacing="1",
                        align="center",
                    ),
                    href="/cart",
                    display=["none", "flex"],
                ),

                rx.box(cart_drawer(), display=["flex", "none"]),

                spacing="4",
                align="center",
            ),

            width="100%",
            align="center",
            justify="between",
            padding_x="1.5em",
            padding_y="0.75em",
        ),

        # ── Barra de categorías ────────────────────────────────────────── #
        rx.box(
            rx.hstack(
                rx.text(
                    "Todos",
                    on_click=State.clear_category_filter,
                    color=rx.cond(State.selected_category == "", "#93C5FD", "#CBD5E1"),
                    font_weight=rx.cond(State.selected_category == "", "700", "400"),
                    font_size="0.85rem",
                    cursor="pointer",
                    padding_x="0.75em",
                    padding_y="0.4em",
                    border_radius="4px",
                    _hover={"color": "#FFFFFF", "background": "rgba(255,255,255,0.1)"},
                ),
                *[_cat_link(slug, label) for slug, label in CATEGORIES],
                spacing="1",
                overflow_x="auto",
                padding_x="1.5em",
                padding_y="0.35em",
            ),
            background=NAV_SUB,
            width="100%",
            display=["none", "none", "block"],
        ),

        background=NAV_BG,
        width="100%",
        position="sticky",
        top="0",
        z_index="100",
        box_shadow="0 2px 8px rgba(0,0,0,0.25)",
    )
