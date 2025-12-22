import reflex as rx
from state import State


def cart_item(item: dict) -> rx.Component:
    return rx.hstack(
        rx.text(item["name"], width="40%"),
        rx.text(f"${item['price']:.2f}"),
        rx.hstack(
            rx.button("-", on_click=lambda: State.decrease_qty(item["id"]), size="1"),
            rx.text(item["qty"]),
            rx.button("+", on_click=lambda: State.increase_qty(item["id"]), size="1"),
            spacing="2",
        ),
        rx.text(f"${item['total']:.2f}"),
        justify="between",
        width="100%",
    )



def cart() -> rx.Component:
    return rx.vstack(
        rx.heading("🛒 Carrito"),
        rx.foreach(State.cart, cart_item),
        rx.divider(),
        rx.text(
            "Total: ",
            rx.text(State.cart_total, as_="span", font_weight="bold"),
        ),
        max_width="800px",
        margin="0 auto",
        padding="2em",
        spacing="4",
    )








