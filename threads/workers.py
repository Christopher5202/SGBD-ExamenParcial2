from PySide6.QtCore import QThread, Signal
import time

class ExportWorker(QThread):
    """
    Hilo trabajador para exportar datos sin congelar la GUI.
    """
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, export_func, *args, **kwargs):
        super().__init__()
        self.export_func = export_func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            # Simulamos un proceso largo para demostrar que la GUI no se congela
            for i in range(1, 6):
                time.sleep(0.2)
                self.progress.emit(i * 20)
                
            result = self.export_func(*self.args, **self.kwargs)
            self.finished.emit(f"Exportación exitosa a {result}")
        except Exception as e:
            self.error.emit(str(e))


class MongoSyncWorker(QThread):
    """
    Hilo trabajador genérico para tareas de sincronización o procesos largos.
    """
    finished = Signal()
    
    def __init__(self, task_func):
        super().__init__()
        self.task_func = task_func
        
    def run(self):
        # Ejecutar la tarea (ej. simular sync)
        if self.task_func:
            self.task_func()
        self.finished.emit()
