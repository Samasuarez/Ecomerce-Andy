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


# ── Dashboard ─────────────────────────────────────────────────────────────── #

def stat_card(title: str, value, icon: str, color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(title, color="#1E293B", font_size="0.85rem", font_weight="700"),
                rx.icon(icon, size=18, color=color),
                justify="between",
                width="100%",
            ),
            rx.text(value, font_size="1.8rem", font_weight="700", color="#0F172A"),
            spacing="2",
            width="100%",
        ),
        background="white",
        border="1px solid #CBD5E1",
        border_radius="12px",
        padding="1.25em 1.5em",
        border_top=f"4px solid {color}",
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

def _label(text: str) -> rx.Component:
    return rx.text(text, font_size="0.85rem", font_weight="700", color="#0F172A")


def new_product_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("Nuevo producto", font_weight="800", font_size="1.05rem", color="#0F172A"),
                rx.button(
                    "✕ Cerrar",
                    on_click=State.toggle_product_form,
                    size="1",
                    background="#E2E8F0",
                    color="#1E293B",
                    border_radius="6px",
                    cursor="pointer",
                ),
                justify="between",
                width="100%",
            ),
            rx.grid(
                rx.vstack(
                    _label("Nombre *"),
                    rx.input(
                        value=State.np_name,
                        on_change=State.set_np_name,
                        placeholder="Ej: Ambo Clínico Premium",
                        border="2px solid #94A3B8",
                        border_radius="6px",
                        background="white",
                        color="#0F172A",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    _label("Precio ($) *"),
                    rx.input(
                        value=State.np_price,
                        on_change=State.set_np_price,
                        placeholder="Ej: 29.99",
                        border="2px solid #94A3B8",
                        border_radius="6px",
                        background="white",
                        color="#0F172A",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    _label("Categoría"),
                    rx.select(
                        CAT_LABELS,
                        on_change=State.set_np_category,
                        width="100%",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    _label("Stock"),
                    rx.input(
                        value=State.np_stock,
                        on_change=State.set_np_stock,
                        placeholder="0",
                        border="2px solid #94A3B8",
                        border_radius="6px",
                        background="white",
                        color="#0F172A",
                    ),
                    spacing="1",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                gap="3",
            ),
            rx.vstack(
                _label("Descripción *"),
                rx.text_area(
                    value=State.np_description,
                    on_change=State.set_np_description,
                    placeholder="Descripción del producto",
                    width="100%",
                    border="2px solid #94A3B8",
                    border_radius="6px",
                    color="#0F172A",
                    rows="3",
                ),
                spacing="1",
                width="100%",
            ),
            rx.grid(
                rx.vstack(
                    _label("Talles (separados por coma)"),
                    rx.input(
                        value=State.np_sizes,
                        on_change=State.set_np_sizes,
                        placeholder="S,M,L,XL",
                        border="2px solid #94A3B8",
                        border_radius="6px",
                        background="white",
                        color="#0F172A",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    _label("URL imagen (opcional)"),
                    rx.input(
                        value=State.np_image,
                        on_change=State.set_np_image,
                        placeholder="https://...",
                        border="2px solid #94A3B8",
                        border_radius="6px",
                        background="white",
                        color="#0F172A",
                    ),
                    spacing="1",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                gap="3",
            ),
            rx.cond(
                State.product_form_error != "",
                rx.box(
                    rx.text(State.product_form_error, color="#DC2626", font_size="0.9rem", font_weight="600"),
                    background="#FEF2F2",
                    padding="0.6em 0.85em",
                    border_radius="6px",
                    border="1.5px solid #FCA5A5",
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
                    border_radius="8px",
                    size="3",
                    font_weight="700",
                    cursor="pointer",
                    _hover={"background": "#1D4ED8"},
                ),
                rx.button(
                    "Cancelar",
                    on_click=State.toggle_product_form,
                    background="#F1F5F9",
                    color="#1E293B",
                    border_radius="8px",
                    size="3",
                    font_weight="600",
                    cursor="pointer",
                ),
                spacing="3",
            ),
            spacing="4",
            width="100%",
        ),
        background="#EFF6FF",
        border="2px solid #3B82F6",
        border_radius="12px",
        padding="1.5em",
        width="100%",
    )


def edit_product_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("Editar producto", font_weight="800", font_size="1.05rem", color="#0F172A"),
                rx.button(
                    "✕ Cerrar",
                    on_click=State.admin_cancel_edit_product,
                    size="1",
                    background="#E2E8F0",
                    color="#1E293B",
                    border_radius="6px",
                    cursor="pointer",
                ),
                justify="between",
                width="100%",
            ),
            rx.grid(
                rx.vstack(
                    _label("Nombre"),
                    rx.input(
                        value=State.ep_name,
                        on_change=State.set_ep_name,
                        border="2px solid #94A3B8",
                        border_radius="6px",
                        background="white",
                        color="#0F172A",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    _label("Precio ($)"),
                    rx.input(
                        value=State.ep_price,
                        on_change=State.set_ep_price,
                        border="2px solid #94A3B8",
                        border_radius="6px",
                        background="white",
                        color="#0F172A",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    _label("Stock"),
                    rx.input(
                        value=State.ep_stock,
                        on_change=State.set_ep_stock,
                        border="2px solid #94A3B8",
                        border_radius="6px",
                        background="white",
                        color="#0F172A",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    _label("Categoría"),
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
                _label("Descripción"),
                rx.text_area(
                    value=State.ep_description,
                    on_change=State.set_ep_description,
                    width="100%",
                    border="2px solid #94A3B8",
                    border_radius="6px",
                    color="#0F172A",
                    rows="3",
                ),
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                _label("Talles (separados por coma)"),
                rx.input(
                    value=State.ep_sizes,
                    on_change=State.set_ep_sizes,
                    border="2px solid #94A3B8",
                    border_radius="6px",
                    background="white",
                    color="#0F172A",
                ),
                spacing="1",
                width="100%",
            ),
            rx.cond(
                State.edit_form_error != "",
                rx.box(
                    rx.text(State.edit_form_error, color="#DC2626", font_size="0.9rem", font_weight="600"),
                    background="#FEF2F2",
                    padding="0.6em 0.85em",
                    border_radius="6px",
                    border="1.5px solid #FCA5A5",
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
                    border_radius="8px",
                    size="3",
                    font_weight="700",
                    cursor="pointer",
                    _hover={"background": "#15803D"},
                ),
                rx.button(
                    "Cancelar",
                    on_click=State.admin_cancel_edit_product,
                    background="#F1F5F9",
                    color="#1E293B",
                    border_radius="8px",
                    size="3",
                    font_weight="600",
                    cursor="pointer",
                ),
                spacing="3",
            ),
            spacing="4",
            width="100%",
        ),
        background="#F0FDF4",
        border="2px solid #22C55E",
        border_radius="12px",
        padding="1.5em",
        width="100%",
    )


def admin_product_row(product: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.text(product["id"], font_size="0.8rem", color="#475569", font_weight="500"),
        ),
        rx.table.cell(
            rx.vstack(
                rx.text(product["name"], font_weight="700", font_size="0.9rem", color="#0F172A"),
                rx.text(product["category"], font_size="0.75rem", color="#475569", font_weight="500"),
                spacing="0",
                align="start",
            ),
        ),
        rx.table.cell(
            rx.text("$ ", product["price"], font_weight="700", color="#1D4ED8", font_size="0.9rem"),
        ),
        rx.table.cell(
            rx.badge(
                product["stock"],
                background="#DBEAFE",
                color="#1E40AF",
                radius="full",
                font_weight="700",
                font_size="0.8rem",
                padding_x="0.6em",
            ),
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "✏ Editar",
                    on_click=State.admin_start_edit_product(product["id"]),
                    size="2",
                    background="#2563EB",
                    color="white",
                    border_radius="6px",
                    font_weight="700",
                    cursor="pointer",
                    _hover={"background": "#1D4ED8"},
                ),
                rx.button(
                    "✕ Eliminar",
                    on_click=State.admin_delete_product(product["id"]),
                    size="2",
                    background="#DC2626",
                    color="white",
                    border_radius="6px",
                    font_weight="700",
                    cursor="pointer",
                    _hover={"background": "#B91C1C"},
                ),
                spacing="2",
            ),
        ),
    )


def products_tab() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.heading("Productos", size="5", color="#0F172A", font_weight="800"),
                rx.badge(
                    State.admin_products.length(),
                    background="#DBEAFE",
                    color="#1E40AF",
                    radius="full",
                    font_weight="700",
                ),
                spacing="2",
                align="center",
            ),
            rx.button(
                "+ Agregar producto",
                on_click=State.toggle_product_form,
                size="3",
                background="#2563EB",
                color="white",
                border_radius="8px",
                font_weight="700",
                cursor="pointer",
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
                        rx.table.column_header_cell(rx.text("ID", color="#0F172A", font_weight="700")),
                        rx.table.column_header_cell(rx.text("Producto", color="#0F172A", font_weight="700")),
                        rx.table.column_header_cell(rx.text("Precio", color="#0F172A", font_weight="700")),
                        rx.table.column_header_cell(rx.text("Stock", color="#0F172A", font_weight="700")),
                        rx.table.column_header_cell(rx.text("Acciones", color="#0F172A", font_weight="700")),
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
            border="1.5px solid #CBD5E1",
            border_radius="8px",
        ),
        spacing="4",
        width="100%",
    )


# ── Pedidos ───────────────────────────────────────────────────────────────── #

def order_item_row(item: dict) -> rx.Component:
    return rx.hstack(
        rx.text("·", color="#475569", font_weight="700"),
        rx.text(item["name"], flex="1", font_size="0.88rem", color="#1E293B", font_weight="500"),
        rx.text("x", item["qty"], color="#475569", font_size="0.88rem", font_weight="600"),
        rx.text("$", item["price"], font_weight="700", font_size="0.88rem", color="#1D4ED8"),
        spacing="2",
        align="center",
        width="100%",
    )


def status_badge(status) -> rx.Component:
    return rx.cond(
        status == "pending",
        rx.badge("Pendiente", background="#FEF3C7", color="#92400E", radius="full", font_weight="700"),
        rx.cond(
            status == "confirmed",
            rx.badge("Confirmado", background="#DBEAFE", color="#1E40AF", radius="full", font_weight="700"),
            rx.cond(
                status == "shipped",
                rx.badge("Enviado", background="#EDE9FE", color="#5B21B6", radius="full", font_weight="700"),
                rx.cond(
                    status == "delivered",
                    rx.badge("Entregado", background="#DCFCE7", color="#14532D", radius="full", font_weight="700"),
                    rx.badge("Cancelado", background="#FEE2E2", color="#991B1B", radius="full", font_weight="700"),
                ),
            ),
        ),
    )


def admin_order_card(order: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(order["user_email"], font_weight="700", font_size="0.9rem", color="#0F172A"),
                    rx.text(
                        order["id"],
                        font_size="0.72rem",
                        color="#475569",
                        font_family="monospace",
                        font_weight="500",
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
                    rx.text("$", order["total"], font_weight="800", color="#1D4ED8", font_size="0.95rem"),
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
                    rx.divider(border_color="#CBD5E1"),
                    rx.foreach(State.expanded_order_items, order_item_row),
                    rx.hstack(
                        rx.button(
                            "Confirmar",
                            on_click=State.admin_update_order_status(order["id"], "confirmed"),
                            size="2", background="#2563EB", color="white", border_radius="6px",
                            font_weight="700", cursor="pointer",
                        ),
                        rx.button(
                            "Enviado",
                            on_click=State.admin_update_order_status(order["id"], "shipped"),
                            size="2", background="#7C3AED", color="white", border_radius="6px",
                            font_weight="700", cursor="pointer",
                        ),
                        rx.button(
                            "Entregado",
                            on_click=State.admin_update_order_status(order["id"], "delivered"),
                            size="2", background="#16A34A", color="white", border_radius="6px",
                            font_weight="700", cursor="pointer",
                        ),
                        rx.button(
                            "Cancelar",
                            on_click=State.admin_update_order_status(order["id"], "cancelled"),
                            size="2", background="#DC2626", color="white", border_radius="6px",
                            font_weight="700", cursor="pointer",
                        ),
                        spacing="2",
                        flex_wrap="wrap",
                        padding_top="0.5em",
                    ),
                    spacing="3",
                    width="100%",
                    padding_top="0.75em",
                ),
                rx.box(),
            ),
            spacing="1",
            width="100%",
        ),
        background="white",
        border="1.5px solid #CBD5E1",
        border_radius="10px",
        padding="1em 1.25em",
        width="100%",
        _hover={"border_color": "#2563EB", "box_shadow": "0 2px 8px rgba(37,99,235,0.1)"},
        transition="all 0.15s ease",
    )


def filter_pill(slug: str, label: str) -> rx.Component:
    return rx.text(
        label,
        on_click=State.set_orders_status_filter(slug),
        background=rx.cond(State.orders_status_filter == slug, "#2563EB", "#E2E8F0"),
        color=rx.cond(State.orders_status_filter == slug, "white", "#1E293B"),
        font_size="0.85rem",
        font_weight="700",
        padding_x="1em",
        padding_y="0.4em",
        border_radius="20px",
        cursor="pointer",
        white_space="nowrap",
        border=rx.cond(State.orders_status_filter == slug, "2px solid #1D4ED8", "2px solid #CBD5E1"),
    )


def orders_tab() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.heading("Pedidos", size="5", color="#0F172A", font_weight="800"),
                rx.badge(
                    State.admin_orders.length(),
                    background="#DBEAFE",
                    color="#1E40AF",
                    radius="full",
                    font_weight="700",
                ),
                spacing="2",
                align="center",
            ),
            rx.button(
                "Actualizar",
                on_click=State.load_admin_orders,
                size="2",
                background="#F1F5F9",
                color="#1E293B",
                border_radius="6px",
                font_weight="700",
                cursor="pointer",
                border="1.5px solid #CBD5E1",
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
                rx.text(user["email"], font_weight="700", font_size="0.88rem", color="#0F172A"),
                rx.text(
                    rx.cond(user["full_name"] != "", user["full_name"], "—"),
                    font_size="0.8rem", color="#475569", font_weight="500",
                ),
                spacing="0", align="start",
            ),
        ),
        rx.table.cell(rx.text(user["profession"], font_size="0.85rem", color="#1E293B", font_weight="500")),
        rx.table.cell(rx.text(user["phone"], font_size="0.85rem", color="#1E293B", font_weight="500")),
        rx.table.cell(rx.text(user["dni"], font_size="0.85rem", color="#1E293B", font_weight="500")),
        rx.table.cell(
            rx.cond(
                user["is_admin"],
                rx.badge("Admin", background="#DBEAFE", color="#1E40AF", radius="full", font_weight="700"),
                rx.badge("Cliente", background="#F1F5F9", color="#334155", radius="full", font_weight="600"),
            ),
        ),
    )


def users_tab() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.heading("Usuarios", size="5", color="#0F172A", font_weight="800"),
                rx.badge(
                    State.admin_users.length(),
                    background="#DBEAFE",
                    color="#1E40AF",
                    radius="full",
                    font_weight="700",
                ),
                spacing="2",
                align="center",
            ),
            rx.button(
                "Actualizar",
                on_click=State.load_admin_users,
                size="2",
                background="#F1F5F9",
                color="#1E293B",
                border_radius="6px",
                font_weight="700",
                cursor="pointer",
                border="1.5px solid #CBD5E1",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell(rx.text("Email / Nombre", color="#0F172A", font_weight="700")),
                        rx.table.column_header_cell(rx.text("Profesión", color="#0F172A", font_weight="700")),
                        rx.table.column_header_cell(rx.text("Teléfono", color="#0F172A", font_weight="700")),
                        rx.table.column_header_cell(rx.text("DNI", color="#0F172A", font_weight="700")),
                        rx.table.column_header_cell(rx.text("Rol", color="#0F172A", font_weight="700")),
                    )
                ),
                rx.table.body(rx.foreach(State.admin_users, admin_user_row)),
                width="100%",
                variant="surface",
            ),
            overflow_x="auto",
            width="100%",
            border="1.5px solid #CBD5E1",
            border_radius="8px",
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
                        rx.icon("shield-check", size=24, color="#2563EB"),
                        rx.heading("Panel de Administración", size="6", color="#0F172A", font_weight="800"),
                        spacing="2",
                        align="center",
                    ),
                    rx.text("Admin: ", State.user_email, color="#475569", font_size="0.85rem", font_weight="500"),
                    justify="between",
                    align="center",
                    width="100%",
                    flex_wrap="wrap",
                ),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Dashboard", value="dashboard"),
                        rx.tabs.trigger("Productos", value="products"),
                        rx.tabs.trigger("Pedidos", value="orders"),
                        rx.tabs.trigger("Usuarios", value="users"),
                        mb="4",
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
                    rx.heading("Acceso denegado", size="5", color="#0F172A"),
                    rx.text("Esta sección es solo para administradores.", color="#475569", font_weight="500"),
                    rx.button(
                        "Volver al inicio",
                        on_click=rx.redirect("/"),
                        background="#2563EB",
                        color="white",
                        border_radius="8px",
                        font_weight="700",
                        cursor="pointer",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="4em 1em",
                width="100%",
            ),
        )
    )
