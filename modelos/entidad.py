"""
Módulo de entidades abstractas base.
"""
from abc import ABC, abstractmethod
import uuid
from datetime import datetime

class Entidad(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    Asigna un identificador único (UUID) y una fecha de creación.
    """
    def __init__(self) -> None:
        """
        Inicializa una nueva entidad con un ID único y la fecha actual.
        """
        # Según los requerimientos se asigna en la inicialización
        self._id = str(uuid.uuid4())
        self._fecha_creacion = datetime.now().isoformat()
    
    @property
    def id(self) -> str:
        """Obtiene el ID de la entidad."""
        return self._id
        
    @property
    def fecha_creacion(self) -> str:
        """Obtiene la fecha de creación en formato ISO."""
        return self._fecha_creacion

    @abstractmethod
    def __str__(self) -> str:
        """
        Representación en string del objeto.
        Debe ser implementado por subclases.
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Exporta el estado interno a un diccionario serializable en JSON.
        Debe ser implementado por subclases.
        
        Returns:
            dict: Estado del objeto.
        """
        pass
