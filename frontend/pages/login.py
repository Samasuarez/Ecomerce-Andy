import reflex as rx
from ..state import State
from ..components.layout import layout


def login() -> rx.Component:
    return layout(
        rx.center(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("cross", color="#2563EB", size=18),
                        rx.text("NurseShop", font_weight="800", font_size="1.1rem", color="#1E293B"),
                        spacing="2",
                        align="center",
                        justify="center",
                    ),
                    rx.vstack(
                        rx.heading(
                            rx.cond(State.register_mode, "Crear cuenta", "Iniciar sesión"),
                            size="5",
                            color="#1E293B",
                        ),
                        rx.text(
                            rx.cond(
                                State.register_mode,
                                "Completá tus datos para registrarte",
                                "Ingresá con tu cuenta",
                            ),
                            color="#64748B",
                            font_size="0.88rem",
                        ),
                        spacing="1",
                        align="start",
                        width="100%",
                    ),
                    rx.cond(
                        State.login_error != "",
                        rx.box(
                            rx.hstack(
                                rx.icon("alert-circle", size=15, color="#DC2626"),
                                rx.text(State.login_error, color="#DC2626", font_size="0.85rem"),
                                spacing="2",
                                align="center",
                            ),
                            background="#FEF2F2",
                            border="1px solid #FECACA",
                            border_radius="6px",
                            padding="0.75em 1em",
                            width="100%",
                        ),
                    ),
                    rx.vstack(
                        rx.box(
                            rx.text("Email", font_size="0.82rem", font_weight="600", color="#374151", margin_bottom="0.3em"),
                            rx.input(
                                placeholder="tu@email.com",
                                type="email",
                                on_change=State.set_login_email,
                                value=State.login_email,
                                width="100%",
                                border="1.5px solid #E2E8F0",
                                border_radius="8px",
                                background="white",
                                color="#1E293B",
                                _focus={"border_color": "#2563EB", "outline": "none"},
                                _placeholder={"color": "#94A3B8"},
                            ),
                            width="100%",
                        ),
                        rx.box(
                            rx.text("Contraseña", font_size="0.82rem", font_weight="600", color="#374151", margin_bottom="0.3em"),
                            rx.input(
                                placeholder="••••••••",
                                type="password",
                                on_change=State.set_login_password,
                                value=State.login_password,
                                width="100%",
                                border="1.5px solid #E2E8F0",
                                border_radius="8px",
                                background="white",
                                color="#1E293B",
                                _focus={"border_color": "#2563EB", "outline": "none"},
                                _placeholder={"color": "#94A3B8"},
                            ),
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    rx.button(
                        rx.cond(State.register_mode, "Crear cuenta", "Ingresar"),
                        on_click=rx.cond(State.register_mode, State.register, State.login),
                        width="100%",
                        background="#2563EB",
                        color="white",
                        border_radius="8px",
                        font_weight="600",
                        font_size="0.95rem",
                        padding_y="0.6em",
                        cursor="pointer",
                        _hover={"background": "#1D4ED8"},
                    ),
                    rx.divider(border_color="#E2E8F0"),
                    rx.hstack(
                        rx.text(
                            rx.cond(State.register_mode, "¿Ya tenés cuenta?", "¿No tenés cuenta?"),
                            color="#64748B",
                            font_size="0.85rem",
                        ),
                        rx.text(
                            rx.cond(State.register_mode, "Iniciá sesión", "Registrate"),
                            color="#2563EB",
                            font_size="0.85rem",
                            font_weight="600",
                            cursor="pointer",
                            on_click=State.toggle_register_mode,
                            _hover={"text_decoration": "underline"},
                        ),
                        spacing="1",
                        justify="center",
                        width="100%",
                    ),
                    spacing="5",
                    width="100%",
                ),
                background="white",
                border="1px solid #E2E8F0",
                border_radius="14px",
                padding="2.5em",
                width="100%",
                max_width="400px",
                box_shadow="0 4px 24px rgba(0,0,0,0.06)",
            ),
            min_height="70vh",
            padding="3em 1em",
        )
    )
