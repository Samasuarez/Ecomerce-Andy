import reflex as rx



class State(rx.State):
    """The app state."""



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
                object_fit="cover"
            ),
            side="top",
            pb="current",
        ),
        rx.vstack(
            rx.heading(product["name"], size="4"),
            rx.text(f"${product['price']:.2f}", weight="bold"),
            spacing="2",  # Esto separa el texto dentro de la card
            padding="3",
        ),
        width="360px",
    )

def product_grid() -> rx.Component:
    return rx.vstack(
        # Aquí van las cards, usando la función product_card
        *[product_card(product) for product in products],  # Asumiendo que tienes una lista de productos
        spacing="4",  # Espacio entre las cards
        padding="10px",  # Padding global para que las cards no queden pegadas a los bordes
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
    return rx.center(rx.grid(
        *[product_card(product) for product in products],

        columns="3",
        spacing="4",

    ))
        
   
    


app = rx.App()
app.add_page(index)
