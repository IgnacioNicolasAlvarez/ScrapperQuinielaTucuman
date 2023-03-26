from pydantic import BaseModel
from typing import List
from datetime import date


class Premio(BaseModel):
    posicion: int
    numero: int


class Sorteo(BaseModel):
    nombre: str
    fecha: str
    hora: str
    premios: List[Premio]
    store_date: str = date.today().strftime("%d-%m-%Y")
