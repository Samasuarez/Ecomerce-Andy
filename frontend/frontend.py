import reflex as rx

from .pages.home import home
from .pages.login import login
from .pages.profile import profile
from .pages.products import products
from .pages.product_detail import product_detail  # noqa: F401 — @rx.page auto-registers the route
from .pages.cart import cart
from .pages.admin import admin
from .state import State


app = rx.App()

app.add_page(home, route="/", on_load=State.load_products)
app.add_page(login, route="/login")
app.add_page(profile, route="/profile", on_load=State.load_my_orders)
app.add_page(products, route="/products", on_load=State.load_products)
app.add_page(cart, route="/cart")
app.add_page(
    admin,
    route="/admin",
    on_load=[
        State.check_admin,
        State.load_admin_stats,
        State.load_admin_users,
        State.load_admin_orders,
        State.load_admin_products,
    ],
)
