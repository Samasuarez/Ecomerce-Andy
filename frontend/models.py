from typing import TypedDict, List

class Product(TypedDict):
    id: int
    name: str
    price: float
    image: str
    description: str
    sizes: List[str]
    category: str
