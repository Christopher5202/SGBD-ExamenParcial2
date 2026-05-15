"""
Módulo de libros del sistema.
Define la jerarquía de libros.
"""
from datetime import datetime
from typing import ClassVar, Dict, Any, TypeVar, Type
from modelos.entidad import Entidad
from utils.validadores import validar_isbn13

T = TypeVar('T', bound='Libro')

class Libro(Entidad):
    """
    Clase base para todos los libros del catálogo.
    """
    def __init__(self, titulo: str, autor: str, isbn: str, anio: int, genero: str, disponible: bool = True) -> None:
        super().__init__()
        self._titulo = titulo
        self._autor = autor
        self.isbn = isbn  # Usar el setter para validación
        self.anio = anio  # Usar setter para validación
        self._genero = genero
        self._disponible = disponible

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, value: str) -> None:
        self._titulo = value

    @property
    def autor(self) -> str:
        return self._autor

    @property
    def isbn(self) -> str:
        return self._isbn
        
    @isbn.setter
    def isbn(self, value: str) -> None:
        if not validar_isbn13(value):
            raise ValueError(f"ISBN-13 inválido: {value}")
        self._isbn = value

    @property
    def anio(self) -> int:
        return self._anio
        
    @anio.setter
    def anio(self, value: int) -> None:
        anio_actual = datetime.now().year
        if not (1440 <= value <= anio_actual):
            raise ValueError(f"El año debe estar entre 1440 y {anio_actual}")
        self._anio = value

    @property
    def genero(self) -> str:
        return self._genero

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, value: bool) -> None:
        self._disponible = value
        
    def prestar(self) -> None:
        """Marca el libro como no disponible."""
        if not self._disponible:
            raise ValueError("El libro ya se encuentra prestado.")
        self._disponible = False
        
    def devolver(self) -> None:
        """Restablece la disponibilidad del libro."""
        self._disponible = True
        
    def buscar_coincidencia(self, query: str) -> bool:
        """Busca texto en título, autor o isbn."""
        q = query.lower()
        return q in self._titulo.lower() or q in self._autor.lower() or q in self._isbn.lower()

    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "Prestado"
        return f"Libro: {self._titulo} por {self._autor} ({self._anio}) - {estado}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._isbn}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Libro):
            return False
        return self._isbn == other._isbn

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo": self.__class__.__name__,
            "fecha_creacion": self.fecha_creacion,
            "titulo": self._titulo,
            "autor": self._autor,
            "isbn": self._isbn,
            "anio": self._anio,
            "genero": self._genero,
            "disponible": self._disponible
        }
        
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Crea una instancia de Libro o sus subclases a partir de un diccionario.
        """
        # Extraer parámetros base
        kwargs = {
            "titulo": data.get("titulo", "Sin título"),
            "autor": data.get("autor", "Sin autor"),
            "isbn": data.get("isbn", "0000000000000"),
            "anio": data.get("anio", 2000),
            "genero": data.get("genero", "General"),
            "disponible": data.get("disponible", True)
        }
        
        # Inyectar atributos específicos al llamar a las subclases desde aquí
        # Aunque lo ideal es que cada clase tenga su propio from_dict o maneje la instanciación.
        tipo = data.get("tipo", "Libro")
        
        if tipo == "LibroDigital":
            kwargs["formato"] = data.get("formato", "PDF")
            kwargs["tamano_mb"] = data.get("tamano_mb", 1.0)
            kwargs["url_descarga"] = data.get("url_descarga", "http://ejemplo.com")
            # Devolver directamente la instancia de subclase
            instancia = globals()[tipo](**kwargs)
        elif tipo == "LibroFisico":
            kwargs["ubicacion"] = data.get("ubicacion", "Estante General")
            kwargs["num_ejemplares"] = data.get("num_ejemplares", 1)
            instancia = globals()[tipo](**kwargs)
        else:
            instancia = cls(**kwargs)
            
        # Respetar ID original si existe
        if "id" in data:
            instancia._id = data["id"]
        if "fecha_creacion" in data:
            instancia._fecha_creacion = data["fecha_creacion"]
            
        return instancia

class LibroDigital(Libro):
    """Libro en formato digital."""
    def __init__(self, titulo: str, autor: str, isbn: str, anio: int, genero: str, disponible: bool = True, formato: str = "PDF", tamano_mb: float = 1.0, url_descarga: str = "") -> None:
        super().__init__(titulo, autor, isbn, anio, genero, disponible)
        if formato not in ["PDF", "EPUB", "MOBI"]:
            raise ValueError("Formato inválido. Debe ser PDF, EPUB o MOBI.")
        if tamano_mb <= 0:
            raise ValueError("El tamaño en MB debe ser positivo.")
            
        self._formato = formato
        self._tamano_mb = tamano_mb
        self._url_descarga = url_descarga
        
    def descargar(self) -> str:
        return f"Iniciando descarga desde {self._url_descarga}..."
        
    def __str__(self) -> str:
        return f"{super().__str__()} [Digital: {self._formato}]"
        
    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            "formato": self._formato,
            "tamano_mb": self._tamano_mb,
            "url_descarga": self._url_descarga
        })
        return d

class LibroFisico(Libro):
    """Libro en formato físico."""
    def __init__(self, titulo: str, autor: str, isbn: str, anio: int, genero: str, disponible: bool = True, ubicacion: str = "N/A", num_ejemplares: int = 1) -> None:
        super().__init__(titulo, autor, isbn, anio, genero, disponible)
        if not ubicacion:
            raise ValueError("La ubicación no puede estar vacía.")
        if num_ejemplares < 1:
            raise ValueError("El número de ejemplares debe ser al menos 1.")
            
        self._ubicacion = ubicacion
        self._num_ejemplares = num_ejemplares
        
    def reservar(self) -> str:
        return f"Reservado 1 ejemplar de {self._titulo} en {self._ubicacion}."
        
    def __str__(self) -> str:
        return f"{super().__str__()} [Físico: {self._ubicacion}]"
        
    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            "ubicacion": self._ubicacion,
            "num_ejemplares": self._num_ejemplares
        })
        return d
