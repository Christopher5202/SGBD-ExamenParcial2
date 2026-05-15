"""
Módulo de usuarios del sistema.
Define la jerarquía de clases de usuarios.
"""
from abc import abstractmethod
from typing import Optional
from modelos.entidad import Entidad

class Usuario(Entidad):
    """
    Clase abstracta que representa a un usuario genérico del sistema.
    Hereda de Entidad.
    """
    def __init__(self, nombre: str, email: str, contrasena_hash: str) -> None:
        """
        Inicializa un Usuario.
        
        Args:
            nombre (str): Nombre completo del usuario.
            email (str): Correo electrónico validado.
            contrasena_hash (str): Contraseña en formato hash.
        """
        super().__init__()
        self._nombre = nombre
        self._email = email
        self._contrasena_hash = contrasena_hash
        self._libros_prestados = 0

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> str:
        return self._email

    @property
    def libros_prestados(self) -> int:
        return self._libros_prestados
        
    def incrementar_libros(self) -> None:
        """Aumenta en 1 el contador de libros prestados."""
        self._libros_prestados += 1
        
    def decrementar_libros(self) -> None:
        """Disminuye en 1 el contador, si no es cero."""
        if self._libros_prestados > 0:
            self._libros_prestados -= 1

    @abstractmethod
    def puede_pedir_prestado(self) -> bool:
        """
        Determina si el usuario puede realizar otro préstamo.
        
        Returns:
            bool: True si tiene permitidos más libros, False en caso contrario.
        """
        pass

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self._nombre} ({self._email})"

    def to_dict(self) -> dict:
        """Exporta el usuario a diccionario."""
        return {
            "id": self.id,
            "tipo": self.__class__.__name__,
            "fecha_creacion": self.fecha_creacion,
            "nombre": self._nombre,
            "email": self._email,
            "libros_prestados": self._libros_prestados
        }

class Alumno(Usuario):
    """Usuario tipo Alumno."""
    def __init__(self, nombre: str, email: str, contrasena_hash: str, carrera: str, semestre: int) -> None:
        super().__init__(nombre, email, contrasena_hash)
        self._carrera = carrera
        self._semestre = semestre
        self._max_libros = 3

    def calcular_multa(self, dias_retraso: int) -> float:
        """
        Calcula la multa para los alumnos, $5 por día según Tarea 1.3 / 2.4.
        
        Args:
            dias_retraso (int): Número de días.
            
        Returns:
            float: Multa calculada.
        """
        if dias_retraso <= 0: return 0.0
        base = dias_retraso * 5.0
        if dias_retraso > 30: return base * 1.20
        return base

    def puede_pedir_prestado(self) -> bool:
        return self._libros_prestados < self._max_libros
        
    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"carrera": self._carrera, "semestre": self._semestre, "max_libros": self._max_libros})
        return d

class Profesor(Usuario):
    """Usuario tipo Profesor."""
    def __init__(self, nombre: str, email: str, contrasena_hash: str, departamento: str) -> None:
        super().__init__(nombre, email, contrasena_hash)
        self._departamento = departamento
        self._max_libros = 8

    def calcular_multa(self, dias_retraso: int) -> float:
        """
        Calcula la multa para los profesores, $2 por día.
        """
        if dias_retraso <= 0: return 0.0
        base = dias_retraso * 2.0
        if dias_retraso > 30: return base * 1.20
        return base

    def puede_pedir_prestado(self) -> bool:
        return self._libros_prestados < self._max_libros
        
    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"departamento": self._departamento, "max_libros": self._max_libros})
        return d

class Administrador(Usuario):
    """Usuario tipo Administrador, sin límite de libros teóricamente."""
    def __init__(self, nombre: str, email: str, contrasena_hash: str, nivel_acceso: int) -> None:
        super().__init__(nombre, email, contrasena_hash)
        self._nivel_acceso = nivel_acceso

    def calcular_multa(self, dias_retraso: int) -> float:
        return 0.0 # Los admins no pagan multa

    def puede_pedir_prestado(self) -> bool:
        return True # El administrador puede pedir los que quiera.

    def agregar_libro(self) -> str:
        """Método representativo de la clase."""
        return "Acción autorizada: Agregar libro."

    def eliminar_usuario(self) -> str:
        """Método representativo de la clase."""
        return "Acción autorizada: Eliminar usuario."
        
    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"nivel_acceso": self._nivel_acceso})
        return d
