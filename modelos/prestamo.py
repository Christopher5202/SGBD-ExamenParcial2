"""
Módulo de préstamos.
Gestiona el vínculo entre un Usuario y un Libro.
"""
from datetime import datetime
from modelos.entidad import Entidad
from modelos.usuario import Usuario
from modelos.libro import Libro

class Prestamo(Entidad):
    """Representa un préstamo activo o histórico de un libro."""
    def __init__(self, usuario: Usuario, libro: Libro, fecha_prestamo: str = None, fecha_devolucion: str = None, activo: bool = True) -> None:
        super().__init__()
        self._usuario = usuario
        self._libro = libro
        
        # Guardamos como string ISO para serializar fácil, en un proyecto más complejo se usa datetime object
        self._fecha_prestamo = fecha_prestamo or datetime.now().isoformat()
        self._fecha_devolucion = fecha_devolucion
        self._activo = activo
        
    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def libro(self) -> Libro:
        return self._libro

    @property
    def activo(self) -> bool:
        return self._activo

    def calcular_multa(self) -> float:
        """
        Calcula la multa actual delegando el cálculo al tipo de usuario.
        """
        if not self._fecha_devolucion:
            # Si no se ha devuelto, multas hipotéticas hasta hoy
            fecha_fin = datetime.now()
        else:
            fecha_fin = datetime.fromisoformat(self._fecha_devolucion)
            
        fecha_inicio = datetime.fromisoformat(self._fecha_prestamo)
        dias_prestamo = (fecha_fin - fecha_inicio).days
        
        # Asumiendo que el plazo gratis es de 14 días para todos.
        dias_retraso = max(0, dias_prestamo - 14)
        
        # El usuario calcula su multa basado en el retraso
        return self._usuario.calcular_multa(dias_retraso)
        
    def cerrar(self) -> None:
        """Da por terminado el préstamo."""
        if not self._activo:
            raise ValueError("El préstamo ya está cerrado.")
        self._activo = False
        self._fecha_devolucion = datetime.now().isoformat()
        
    def __str__(self) -> str:
        estado = "Activo" if self._activo else "Cerrado"
        return f"Prestamo: '{self._libro.titulo}' a {self._usuario.nombre} - [{estado}]"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo": self.__class__.__name__,
            "fecha_creacion": self.fecha_creacion,
            "usuario_email": self._usuario.email,
            "libro_isbn": self._libro.isbn,
            "fecha_prestamo": self._fecha_prestamo,
            "fecha_devolucion": self._fecha_devolucion,
            "activo": self._activo
        }
