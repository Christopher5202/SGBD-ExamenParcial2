import sys
import os

# Asegurar que el sistema reconozca el directorio actual para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PySide6.QtWidgets import QApplication, QMessageBox
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Error: No se pudieron importar las librerías necesarias. {e}")
    print("Por favor, instala las dependencias ejecutando:")
    print("py -m pip install PySide6 pymongo matplotlib")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado al iniciar: {e}")
    sys.exit(1)

def main():
    """
    Punto de entrada principal.
    Inicializa la aplicación PySide6.
    """
    app = QApplication(sys.argv)
    
    # Aplicar estilo global moderno (dark theme simplificado)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
