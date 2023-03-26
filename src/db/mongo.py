from pymongo import MongoClient
from config import settings


class ResultadosQuiniela:
    def __init__(self):
        self.client = MongoClient(
            f"mongodb+srv://{settings.mongo.credentials.username}:{settings.mongo.credentials.password}@{settings.mongo.credentials.server}/?retryWrites=true&w=majority")
        self.db = self.client["ResultadosQuiniela"]
        self.collection = self.db["resultados"]

    def upsert_por_store_day(self, fecha: str, hora: str, elemento: dict) -> None:
        query = {"fecha": fecha, "hora": hora}
        self.collection.update_one(query, {"$set": elemento}, upsert=True)
