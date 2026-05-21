import reflex as rx
from ..state import State
from ..components.layout import layout


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
            stat_card("Usuarios totales", State.stat_total_users, "users", "#2563EB"),
            stat_card("Pedidos totales", State.stat_total_orders, "shopping-cart", "#7C3AED"),
            stat_card("Ingresos totales", State.stat_revenue_fmt, "dollar-sign", "#16A34A"),
            stat_card("Pedidos pendientes", State.stat_pending_orders, "clock", "#D97706"),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            gap="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


def new_product_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Nuevo producto", font_weight="700", font_size="1rem", color="#1E293B"),
            rx.grid(
                rx.input(
                    placeholder="Nombre del producto",
                    value=State.np_name,
                    on_change=State.set_np_name,
                    border_radius="6px",
                ),
                rx.input(
                    placeholder="Precio (ej: 29.99)",
                    value=State.np_price,
                    on_change=State.set_np_price,
                    border_radius="6px",
                ),
                rx.select.root(
                    rx.select.trigger(placeholder="Categoría"),
                    rx.select.content(
                        rx.select.item("Ambos", value="ambos"),
                        rx.select.item("Calzado Clínico", value="calzado_clinico"),
                        rx.select.item("Accesorios", value="accesorios"),
                        rx.select.item("Equipamiento", value="equipamiento"),
                        rx.select.item("Descartables", value="descartables"),
                        rx.select.item("Ropa Clínica", value="ropa_clinica"),
                    ),
                    value=State.np_category,
                    on_change=State.set_np_category,
                ),
                rx.input(
                    placeholder="Stock",
                    value=State.np_stock,
                    on_change=State.set_np_stock,
                    border_radius="6px",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                gap="3",
            ),
            rx.text_area(
                placeholder="Descripción del producto",
                value=State.np_description,
                on_change=State.set_np_description,
                width="100%",
                border_radius="6px",
                rows="3",
            ),
            rx.input(
                placeholder="Talles separados por coma (ej: S,M,L,XL)",
                value=State.np_sizes,
                on_change=State.set_np_sizes,
                border_radius="6px",
            ),
            rx.cond(
                State.product_form_error != "",
                rx.hstack(
                    rx.icon("alert-circle", size=15, color="#DC2626"),
                    rx.text(State.product_form_error, color="#DC2626", font_size="0.85rem"),
                    spacing="1",
                ),
            ),
            rx.hstack(
                rx.button(
                    "Crear producto",
                    on_click=State.admin_create_product,
                    background="#2563EB",
                    color="white",
                    border_radius="6px",
                ),
                rx.button(
                    "Cancelar",
                    on_click=State.toggle_product_form,
                    variant="ghost",
                    border_radius="6px",
                ),
                spacing="2",
            ),
            spacing="3",
            width="100%",
        ),
        background="#F8FAFC",
        border="1px solid #E2E8F0",
        border_radius="8px",
        padding="1.5em",
        width="100%",
    )


def admin_product_row(product: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(product["id"], font_size="0.85rem"),
        rx.table.cell(product["name"], font_weight="500"),
        rx.table.cell(product["category"], font_size="0.85rem"),
        rx.table.cell(rx.text("$", product["price"], font_weight="600", color="#2563EB")),
        rx.table.cell(product["stock"]),
        rx.table.cell(
            rx.button(
                rx.icon("trash-2", size=14),
                on_click=State.admin_delete_product(product["id"]),
                size="1",
                variant="ghost",
                color_scheme="red",
            )
        ),
    )


def products_tab() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Productos", size="5", color="#1E293B"),
            rx.button(
                rx.hstack(rx.icon("plus", size=15), rx.text("Agregar"), spacing="1", align="center"),
                on_click=State.toggle_product_form,
                size="2",
                background="#2563EB",
                color="white",
                border_radius="6px",
                _hover={"background": "#1D4ED8"},
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.cond(State.show_product_form, new_product_form()),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Nombre"),
                        rx.table.column_header_cell("Categoría"),
                        rx.table.column_header_cell("Precio"),
                        rx.table.column_header_cell("Stock"),
                        rx.table.column_header_cell(""),
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


def admin_user_row(user: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(user["email"]),
        rx.table.cell(rx.text(user["first_name"], " ", user["last_name"])),
        rx.table.cell(user["created_at"], font_size="0.82rem"),
        rx.table.cell(
            rx.cond(
                user["is_admin"],
                rx.badge("Admin", color_scheme="blue"),
                rx.badge("Usuario", color_scheme="gray"),
            )
        ),
    )


def users_tab() -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("Registro"),
                    rx.table.column_header_cell("Rol"),
                )
            ),
            rx.table.body(
                rx.foreach(State.admin_users, admin_user_row),
            ),
            width="100%",
            variant="surface",
        ),
        overflow_x="auto",
        width="100%",
    )


def admin_order_row(order: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.text(order["id"], max_width="80px", overflow="hidden", text_overflow="ellipsis", white_space="nowrap", font_size="0.75rem", color="#94A3B8"),
        ),
        rx.table.cell(order["user_email"], font_size="0.85rem"),
        rx.table.cell(rx.text("$", order["total"], font_weight="600")),
        rx.table.cell(rx.badge(order["status"], color_scheme="blue", radius="full", font_size="0.72rem")),
        rx.table.cell(order["created_at"], font_size="0.82rem"),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "Confirmar",
                    on_click=State.admin_update_order_status(order["id"], "confirmed"),
                    size="1",
                    color_scheme="blue",
                ),
                rx.button(
                    "Enviado",
                    on_click=State.admin_update_order_status(order["id"], "shipped"),
                    size="1",
                    color_scheme="green",
                ),
                rx.button(
                    "Cancelar",
                    on_click=State.admin_update_order_status(order["id"], "cancelled"),
                    size="1",
                    color_scheme="red",
                ),
                spacing="1",
            )
        ),
    )


def orders_tab() -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("ID"),
                    rx.table.column_header_cell("Usuario"),
                    rx.table.column_header_cell("Total"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Fecha"),
                    rx.table.column_header_cell("Acciones"),
                )
            ),
            rx.table.body(
                rx.foreach(State.admin_orders, admin_order_row),
            ),
            width="100%",
            variant="surface",
        ),
        overflow_x="auto",
        width="100%",
    )


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
                            rx.hstack(rx.icon("users", size=15), rx.text("Usuarios"), spacing="2", align="center"),
                            value="users",
                        ),
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("shopping-cart", size=15), rx.text("Pedidos"), spacing="2", align="center"),
                            value="orders",
                        ),
                        mb="4",
                        flex_wrap="wrap",
                    ),
                    rx.tabs.content(dashboard_tab(), value="dashboard"),
                    rx.tabs.content(products_tab(), value="products"),
                    rx.tabs.content(users_tab(), value="users"),
                    rx.tabs.content(orders_tab(), value="orders"),
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
