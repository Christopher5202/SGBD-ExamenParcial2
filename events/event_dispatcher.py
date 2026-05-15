from typing import Callable, Dict, List

class EventDispatcher:
    """
    Despachador de eventos personalizado. 
    Implementa el patrón Observador / Delegados.
    """
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        """Suscribe un callback a un tipo de evento específico."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        """Elimina la suscripción de un callback."""
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def dispatch(self, event_type: str, **kwargs):
        """Dispara un evento llamando a todos los callbacks suscritos."""
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(**kwargs)

# Instancia global para facilitar el acceso
global_dispatcher = EventDispatcher()
