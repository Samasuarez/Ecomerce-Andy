import reflex as rx
from ..state import State
from ..components.layout import layout

CATS = [
    ("ambos", "Ambos"),
    ("calzado_clinico", "Calzado Clínico"),
    ("accesorios", "Accesorios"),
    ("equipamiento", "Equipamiento"),
    ("descartables", "Descartables"),
    ("ropa_clinica", "Ropa Clínica"),
]

STATUS_FILTERS = [
    ("all", "Todos"),
    ("pending", "Pendiente"),
    ("confirmed", "Confirmado"),
    ("shipped", "Enviado"),
    ("delivered", "Entregado"),
    ("cancelled", "Cancelado"),
]

CAT_LABELS = [label for _, label in CATS]
CAT_VALUES = [slug for slug, _ in CATS]


# ── Dashboard ─────────────────────────────────────────────────────────────── #

def stat_card(title: str, value, icon: str, color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(title, color="#64748B", font_size="0.82rem", font_weight="600"),
                rx.icon(icon, size=18, color=color),
                justify="between",
                width="100%",
            ),
            rx.text(value, font_size="1.8rem", font_weight="700", color="#1E293B"),
            spacing="2",
            width="100%",
        ),
        background="white",
        border="1px solid #E2E8F0",
        border_radius="12px",
        padding="1.25em 1.5em",
        border_top=f"3px solid {color}",
    )


def dashboard_tab() -> rx.Component:
    return rx.vstack(
        rx.grid(
            stat_card("Usuarios", State.stat_total_users, "users", "#2563EB"),
            stat_card("Pedidos", State.stat_total_orders, "shopping-cart", "#7C3AED"),
            stat_card("Ingresos", State.stat_revenue_fmt, "dollar-sign", "#16A34A"),
            stat_card("Pendientes", State.stat_pending_orders, "clock", "#D97706"),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            gap="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


# ── Productos ─────────────────────────────────────────────────────────────── #

def new_product_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("Nuevo producto", font_weight="700", font_size="1rem", color="#1E293B"),
                rx.button(
                    "✕ Cerrar",
                    on_click=State.toggle_product_form,
                    size="1",
                    variant="ghost",
                    color="#64748B",
                ),
                justify="between",
                width="100%",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Nombre *", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.input(
                        value=State.np_name,
                        on_change=State.set_np_name,
                        placeholder="Ej: Ambo Clínico Premium",
                        border="1.5px solid #CBD5E1",
                        border_radius="6px",
                        background="white",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Precio ($) *", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.input(
                        value=State.np_price,
                        on_change=State.set_np_price,
                        placeholder="Ej: 29.99",
                        border="1.5px solid #CBD5E1",
                        border_radius="6px",
                        background="white",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Categoría", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.select(
                        CAT_LABELS,
                        on_change=State.set_np_category,
                        width="100%",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Stock", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.input(
                        value=State.np_stock,
                        on_change=State.set_np_stock,
                        placeholder="0",
                        border="1.5px solid #CBD5E1",
                        border_radius="6px",
                        background="white",
                    ),
                    spacing="1",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                gap="3",
            ),
            rx.vstack(
                rx.text("Descripción *", font_size="0.8rem", font_weight="600", color="#374151"),
                rx.text_area(
                    value=State.np_description,
                    on_change=State.set_np_description,
                    placeholder="Descripción del producto",
                    width="100%",
                    border="1.5px solid #CBD5E1",
                    border_radius="6px",
                    rows="3",
                ),
                spacing="1",
                width="100%",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Talles (separados por coma)", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.input(
                        value=State.np_sizes,
                        on_change=State.set_np_sizes,
                        placeholder="S,M,L,XL",
                        border="1.5px solid #CBD5E1",
                        border_radius="6px",
                        background="white",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("URL imagen (opcional)", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.input(
                        value=State.np_image,
                        on_change=State.set_np_image,
                        placeholder="https://...",
                        border="1.5px solid #CBD5E1",
                        border_radius="6px",
                        background="white",
                    ),
                    spacing="1",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                gap="3",
            ),
            rx.cond(
                State.product_form_error != "",
                rx.box(
                    rx.text(State.product_form_error, color="#DC2626", font_size="0.85rem"),
                    background="#FEF2F2",
                    padding="0.5em 0.75em",
                    border_radius="6px",
                    border="1px solid #FECACA",
                    width="100%",
                ),
                rx.box(),
            ),
            rx.hstack(
                rx.button(
                    "Crear producto",
                    on_click=State.admin_create_product,
                    background="#2563EB",
                    color="white",
                    border_radius="6px",
                    size="3",
                    font_weight="600",
                ),
                rx.button(
                    "Cancelar",
                    on_click=State.toggle_product_form,
                    variant="ghost",
                    border_radius="6px",
                ),
                spacing="3",
            ),
            spacing="4",
            width="100%",
        ),
        background="#EFF6FF",
        border="2px solid #93C5FD",
        border_radius="12px",
        padding="1.5em",
        width="100%",
    )


def edit_product_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("✏️ Editar producto", font_weight="700", font_size="1rem", color="#1E293B"),
                rx.button(
                    "✕ Cerrar",
                    on_click=State.admin_cancel_edit_product,
                    size="1",
                    variant="ghost",
                    color="#64748B",
                ),
                justify="between",
                width="100%",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Nombre", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.input(
                        value=State.ep_name,
                        on_change=State.set_ep_name,
                        border="1.5px solid #CBD5E1",
                        border_radius="6px",
                        background="white",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Precio ($)", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.input(
                        value=State.ep_price,
                        on_change=State.set_ep_price,
                        border="1.5px solid #CBD5E1",
                        border_radius="6px",
                        background="white",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Stock", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.input(
                        value=State.ep_stock,
                        on_change=State.set_ep_stock,
                        border="1.5px solid #CBD5E1",
                        border_radius="6px",
                        background="white",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Categoría", font_size="0.8rem", font_weight="600", color="#374151"),
                    rx.select(
                        CAT_LABELS,
                        on_change=State.set_ep_category,
                        width="100%",
                    ),
                    spacing="1",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                gap="3",
            ),
            rx.vstack(
                rx.text("Descripción", font_size="0.8rem", font_weight="600", color="#374151"),
                rx.text_area(
                    value=State.ep_description,
                    on_change=State.set_ep_description,
                    width="100%",
                    border="1.5px solid #CBD5E1",
                    border_radius="6px",
                    rows="3",
                ),
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                rx.text("Talles (separados por coma)", font_size="0.8rem", font_weight="600", color="#374151"),
                rx.input(
                    value=State.ep_sizes,
                    on_change=State.set_ep_sizes,
                    border="1.5px solid #CBD5E1",
                    border_radius="6px",
                    background="white",
                ),
                spacing="1",
                width="100%",
            ),
            rx.cond(
                State.edit_form_error != "",
                rx.box(
                    rx.text(State.edit_form_error, color="#DC2626", font_size="0.85rem"),
                    background="#FEF2F2",
                    padding="0.5em 0.75em",
                    border_radius="6px",
                    width="100%",
                ),
                rx.box(),
            ),
            rx.hstack(
                rx.button(
                    "Guardar cambios",
                    on_click=State.admin_save_edit_product,
                    background="#16A34A",
                    color="white",
                    border_radius="6px",
                    size="3",
                    font_weight="600",
                ),
                rx.button(
                    "Cancelar",
                    on_click=State.admin_cancel_edit_product,
                    variant="ghost",
                    border_radius="6px",
                ),
                spacing="3",
            ),
            spacing="4",
            width="100%",
        ),
        background="#F0FDF4",
        border="2px solid #86EFAC",
        border_radius="12px",
        padding="1.5em",
        width="100%",
    )


def admin_product_row(product: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.text(product["id"], font_size="0.78rem", color="#94A3B8"),
        ),
        rx.table.cell(
            rx.vstack(
                rx.text(product["name"], font_weight="600", font_size="0.88rem"),
                rx.text(product["category"], font_size="0.72rem", color="#94A3B8"),
                spacing="0",
                align="start",
            ),
        ),
        rx.table.cell(
            rx.text("$", product["price"], font_weight="700", color="#2563EB"),
        ),
        rx.table.cell(
            rx.badge(product["stock"], color_scheme="blue", radius="full"),
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "Editar",
                    on_click=State.admin_start_edit_product(product["id"]),
                    size="1",
                    color_scheme="blue",
                    variant="soft",
                ),
                rx.button(
                    "Eliminar",
                    on_click=State.admin_delete_product(product["id"]),
                    size="1",
                    color_scheme="red",
                    variant="soft",
                ),
                spacing="2",
            ),
        ),
    )


def products_tab() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.heading("Productos", size="5", color="#1E293B"),
                rx.badge(State.admin_products.length(), color_scheme="blue", radius="full"),
                spacing="2",
                align="center",
            ),
            rx.button(
                "+ Agregar producto",
                on_click=State.toggle_product_form,
                size="2",
                background="#2563EB",
                color="white",
                border_radius="8px",
                font_weight="600",
                _hover={"background": "#1D4ED8"},
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.cond(
            State.show_product_form,
            new_product_form(),
            rx.box(),
        ),
        rx.cond(
            State.edit_product_id > 0,
            edit_product_form(),
            rx.box(),
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Producto"),
                        rx.table.column_header_cell("Precio"),
                        rx.table.column_header_cell("Stock"),
                        rx.table.column_header_cell("Acciones"),
                    )
                ),
                rx.table.body(
                    rx.foreach(State.admin_products, admin_product_row),
                ),
                width="100%",
                variant="surface",
            ),
            overflow_x="auto",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


# ── Pedidos ───────────────────────────────────────────────────────────────── #

def order_item_row(item: dict) -> rx.Component:
    return rx.hstack(
        rx.text("·", color="#94A3B8"),
        rx.text(item["name"], flex="1", font_size="0.85rem", color="#374151"),
        rx.text("x", item["qty"], color="#64748B", font_size="0.85rem"),
        rx.text("$", item["price"], font_weight="600", font_size="0.85rem", color="#2563EB"),
        spacing="2",
        align="center",
        width="100%",
    )


def status_badge(status) -> rx.Component:
    return rx.cond(
        status == "pending",
        rx.badge("Pendiente", color_scheme="orange", radius="full", font_size="0.72rem"),
        rx.cond(
            status == "confirmed",
            rx.badge("Confirmado", color_scheme="blue", radius="full", font_size="0.72rem"),
            rx.cond(
                status == "shipped",
                rx.badge("Enviado", color_scheme="purple", radius="full", font_size="0.72rem"),
                rx.cond(
                    status == "delivered",
                    rx.badge("Entregado", color_scheme="green", radius="full", font_size="0.72rem"),
                    rx.badge("Cancelado", color_scheme="red", radius="full", font_size="0.72rem"),
                ),
            ),
        ),
    )


def admin_order_card(order: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(order["user_email"], font_weight="600", font_size="0.88rem"),
                    rx.text(
                        order["id"],
                        font_size="0.7rem",
                        color="#94A3B8",
                        font_family="monospace",
                        max_width="200px",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.hstack(
                    status_badge(order["status"]),
                    rx.text("$", order["total"], font_weight="700", color="#2563EB"),
                    spacing="2",
                    align="center",
                ),
                justify="between",
                align="center",
                width="100%",
                cursor="pointer",
                on_click=State.toggle_expanded_order(order["id"]),
            ),
            rx.cond(
                State.expanded_order_id == order["id"],
                rx.vstack(
                    rx.divider(border_color="#E2E8F0"),
                    rx.foreach(State.expanded_order_items, order_item_row),
                    rx.hstack(
                        rx.button("Confirmar", on_click=State.admin_update_order_status(order["id"], "confirmed"), size="1", color_scheme="blue", variant="soft"),
                        rx.button("Enviado", on_click=State.admin_update_order_status(order["id"], "shipped"), size="1", color_scheme="purple", variant="soft"),
                        rx.button("Entregado", on_click=State.admin_update_order_status(order["id"], "delivered"), size="1", color_scheme="green", variant="soft"),
                        rx.button("Cancelar", on_click=State.admin_update_order_status(order["id"], "cancelled"), size="1", color_scheme="red", variant="soft"),
                        spacing="2",
                        flex_wrap="wrap",
                        padding_top="0.5em",
                    ),
                    spacing="2",
                    width="100%",
                    padding_top="0.5em",
                ),
                rx.box(),
            ),
            spacing="1",
            width="100%",
        ),
        background="white",
        border="1px solid #E2E8F0",
        border_radius="8px",
        padding="0.85em 1em",
        width="100%",
        _hover={"border_color": "#CBD5E1"},
        transition="border-color 0.15s ease",
    )


def filter_pill(slug: str, label: str) -> rx.Component:
    return rx.text(
        label,
        on_click=State.set_orders_status_filter(slug),
        background=rx.cond(State.orders_status_filter == slug, "#2563EB", "#F1F5F9"),
        color=rx.cond(State.orders_status_filter == slug, "white", "#475569"),
        font_size="0.8rem",
        font_weight="500",
        padding_x="0.85em",
        padding_y="0.35em",
        border_radius="20px",
        cursor="pointer",
        white_space="nowrap",
    )


def orders_tab() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.heading("Pedidos", size="5", color="#1E293B"),
                rx.badge(State.admin_orders.length(), color_scheme="blue", radius="full"),
                spacing="2",
                align="center",
            ),
            rx.button(
                rx.icon("refresh-cw", size=14),
                on_click=State.load_admin_orders,
                size="1",
                variant="ghost",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.hstack(
            *[filter_pill(slug, label) for slug, label in STATUS_FILTERS],
            spacing="2",
            flex_wrap="wrap",
        ),
        rx.vstack(
            rx.foreach(State.filtered_admin_orders, admin_order_card),
            spacing="2",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


# ── Usuarios ──────────────────────────────────────────────────────────────── #

def admin_user_row(user: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.vstack(
                rx.text(user["email"], font_weight="500", font_size="0.85rem"),
                rx.text(
                    rx.cond(user["full_name"] != "", user["full_name"], "—"),
                    font_size="0.78rem", color="#64748B",
                ),
                spacing="0", align="start",
            ),
        ),
        rx.table.cell(rx.text(user["profession"], font_size="0.82rem", color="#374151")),
        rx.table.cell(rx.text(user["phone"], font_size="0.82rem", color="#64748B")),
        rx.table.cell(rx.text(user["dni"], font_size="0.82rem", color="#64748B")),
        rx.table.cell(
            rx.cond(
                user["is_admin"],
                rx.badge("Admin", color_scheme="blue", radius="full"),
                rx.badge("Cliente", color_scheme="gray", radius="full"),
            ),
        ),
    )


def users_tab() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.heading("Usuarios", size="5", color="#1E293B"),
                rx.badge(State.admin_users.length(), color_scheme="blue", radius="full"),
                spacing="2",
                align="center",
            ),
            rx.button(rx.icon("refresh-cw", size=14), on_click=State.load_admin_users, size="1", variant="ghost"),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Email / Nombre"),
                        rx.table.column_header_cell("Profesión"),
                        rx.table.column_header_cell("Teléfono"),
                        rx.table.column_header_cell("DNI"),
                        rx.table.column_header_cell("Rol"),
                    )
                ),
                rx.table.body(rx.foreach(State.admin_users, admin_user_row)),
                width="100%",
                variant="surface",
            ),
            overflow_x="auto",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


# ── Página ────────────────────────────────────────────────────────────────── #

def admin() -> rx.Component:
    return layout(
        rx.cond(
            State.is_admin,
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon("shield-check", size=22, color="#2563EB"),
                        rx.heading("Panel de Administración", size="6", color="#1E293B"),
                        spacing="2",
                        align="center",
                    ),
                    rx.text("Bienvenido, ", State.user_email, color="#64748B", font_size="0.85rem"),
                    justify="between",
                    align="center",
                    width="100%",
                    flex_wrap="wrap",
                ),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("bar-chart", size=15), rx.text("Dashboard"), spacing="2", align="center"),
                            value="dashboard",
                        ),
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("package", size=15), rx.text("Productos"), spacing="2", align="center"),
                            value="products",
                        ),
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("shopping-cart", size=15), rx.text("Pedidos"), spacing="2", align="center"),
                            value="orders",
                        ),
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("users", size=15), rx.text("Usuarios"), spacing="2", align="center"),
                            value="users",
                        ),
                        mb="4",
                        flex_wrap="wrap",
                    ),
                    rx.tabs.content(dashboard_tab(), value="dashboard"),
                    rx.tabs.content(products_tab(), value="products"),
                    rx.tabs.content(orders_tab(), value="orders"),
                    rx.tabs.content(users_tab(), value="users"),
                    default_value="dashboard",
                    width="100%",
                ),
                spacing="5",
                width="100%",
            ),
            rx.center(
                rx.vstack(
                    rx.icon("shield", size=44, color="#94A3B8"),
                    rx.heading("Acceso denegado", size="5"),
                    rx.text("Esta sección es solo para administradores.", color="#64748B"),
                    rx.button(
                        "Volver al inicio",
                        on_click=rx.redirect("/"),
                        background="#2563EB",
                        color="white",
                        border_radius="8px",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="4em 1em",
                width="100%",
            ),
        )
    )
