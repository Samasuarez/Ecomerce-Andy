import reflex as rx
from ..state import State
from ..components.layout import layout


@rx.page(route="/product/[product_id]", on_load=State.load_product)
def product_detail() -> rx.Component:
    return layout(
        rx.cond(
            State.pd_id > 0,
            rx.box(
                rx.hstack(
                    # Imagen placeholder
                    rx.center(
                        rx.vstack(
                            rx.icon("package", color="#94A3B8", size=56),
                            rx.text(State.pd_category, color="#94A3B8", font_size="0.8rem"),
                            spacing="2",
                            align="center",
                        ),
                        background="linear-gradient(135deg,#F1F5F9,#E2E8F0)",
                        border_radius="12px",
                        width=["100%", "100%", "400px"],
                        height=["240px", "300px", "380px"],
                        flex_shrink="0",
                    ),

                    # Info
                    rx.vstack(
                        # Breadcrumb
                        rx.hstack(
                            rx.link("Inicio", href="/", color="#64748B", font_size="0.82rem"),
                            rx.text("/", color="#94A3B8", font_size="0.82rem"),
                            rx.link("Productos", href="/products", color="#64748B", font_size="0.82rem"),
                            rx.text("/", color="#94A3B8", font_size="0.82rem"),
                            rx.text(State.pd_category, color="#64748B", font_size="0.82rem"),
                            spacing="1",
                            align="center",
                        ),

                        rx.heading(State.pd_name, size="6", color="#1E293B"),

                        rx.hstack(
                            rx.icon("truck", size=15, color="#16A34A"),
                            rx.text("Envío gratis a todo el país", color="#16A34A", font_size="0.85rem", font_weight="600"),
                            spacing="2",
                            align="center",
                        ),

                        # Precio
                        rx.text(
                            State.pd_price_fmt,
                            font_size="2rem",
                            font_weight="800",
                            color="#1E293B",
                        ),

                        rx.divider(border_color="#E2E8F0"),

                        rx.text(State.pd_description, color="#475569", line_height="1.6"),

                        # Talles
                        rx.cond(
                            State.pd_sizes.length() > 0,
                            rx.vstack(
                                rx.text("Talle", font_weight="700", font_size="0.9rem", color="#1E293B"),
                                rx.hstack(
                                    rx.foreach(
                                        State.pd_sizes,
                                        lambda s: rx.box(
                                            rx.text(s, font_size="0.85rem", font_weight="600"),
                                            padding="0.4em 0.9em",
                                            border=rx.cond(
                                                State.selected_size == s,
                                                "2px solid #2563EB",
                                                "1.5px solid #E2E8F0",
                                            ),
                                            border_radius="6px",
                                            cursor="pointer",
                                            background=rx.cond(
                                                State.selected_size == s,
                                                "#EFF6FF",
                                                "white",
                                            ),
                                            color=rx.cond(
                                                State.selected_size == s,
                                                "#2563EB",
                                                "#1E293B",
                                            ),
                                            on_click=State.set_selected_size(s),
                                            _hover={"border_color": "#2563EB"},
                                        ),
                                    ),
                                    spacing="2",
                                    flex_wrap="wrap",
                                ),
                                spacing="2",
                                align="start",
                            ),
                        ),

                        # Botón agregar
                        rx.button(
                            rx.hstack(
                                rx.icon("shopping-cart", size=18),
                                rx.text("Agregar al carrito"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=State.add_to_cart(State.pd_id),
                            width="100%",
                            size="3",
                            background="#2563EB",
                            color="white",
                            border_radius="8px",
                            font_weight="600",
                            _hover={"background": "#1D4ED8"},
                        ),

                        rx.button(
                            "Ver carrito",
                            on_click=rx.redirect("/cart"),
                            width="100%",
                            size="3",
                            variant="outline",
                            border="1.5px solid #E2E8F0",
                            color="#475569",
                            border_radius="8px",
                            background="transparent",
                            _hover={"background": "#F1F5F9"},
                        ),

                        spacing="4",
                        align="start",
                        flex="1",
                    ),

                    spacing="6",
                    align="start",
                    flex_wrap=["wrap", "wrap", "nowrap"],
                    width="100%",
                ),
                max_width="1000px",
                margin="0 auto",
                padding_y="2em",
                width="100%",
            ),
            rx.center(
                rx.vstack(
                    rx.spinner(size="3"),
                    rx.text("Cargando producto...", color="#64748B"),
                    spacing="3",
                    align="center",
                ),
                padding="6em",
                width="100%",
            ),
        )
    )
