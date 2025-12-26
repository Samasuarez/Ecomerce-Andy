import reflex as rx
from state import State
from components.layout import layout


def cart_link_with_badge() -> rx.Component:
    return rx.hstack(
        rx.text("Carrito"),
        rx.cond(
            State.cart_count > 0,
            rx.badge(
                State.cart_count,
                color_scheme="red",
                radius="full",
            ),
        ),
        spacing="1",
        align="center",
    )

def cart_item(item: dict) -> rx.Component:
    return rx.card(                     
        rx.hstack(
            rx.text(
                item["name"],
                width="40%",
                font_weight="medium",
            ),
            rx.text(
                f"${item['price']:.2f}",
                color="gray",
            ),
            rx.hstack(
                rx.icon_button(          
                    rx.icon(tag="minus"),
                    on_click=lambda: State.decrease_qty(item["id"]),
                    size="2",
                    variant="soft",
                ),
                rx.text(
                    item["qty"],
                    min_width="24px",
                    text_align="center",
                    font_weight="bold",
                ),
                rx.icon_button(
                    rx.icon(tag="plus"),
                    on_click=lambda: State.increase_qty(item["id"]),
                    size="2",
                    variant="soft",
                ),
                spacing="2",
            ),
            rx.text(
                f"${item['total']:.2f}",
                font_weight="bold",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
      
        padding="1em",
        width="100%",
        transition="background-color 0.2s ease",
        _hover={"backgroundColor": "#fafafa"},
    )




from components.layout import layout

def cart() -> rx.Component:
    return layout(
        rx.box(
            rx.cond(
                State.is_logged_in,

                rx.center(
                    rx.container(
                        rx.vstack(
                            rx.heading("🛒 Carrito", size="6"),
                            rx.foreach(State.cart, cart_item),
                            rx.divider(),
                            rx.hstack(
                                rx.text("Total", size="4"),
                                rx.text(
                                    f"${State.cart_total:.2f}",
                                    size="4",
                                    font_weight="bold",
                                ),
                                justify="between",
                                width="100%",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        max_width="800px",
                        padding="2em",
                    ),
                    width="100%",
                ),

                rx.box(),
            ),

            on_mount=rx.cond(
                ~State.is_logged_in,
                rx.redirect("/login"),
                None,
            ),
        )
    )









