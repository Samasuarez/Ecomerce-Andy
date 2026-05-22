import reflex as rx
import httpx
import os

API_URL = os.environ.get("API_URL", "https://nurseshop-api.onrender.com")

CATEGORIES = {
    "ambos": "Ambos",
    "calzado_clinico": "Calzado Clínico",
    "accesorios": "Accesorios",
    "equipamiento": "Equipamiento",
    "descartables": "Descartables",
    "ropa_clinica": "Ropa Clínica",
}


class State(rx.State):

    # ── Productos ─────────────────────────────────────────────────────── #
    products_list: list[dict] = []
    selected_category: str = ""
    search_query: str = ""
    sort_order: str = ""

    # ── Producto detalle (vars tipados para rx.foreach) ────────────────── #
    pd_id: int = 0
    pd_name: str = ""
    pd_price: float = 0.0
    pd_image: str = ""
    pd_description: str = ""
    pd_sizes: list[str] = []
    pd_category: str = ""
    selected_size: str = ""

    # ── Carrito ───────────────────────────────────────────────────────── #
    cart: list[dict] = []
    cart_drawer_open: bool = False

    # ── Auth ──────────────────────────────────────────────────────────── #
    token: str = ""
    user_id: str = ""
    is_logged_in: bool = False
    is_admin: bool = False
    user_email: str = ""
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""
    register_mode: bool = False

    # ── Campos extra para registro ────────────────────────────────────── #
    reg_full_name: str = ""
    reg_phone: str = ""
    reg_dni: str = ""
    reg_profession: str = ""
    reg_province: str = ""
    reg_city: str = ""
    reg_address: str = ""

    # ── Perfil ────────────────────────────────────────────────────────── #
    first_name: str = ""
    last_name: str = ""
    full_name: str = ""
    address: str = ""
    phone: str = ""
    dni: str = ""
    profession: str = ""
    province: str = ""
    city: str = ""
    editing_field: str | None = None

    # ── Pedidos del usuario ───────────────────────────────────────────── #
    my_orders: list[dict] = []
    order_placing: bool = False
    order_success: bool = False
    order_error: str = ""
    last_order_id: str = ""

    # ── MercadoPago ───────────────────────────────────────────────────── #
    mp_checkout_loading: bool = False
    mp_checkout_error: str = ""

    # ── Admin stats ───────────────────────────────────────────────────── #
    stat_total_users: int = 0
    stat_total_orders: int = 0
    stat_total_revenue: float = 0.0
    stat_pending_orders: int = 0
    admin_users: list[dict] = []
    admin_orders: list[dict] = []
    admin_products: list[dict] = []

    # ── Admin form nuevo producto ─────────────────────────────────────── #
    show_product_form: bool = False
    np_name: str = ""
    np_price: str = ""
    np_description: str = ""
    np_category: str = "ambos"
    np_sizes: str = "S,M,L,XL"
    np_image: str = ""
    np_stock: str = "0"
    product_form_error: str = ""

    # ================================================================== #
    #  Computed vars                                                      #
    # ================================================================== #

    @rx.var
    def filtered_products(self) -> list[dict]:
        products = self.products_list
        if self.selected_category:
            products = [p for p in products if p.get("category") == self.selected_category]
        if self.search_query:
            q = self.search_query.lower()
            products = [p for p in products if q in p.get("name", "").lower()]
        if self.sort_order == "price_asc":
            products = sorted(products, key=lambda p: p.get("price", 0))
        elif self.sort_order == "price_desc":
            products = sorted(products, key=lambda p: p.get("price", 0), reverse=True)
        return products

    @rx.var
    def featured_products(self) -> list[dict]:
        return self.products_list[:8]

    @rx.var
    def pd_price_fmt(self) -> str:
        return f"${self.pd_price:.2f}"

    @rx.var
    def profile_completed(self) -> bool:
        return bool(self.full_name or (self.first_name and self.last_name))

    @rx.var
    def cart_count(self) -> int:
        return sum(item["qty"] for item in self.cart)

    @rx.var
    def cart_total(self) -> float:
        return round(sum(item["total"] for item in self.cart), 2)

    @rx.var
    def cart_total_fmt(self) -> str:
        return f"${self.cart_total:.2f}"

    @rx.var
    def stat_revenue_fmt(self) -> str:
        return f"${self.stat_total_revenue:.2f}"

    # ================================================================== #
    #  Productos                                                          #
    # ================================================================== #

    async def load_products(self):
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{API_URL}/products")
                if resp.status_code == 200:
                    self.products_list = resp.json()
            except Exception:
                pass

    async def load_product(self):
        product_id = self.router.page.params.get("product_id", "1")
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{API_URL}/products/{product_id}")
                if resp.status_code == 200:
                    p = resp.json()
                    self.pd_id = p["id"]
                    self.pd_name = p["name"]
                    self.pd_price = p["price"]
                    self.pd_image = p["image"]
                    self.pd_description = p["description"]
                    self.pd_sizes = p["sizes"]
                    self.pd_category = p["category"]
                    self.selected_size = ""
                else:
                    self.pd_id = 0
            except Exception:
                self.pd_id = 0

    def go_to_product(self, product_id: int):
        return rx.redirect(f"/product/{product_id}")

    def go_to_category(self, category: str):
        self.selected_category = category
        return rx.redirect("/products")

    def set_category_filter(self, category: str):
        self.selected_category = category

    def clear_category_filter(self):
        self.selected_category = ""

    def set_search_query(self, query: str):
        self.search_query = query

    def set_sort_order(self, order: str):
        self.sort_order = order

    def set_selected_size(self, size: str):
        self.selected_size = size

    # ================================================================== #
    #  Carrito                                                            #
    # ================================================================== #

    def toggle_cart_drawer(self, open: bool):
        self.cart_drawer_open = open

    def add_to_cart(self, product_id: int):
        product = next((p for p in self.products_list if p["id"] == product_id), None)
        if not product:
            return
        updated = self.cart.copy()
        for item in updated:
            if item["id"] == product_id:
                item["qty"] += 1
                item["total"] = round(item["price"] * item["qty"], 2)
                self.cart = updated
                return
        updated.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "qty": 1,
            "total": product["price"],
        })
        self.cart = updated

    def increase_qty(self, product_id: int):
        updated = self.cart.copy()
        for item in updated:
            if item["id"] == product_id:
                item["qty"] += 1
                item["total"] = round(item["price"] * item["qty"], 2)
        self.cart = updated

    def decrease_qty(self, product_id: int):
        updated = []
        for item in self.cart:
            if item["id"] == product_id:
                if item["qty"] > 1:
                    item["qty"] -= 1
                    item["total"] = round(item["price"] * item["qty"], 2)
                    updated.append(item)
            else:
                updated.append(item)
        self.cart = updated

    def remove_from_cart(self, product_id: int):
        self.cart = [item for item in self.cart if item["id"] != product_id]

    # ================================================================== #
    #  Auth                                                               #
    # ================================================================== #

    def set_login_email(self, value: str):
        self.login_email = value
        self.login_error = ""

    def set_login_password(self, value: str):
        self.login_password = value
        self.login_error = ""

    def toggle_register_mode(self):
        self.register_mode = not self.register_mode
        self.login_error = ""

    def set_reg_full_name(self, v: str): self.reg_full_name = v
    def set_reg_phone(self, v: str): self.reg_phone = v
    def set_reg_dni(self, v: str): self.reg_dni = v
    def set_reg_profession(self, v: str): self.reg_profession = v
    def set_reg_province(self, v: str): self.reg_province = v
    def set_reg_city(self, v: str): self.reg_city = v
    def set_reg_address(self, v: str): self.reg_address = v

    def _apply_user(self, data: dict):
        self.token = data["access_token"]
        user = data["user"]
        self.user_id = user["id"]
        self.user_email = user["email"]
        self.full_name = user.get("full_name", "")
        self.first_name = user.get("first_name", "")
        self.last_name = user.get("last_name", "")
        self.phone = user.get("phone", "")
        self.address = user.get("address", "")
        self.dni = user.get("dni", "")
        self.profession = user.get("profession", "")
        self.province = user.get("province", "")
        self.city = user.get("city", "")
        self.is_admin = user.get("is_admin", False)
        self.is_logged_in = True
        self.login_email = ""
        self.login_password = ""

    async def login(self):
        if not self.login_email or not self.login_password:
            self.login_error = "Completá email y contraseña."
            return
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{API_URL}/auth/login",
                    json={"email": self.login_email, "password": self.login_password},
                )
                if resp.status_code == 200:
                    self._apply_user(resp.json())
                    return rx.redirect("/")
                self.login_error = resp.json().get("detail", "Credenciales incorrectas.")
            except Exception:
                self.login_error = "No se pudo conectar con el servidor."

    async def register(self):
        if not self.login_email or not self.login_password:
            self.login_error = "Completá email y contraseña."
            return
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{API_URL}/auth/register",
                    json={
                        "email": self.login_email,
                        "password": self.login_password,
                        "full_name": self.reg_full_name,
                        "phone": self.reg_phone,
                        "dni": self.reg_dni,
                        "profession": self.reg_profession,
                        "province": self.reg_province,
                        "city": self.reg_city,
                        "address": self.reg_address,
                    },
                )
                if resp.status_code == 200:
                    self._apply_user(resp.json())
                    self.reg_full_name = ""
                    self.reg_phone = ""
                    self.reg_dni = ""
                    self.reg_profession = ""
                    self.reg_province = ""
                    self.reg_city = ""
                    self.reg_address = ""
                    return rx.redirect("/profile")
                self.login_error = resp.json().get("detail", "Error al registrarse.")
            except Exception:
                self.login_error = "No se pudo conectar con el servidor."

    def logout(self):
        self.token = ""
        self.user_id = ""
        self.is_logged_in = False
        self.is_admin = False
        self.user_email = ""
        self.full_name = ""
        self.first_name = ""
        self.last_name = ""
        self.phone = ""
        self.address = ""
        self.dni = ""
        self.profession = ""
        self.province = ""
        self.city = ""
        self.cart = []
        self.my_orders = []

    # ================================================================== #
    #  Perfil                                                             #
    # ================================================================== #

    def set_full_name(self, v: str): self.full_name = v
    def set_first_name(self, v: str): self.first_name = v
    def set_last_name(self, v: str): self.last_name = v
    def set_phone(self, v: str): self.phone = v
    def set_address(self, v: str): self.address = v
    def set_dni(self, v: str): self.dni = v
    def set_profession(self, v: str): self.profession = v
    def set_province(self, v: str): self.province = v
    def set_city(self, v: str): self.city = v

    def start_edit(self, field: str):
        self.editing_field = field

    async def stop_edit(self):
        self.editing_field = None
        await self._persist_profile()

    async def save_profile(self):
        await self._persist_profile()

    async def _persist_profile(self):
        if not self.token:
            return
        async with httpx.AsyncClient() as client:
            try:
                await client.put(
                    f"{API_URL}/users/me",
                    json={
                        "full_name": self.full_name,
                        "first_name": self.first_name,
                        "last_name": self.last_name,
                        "phone": self.phone,
                        "address": self.address,
                        "dni": self.dni,
                        "profession": self.profession,
                        "province": self.province,
                        "city": self.city,
                    },
                    headers={"Authorization": f"Bearer {self.token}"},
                )
            except Exception:
                pass

    # ================================================================== #
    #  Pedidos del usuario                                                #
    # ================================================================== #

    async def place_order(self):
        if not self.is_logged_in:
            return rx.redirect("/login")
        if not self.cart:
            return
        self.order_placing = True
        self.order_error = ""
        async with httpx.AsyncClient() as client:
            try:
                items = [
                    {"product_id": i["id"], "name": i["name"],
                     "price": i["price"], "qty": i["qty"]}
                    for i in self.cart
                ]
                resp = await client.post(
                    f"{API_URL}/orders",
                    json={"items": items},
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    self.last_order_id = data["id"]
                    self.order_success = True
                    self.cart = []
                else:
                    self.order_error = "No se pudo procesar el pedido."
            except Exception:
                self.order_error = "Error de conexión."
        self.order_placing = False

    def reset_order_success(self):
        self.order_success = False
        self.last_order_id = ""

    async def load_my_orders(self):
        if not self.token:
            return
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{API_URL}/orders/mine",
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if resp.status_code == 200:
                    self.my_orders = resp.json()
            except Exception:
                pass

    # ================================================================== #
    #  MercadoPago                                                        #
    # ================================================================== #

    async def go_to_mp_checkout(self):
        if not self.is_logged_in:
            return rx.redirect("/login")
        if not self.cart:
            return
        self.mp_checkout_loading = True
        self.mp_checkout_error = ""
        async with httpx.AsyncClient() as client:
            try:
                items = [
                    {"product_id": i["id"], "name": i["name"],
                     "price": i["price"], "qty": i["qty"]}
                    for i in self.cart
                ]
                order_resp = await client.post(
                    f"{API_URL}/orders",
                    json={"items": items},
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if order_resp.status_code != 200:
                    self.mp_checkout_error = "Error al crear el pedido."
                    self.mp_checkout_loading = False
                    return
                order_id = order_resp.json()["id"]

                pref_resp = await client.post(
                    f"{API_URL}/payments/create-preference",
                    json={"order_id": order_id},
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if pref_resp.status_code == 200:
                    init_point = pref_resp.json()["init_point"]
                    self.cart = []
                    self.mp_checkout_loading = False
                    return rx.redirect(init_point)
                else:
                    self.mp_checkout_error = "Error al iniciar el pago. Intentá de nuevo."
            except Exception:
                self.mp_checkout_error = "Error de conexión."
        self.mp_checkout_loading = False

    # ================================================================== #
    #  Admin                                                              #
    # ================================================================== #

    async def check_admin(self):
        if not self.is_admin:
            return rx.redirect("/")

    async def load_admin_stats(self):
        if not self.token:
            return
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{API_URL}/admin/stats",
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if resp.status_code == 200:
                    d = resp.json()
                    self.stat_total_users = d["total_users"]
                    self.stat_total_orders = d["total_orders"]
                    self.stat_total_revenue = d["total_revenue"]
                    self.stat_pending_orders = d["pending_orders"]
            except Exception:
                pass

    async def load_admin_users(self):
        if not self.token:
            return
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{API_URL}/admin/users",
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if resp.status_code == 200:
                    self.admin_users = resp.json()
            except Exception:
                pass

    async def load_admin_orders(self):
        if not self.token:
            return
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{API_URL}/admin/orders",
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if resp.status_code == 200:
                    self.admin_orders = resp.json()
            except Exception:
                pass

    async def load_admin_products(self):
        if not self.token:
            return
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{API_URL}/admin/products",
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if resp.status_code == 200:
                    self.admin_products = resp.json()
            except Exception:
                pass

    def toggle_product_form(self):
        self.show_product_form = not self.show_product_form
        self.product_form_error = ""

    def set_np_name(self, v: str): self.np_name = v
    def set_np_price(self, v: str): self.np_price = v
    def set_np_description(self, v: str): self.np_description = v
    def set_np_category(self, v: str): self.np_category = v
    def set_np_sizes(self, v: str): self.np_sizes = v
    def set_np_image(self, v: str): self.np_image = v
    def set_np_stock(self, v: str): self.np_stock = v

    async def admin_create_product(self):
        self.product_form_error = ""
        try:
            price = float(self.np_price)
            stock = int(self.np_stock) if self.np_stock else 0
        except ValueError:
            self.product_form_error = "Precio o stock inválido."
            return
        if not self.np_name or not self.np_description:
            self.product_form_error = "Nombre y descripción son requeridos."
            return

        sizes = [s.strip() for s in self.np_sizes.split(",") if s.strip()]
        if not sizes:
            sizes = ["Único"]

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{API_URL}/admin/products",
                    json={"name": self.np_name, "price": price,
                          "description": self.np_description, "category": self.np_category,
                          "sizes": sizes, "image": self.np_image, "stock": stock},
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                if resp.status_code == 200:
                    self.np_name = ""
                    self.np_price = ""
                    self.np_description = ""
                    self.np_sizes = "S,M,L,XL"
                    self.np_image = ""
                    self.np_stock = "0"
                    self.show_product_form = False
                    await self.load_admin_products()
                    await self.load_products()
                else:
                    self.product_form_error = resp.json().get("detail", "Error al crear producto.")
            except Exception:
                self.product_form_error = "Error de conexión."

    async def admin_delete_product(self, product_id: int):
        async with httpx.AsyncClient() as client:
            try:
                await client.delete(
                    f"{API_URL}/admin/products/{product_id}",
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                await self.load_admin_products()
                await self.load_products()
            except Exception:
                pass

    async def admin_update_order_status(self, order_id: str, status: str):
        async with httpx.AsyncClient() as client:
            try:
                await client.patch(
                    f"{API_URL}/admin/orders/{order_id}/status?status={status}",
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                await self.load_admin_orders()
            except Exception:
                pass
