import reflex as rx
from pages.home import home
from pages.login import login
from pages.profile import profile
from pages.products import products
from pages.cart import cart
app = rx.App(
    theme=rx.theme(
        appearance="light"
    )
)
app.add_page(home, route="/")
app.add_page(login, route="/login")
app.add_page(profile, route="/profile")
app.add_page(products, route="/products")
app.add_page(cart, route="/cart")






