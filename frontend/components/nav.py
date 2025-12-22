import reflex as rx
from state import State

def navbar_searchbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(src="/logo.jpg", width="2.25em", border_radius="25%"),
                    rx.heading("Shop Andy", size="7", weight="bold"),
                    align_items="center",
                ),

                rx.hstack(
                    rx.input(
                        rx.input.slot(rx.icon("search")),
                        placeholder="Search...",
                        type="search",
                        size="2",
                    ),
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("shopping-cart"),
                                rx.text(State.cart_count),
                                spacing="1",
                            ),
                            variant="soft",
                            color_scheme="gray",
                        ),
                        href="/cart",
                    ),
                    spacing="3",
                ),

                justify="between",
                width="100%",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
    )
