import reflex as rx
from data import PRODUCTS

class State(rx.State):
    cart: list[dict] = []

    # --- UI STATE (drawer mobile) ---
    cart_drawer_open: bool = False

    def toggle_cart_drawer(self, open: bool):
        self.cart_drawer_open = open

    def add_to_cart(self, product_id: int):
        product = next(p for p in PRODUCTS if p["id"] == product_id)

        for item in self.cart:
            if item["id"] == product_id:
                item["qty"] += 1
                item["total"] = item["price"] * item["qty"]
                return

        self.cart.append(
            {
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "qty": 1,
                "total": product["price"],
            }
        )

    def increase_qty(self, product_id: int):
        for item in self.cart:
            if item["id"] == product_id:
                item["qty"] += 1
                item["total"] = item["price"] * item["qty"]
                return

    def decrease_qty(self, product_id: int):
        for item in self.cart:
            if item["id"] == product_id:
                if item["qty"] > 1:
                    item["qty"] -= 1
                    item["total"] = item["price"] * item["qty"]
                else:
                    self.cart.remove(item)
                return

    @rx.var
    def cart_count(self) -> int:
        return sum(item["qty"] for item in self.cart)

    @rx.var
    def cart_total(self) -> float:
        return sum(item["total"] for item in self.cart)





