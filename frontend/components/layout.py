import reflex as rx
from components.nav import navbar_searchbar
from components.footer import footer

def layout(content: rx.Component) -> rx.Component:
    return rx.vstack(
        navbar_searchbar(),
        rx.box(
            content,
            width="100%",
            max_width="900px",
            margin="0 auto",
            padding="3em",
        ),
        footer(),
        min_height="100vh",
        width="100%",
    )




