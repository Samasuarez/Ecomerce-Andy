"""
Reemplaza los productos genéricos por el catálogo de enfermería
y crea el usuario admin si no existe.

Ejecutar desde la raíz: python backend/seed_nursing.py
"""
import asyncio
import bcrypt
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "ecommerce")

NURSING_PRODUCTS = [
    # ── AMBOS ──────────────────────────────────────────────────────────────
    {"id": 1,  "name": "Ambo Unisex Clásico",        "price": 45.99, "category": "ambos",          "sizes": ["XS","S","M","L","XL","XXL"], "stock": 50, "image": "assets/products/ambo-unisex.jpg",     "description": "Ambo unisex de algodón/poliéster antifluidos, corte recto, ideal para uso clínico diario."},
    {"id": 2,  "name": "Ambo Mujer Estampado",        "price": 52.99, "category": "ambos",          "sizes": ["XS","S","M","L","XL"],       "stock": 30, "image": "assets/products/ambo-mujer.jpg",      "description": "Ambo de mujer con estampado floral, tela suave antiestática y bolsillos laterales."},
    {"id": 3,  "name": "Ambo Quirúrgico Verde",       "price": 49.99, "category": "ambos",          "sizes": ["S","M","L","XL","XXL"],      "stock": 40, "image": "assets/products/ambo-verde.jpg",      "description": "Ambo quirúrgico color verde limón, antifluidos y con tratamiento antibacteriano."},
    {"id": 4,  "name": "Ambo Premium Antifluidos",    "price": 74.99, "category": "ambos",          "sizes": ["S","M","L","XL"],            "stock": 20, "image": "assets/products/ambo-premium.jpg",    "description": "Ambo premium con máxima protección antifluidos, bolsillos reforzados y costuras selladas."},
    {"id": 5,  "name": "Ambo Pediátrico Estampado",   "price": 47.99, "category": "ambos",          "sizes": ["XS","S","M","L"],            "stock": 25, "image": "assets/products/ambo-pediatrico.jpg", "description": "Ambo con estampado infantil para el área de pediatría, tela suave y lavable a 90°."},
    {"id": 6,  "name": "Ambo Azul Clásico",           "price": 45.99, "category": "ambos",          "sizes": ["S","M","L","XL","XXL"],      "stock": 45, "image": "assets/products/ambo-azul.jpg",       "description": "Ambo azul clásico, corte recto, algodón premium con bolsillo en pecho."},
    # ── CALZADO CLÍNICO ────────────────────────────────────────────────────
    {"id": 7,  "name": "Zueco Clínico Blanco",        "price": 59.99, "category": "calzado_clinico","sizes": ["36","37","38","39","40","41","42","43"], "stock": 35, "image": "assets/products/zueco-blanco.jpg",  "description": "Zueco clínico antideslizante color blanco, suela de goma y plantilla acolchada."},
    {"id": 8,  "name": "Zueco Antideslizante Negro",  "price": 59.99, "category": "calzado_clinico","sizes": ["36","37","38","39","40","41","42","43"], "stock": 30, "image": "assets/products/zueco-negro.jpg",   "description": "Zueco clínico negro con puntera reforzada, suela antideslizante certificada."},
    {"id": 9,  "name": "Sneaker Clínico Unisex",      "price": 89.99, "category": "calzado_clinico","sizes": ["36","37","38","39","40","41","42","43","44"], "stock": 20, "image": "assets/products/sneaker-clinico.jpg","description": "Zapatilla clínica con amortiguación superior, suela antibacteriana y fácil limpieza."},
    {"id": 10, "name": "Bota Clínica Impermeable",    "price": 74.99, "category": "calzado_clinico","sizes": ["36","37","38","39","40","41","42"], "stock": 15, "image": "assets/products/bota-clinica.jpg",  "description": "Bota clínica impermeable con caña media, ideal para guardias largas y cirugías."},
    # ── ACCESORIOS ─────────────────────────────────────────────────────────
    {"id": 11, "name": "Estetoscopio Doble Campana",  "price": 129.99,"category": "accesorios",     "sizes": ["Único"],                    "stock": 20, "image": "assets/products/estetoscopio.jpg",    "description": "Estetoscopio de doble campana para adultos y pediátrico, membrana de alta sensibilidad."},
    {"id": 12, "name": "Tijeras Bandage Inox",        "price": 18.99, "category": "accesorios",     "sizes": ["Único"],                    "stock": 60, "image": "assets/products/tijeras.jpg",         "description": "Tijeras bandage de acero inoxidable, punta roma con serrado interno para corte seguro."},
    {"id": 13, "name": "Reloj Enfermería Segundero",  "price": 34.99, "category": "accesorios",     "sizes": ["Único"],                    "stock": 30, "image": "assets/products/reloj.jpg",           "description": "Reloj de colgar para uniforme con segundero visible, ideal para toma de pulso."},
    {"id": 14, "name": "Set Lapicero Médico x3",      "price": 12.99, "category": "accesorios",     "sizes": ["Único"],                    "stock": 80, "image": "assets/products/lapicero.jpg",        "description": "Set de 3 lapiceros de bolsillo con clip reforzado para uso médico."},
    {"id": 15, "name": "Porta Credencial Retráctil",  "price": 8.99,  "category": "accesorios",     "sizes": ["Único"],                    "stock":100, "image": "assets/products/porta-credencial.jpg","description": "Porta credencial con cuerda retráctil y clip giratorio de 360°."},
    # ── EQUIPAMIENTO ───────────────────────────────────────────────────────
    {"id": 16, "name": "Tensiómetro Digital Muñeca",  "price": 99.99, "category": "equipamiento",   "sizes": ["Único"],                    "stock": 15, "image": "assets/products/tensiometro.jpg",     "description": "Tensiómetro digital de muñeca con detección de arritmias y memoria para 60 lecturas."},
    {"id": 17, "name": "Oxímetro de Pulso",           "price": 49.99, "category": "equipamiento",   "sizes": ["Único"],                    "stock": 25, "image": "assets/products/oximetro.jpg",        "description": "Oxímetro de dedo con pantalla LED grande, lectura rápida de SpO2 y pulso."},
    {"id": 18, "name": "Termómetro Infrarrojo",       "price": 74.99, "category": "equipamiento",   "sizes": ["Único"],                    "stock": 20, "image": "assets/products/termometro.jpg",      "description": "Termómetro infrarrojo sin contacto, resultado en 1 segundo, fiebre con alarma sonora."},
    {"id": 19, "name": "Glucómetro Kit Completo",     "price": 149.99,"category": "equipamiento",   "sizes": ["Único"],                    "stock": 10, "image": "assets/products/glucometro.jpg",      "description": "Glucómetro con 50 lancetas y 50 tiras reactivas incluidas, memoria para 500 mediciones."},
    # ── DESCARTABLES ───────────────────────────────────────────────────────
    {"id": 20, "name": "Guantes Nitrilo x50",         "price": 24.99, "category": "descartables",   "sizes": ["S","M","L","XL"],           "stock": 50, "image": "assets/products/guantes.jpg",         "description": "Guantes de nitrilo sin polvo, sin látex, caja de 50 unidades. Alta resistencia."},
    {"id": 21, "name": "Barbijo Quirúrgico x50",      "price": 14.99, "category": "descartables",   "sizes": ["Único"],                    "stock": 60, "image": "assets/products/barbijo.jpg",         "description": "Barbijos quirúrgicos 3 capas con filtro BFE ≥98%, caja de 50 unidades."},
    {"id": 22, "name": "Cofia Descartable x100",      "price": 11.99, "category": "descartables",   "sizes": ["Único"],                    "stock": 70, "image": "assets/products/cofia.jpg",           "description": "Cofias descartables de polipropileno no tejido, bolsa de 100 unidades."},
    {"id": 23, "name": "Cubre Calzados x50 Pares",    "price": 13.99, "category": "descartables",   "sizes": ["Único"],                    "stock": 50, "image": "assets/products/cubre-calzados.jpg",  "description": "Cubre calzados descartables antideslizantes, bolsa de 50 pares."},
    # ── ROPA CLÍNICA ───────────────────────────────────────────────────────
    {"id": 24, "name": "Delantal Impermeable",        "price": 39.99, "category": "ropa_clinica",   "sizes": ["Único"],                    "stock": 25, "image": "assets/products/delantal.jpg",        "description": "Delantal clínico impermeable con cierre trasero, reutilizable y lavable a 60°."},
    {"id": 25, "name": "Camisola Descartable x10",    "price": 17.99, "category": "ropa_clinica",   "sizes": ["Único"],                    "stock": 40, "image": "assets/products/camisola.jpg",        "description": "Camisolas descartables para pacientes, no tejido suave, bolsa de 10 unidades."},
]

ADMIN_EMAIL = "admin@nurseshop.com"
ADMIN_PASSWORD = "admin123"


async def seed():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]

    # Reemplazar productos
    await db.products.drop()
    await db.products.insert_many(NURSING_PRODUCTS)
    print(f"[OK] {len(NURSING_PRODUCTS)} productos de enfermeria insertados.")

    # Crear índice único por id
    await db.products.create_index("id", unique=True)

    # Admin user
    existing = await db.users.find_one({"email": ADMIN_EMAIL})
    if existing:
        await db.users.update_one({"email": ADMIN_EMAIL}, {"$set": {"is_admin": True}})
        print(f"[OK] Usuario admin '{ADMIN_EMAIL}' ya existe - marcado como admin.")
    else:
        hashed = bcrypt.hashpw(ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()
        await db.users.insert_one({
            "email": ADMIN_EMAIL,
            "hashed_password": hashed,
            "first_name": "Admin",
            "last_name": "NurseShop",
            "phone": "",
            "address": "",
            "is_admin": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        print(f"[OK] Usuario admin creado: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
