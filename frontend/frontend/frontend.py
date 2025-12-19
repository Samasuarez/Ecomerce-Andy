import reflex as rx

from components.nav import navbar_searchbar
from components.footer import footer

class State(rx.State):
    cart: list[dict] = []

    def add_to_cart(self, product: dict):
        self.cart.append(product)

    @rx.var
    def cart_count(self) -> int:
        return len(self.cart)
def cart_list() -> rx.Component:
    return rx.vstack(
        rx.heading("Carrito", size="5"),
        rx.foreach(
            State.cart,
            lambda product: rx.hstack(
                rx.text(product["name"]),
                rx.text(f"${product['price']:.2f}"),
                justify="between",
                width="100%",
            ),
        ),
        spacing="3",
        width="100%",
    )

       
products = [
    {"id": 1, "name": "Camisa Azul", "price": 29.99, "image": "assets/shirt-blue.png"},
    {"id": 2, "name": "Pantalón Negro", "price": 49.99, "image": "assets/pants-black.png"},
    {"id": 3, "name": "Gorra", "price": 15.00, "image": "assets/cap.png"},
    {"id": 4, "name": "Zapatos Deportivos", "price": 79.99, "image": "assets/shoes-sports.png"},
    {"id": 5, "name": "Vestido Rojo", "price": 39.99, "image": "assets/dress-red.png"},
    {"id": 6, "name": "Jeans Azul", "price": 59.99, "image": "assets/jeans-blue.png"},
    {"id": 7, "name": "Chaqueta Negra", "price": 89.99, "image": "assets/jacket-black.png"},
    {"id": 8, "name": "Sombrero", "price": 19.99, "image": "assets/hat.png"},
    {"id": 9, "name": "Calcetines Blancos", "price": 9.99, "image": "assets/socks-white.png"},
    {"id": 10, "name": "Bolsa", "price": 24.99, "image": "assets/bag.png"},
    {"id": 11, "name": "Reloj", "price": 149.99, "image": "assets/watch.png"},
    {"id": 12, "name": "Gafas de Sol", "price": 49.99, "image": "assets/sunglasses.png"},
    {"id": 13, "name": "Bufanda", "price": 14.99, "image": "assets/scarf.png"},
    {"id": 14, "name": "Guantes", "price": 12.99, "image": "assets/gloves.png"},
    {"id": 15, "name": "Camisa Blanca", "price": 25.99, "image": "assets/shirt-white.png"},
    {"id": 16, "name": "Pantalón Azul", "price": 54.99, "image": "assets/pants-blue.png"},
    {"id": 17, "name": "Gorra Roja", "price": 16.00, "image": "assets/cap-red.png"},
    {"id": 18, "name": "Zapatos Formales", "price": 99.99, "image": "assets/shoes-formal.png"},
    {"id": 19, "name": "Blusa Verde", "price": 34.99, "image": "assets/blouse-green.png"},
    {"id": 20, "name": "Short", "price": 29.99, "image": "assets/shorts.png"},
]


def product_card(product: dict) -> rx.Component:
    return rx.card(
        rx.inset(
            rx.image(
                src=product["image"],
                width="100%",
                height="300px",
                object_fit="cover",
            ),
            side="top",
            pb="current",
        ),
      rx.vstack(
    rx.heading(product["name"], size="4"),
    rx.text(f"${product['price']:.2f}", weight="bold"),
 rx.button(
    "Agregar al carrito",
    color_scheme="gray",
    width="100%",
    on_click=State.add_to_cart(product),


),
 
    spacing="2",
    padding="3",
    
),

   
       width="100%",
    transition="all 0.2s ease",         
    _hover={
        "transform": "translateY(-4px)", 
        "box_shadow": "0 10px 25px rgba(0,0,0,0.15)"},
    )   

rx.card(
    rx.link(
        rx.flex(
            rx.avatar(src="/reflex_banner.png"),
            rx.box(
                rx.heading("Quick Start"),
                rx.text("Get started with Reflex in 5 minutes."),
            ),
            spacing="2",
        ),
    ),
    as_child=True,
)

def index() -> rx.Component:
    return rx.vstack(
        
        navbar_searchbar(),

         rx.text(
            "Productos en carrito: ",
            rx.text(State.cart_count, as_="span", font_weight="bold"),
            font_size="1.2em",
        ),
        rx.box(
            rx.grid(
                *[product_card(product) for product in products],
                columns="repeat(4, 1fr)",
                gap="2rem",
                justify_items="center",
            ),
            max_width="1400px",
            margin="0 auto",
            padding_x="2em",
            padding_y="4em",
            width="100%",
        ),
        cart_list(),

        footer(),
        width="100%",
        spacing="0",
    )

   
    


app = rx.App()
app.add_page(index)
