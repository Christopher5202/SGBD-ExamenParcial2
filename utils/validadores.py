"""
Módulo de validadores.
Contiene funciones para validar reglas de negocio básicas.
"""

def validar_isbn13(isbn: str) -> bool:
    """
    Verifica que la cadena dada sea un ISBN-13 válido.
    
    Reglas:
    1. Debe tener exactamente 13 caracteres.
    2. Todos los caracteres deben ser dígitos.
    3. El dígito de control (último) debe cumplir el algoritmo estándar ISBN-13.
    
    Args:
        isbn (str): Cadena a verificar.
        
    Returns:
        bool: True si es un ISBN-13 válido, False en caso contrario.

    Ejemplos (Doctest manual):
    >>> validar_isbn13("9780596520687")
    True
    >>> validar_isbn13("9780596520688")
    False
    """
    if len(isbn) != 13:
        return False
    
    if not isbn.isdigit():
        return False
    
    # Algoritmo de validación ISBN-13
    suma = 0
    for i in range(12):
        digito = int(isbn[i])
        if i % 2 == 0:
            suma += digito * 1
        else:
            suma += digito * 3
            
    digito_verificador_calculado = 10 - (suma % 10)
    if digito_verificador_calculado == 10:
        digito_verificador_calculado = 0
        
    return digito_verificador_calculado == int(isbn[12])

def validar_email(email: str) -> bool:
    """
    Verifica que la cadena dada tenga forma básica de correo electrónico.
    
    Reglas:
    1. Contiene al menos un carácter '@'.
    2. Después del '@', existe un dominio de al menos 3 caracteres que contiene al menos un '.'.
    
    Args:
        email (str): Cadena a verificar.
        
    Returns:
        bool: True si tiene apariencia de email, False en caso contrario.
    """
    if email is None:
        return False
        
    if "@" not in email:
        return False
        
    partes = email.split("@")
    if len(partes) != 2:
        return False
        
    usuario, dominio = partes
    if len(usuario) == 0 or len(dominio) < 3:
        return False
        
    if "." not in dominio:
        return False
        
    if dominio.startswith(".") or dominio.endswith("."):
        return False
        
    return True
