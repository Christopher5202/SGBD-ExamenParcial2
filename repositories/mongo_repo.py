import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
import logging

class MongoRepository:
    """
    Repositorio para persistencia no relacional en MongoDB.
    Usado para bitácora, eventos del sistema y auditoría.
    """
    def __init__(self, uri: str = "mongodb://localhost:27017/"):
        self.uri = uri
        self.client = None
        self.db = None
        self.collection = None
        self._conectar()

    def _conectar(self):
        try:
            # Timeout corto de 2 segundos para no congelar la app si mongo no está instalado
            self.client = pymongo.MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            # Forzar una llamada para verificar conexión
            self.client.admin.command('ping')
            self.db = self.client["biblioteca_db"]
            self.collection = self.db["bitacora_eventos"]
            print("Conexión a MongoDB establecida.")
        except (ConnectionFailure, ServerSelectionTimeoutError):
            # Modo silencioso: Si no hay Mongo, no mostramos error, solo invalidamos el cliente
            self.client = None

    def registrar_evento(self, tipo_evento: str, descripcion: str, usuario: str = "Sistema"):
        """Registra un evento en la colección de MongoDB."""
        documento = {
            "tipo_evento": tipo_evento,
            "descripcion": descripcion,
            "usuario": usuario,
            "fecha": datetime.now().isoformat()
        }
        
        if self.client and self.collection is not None:
            try:
                self.collection.insert_one(documento)
            except Exception as e:
                logging.error(f"Error al insertar en MongoDB: {e}")
        else:
            # Fallback en caso de que Mongo no esté disponible
            print(f"[Log Local] {tipo_evento}: {descripcion}")

    def obtener_eventos(self, limite: int = 100):
        """Recupera los últimos eventos registrados."""
        if self.client and self.collection is not None:
            try:
                cursor = self.collection.find().sort("fecha", -1).limit(limite)
                return list(cursor)
            except Exception as e:
                logging.error(f"Error al consultar MongoDB: {e}")
                return []
        return []
