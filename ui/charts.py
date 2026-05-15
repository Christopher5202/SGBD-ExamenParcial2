try:
    from PySide6.QtWidgets import QVBoxLayout, QWidget  # type: ignore
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
except ImportError:
    # Fallback si matplotlib no está instalado para que no truene la app completa
    plt = None
    FigureCanvas = None
    Figure = None

class ChartsPanel(QWidget):
    """Panel para mostrar gráficas de estadísticas usando Matplotlib en PySide6."""
    
    def __init__(self, sql_repo, parent=None):
        super().__init__(parent)
        self.sql_repo = sql_repo
        self.layout = QVBoxLayout(self)
        
        if Figure is None:
            from PySide6.QtWidgets import QLabel
            self.layout.addWidget(QLabel("Matplotlib no está instalado. Instálalo con: py -m pip install matplotlib"))
            self.figure = None
            return

        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Estilo para fondo oscuro si se requiere
        self.figure.patch.set_facecolor('#2b2b2b')
        
    def actualizar_graficas(self):
        """Dibuja 2 gráficas en la figura (Libros más prestados y Préstamos por estado)."""
        if self.figure is None:
            return
        self.figure.clear()
        
        # Obtener datos reales de SQL
        prestamos = self.sql_repo.get_prestamos()
        
        # 1. Conteo de préstamos por estado
        estados = [p['estado'] for p in prestamos]
        conteo_estados = {est: estados.count(est) for est in set(estados)}
        
        # 2. Top libros prestados
        isbns = [p['libro_isbn'] for p in prestamos]
        conteo_libros = {isbn: isbns.count(isbn) for isbn in set(isbns)}
        
        # Fondo oscuro global y color de texto blanco
        self.figure.patch.set_facecolor('#1e1e1e')
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'

        def setup_ax(ax):
            ax.set_facecolor('#1e1e1e')
            for spine in ax.spines.values():
                spine.set_color('#444444')
                
        # Subplot 1: Estado de Préstamos (Pastel)
        ax1 = self.figure.add_subplot(121)
        ax1.set_title("Estado de Préstamos", color='white', pad=20, fontsize=14)
        if conteo_estados:
            ax1.pie(conteo_estados.values(), labels=conteo_estados.keys(), autopct='%1.1f%%', textprops={'color':"w", 'fontsize': 10}, startangle=90, colors=['#4CAF50', '#F44336', '#2196F3', '#FFC107'])
        else:
            ax1.text(0.5, 0.5, "Aún no hay préstamos registrados", color='#888888', ha='center', va='center', fontsize=12)
            ax1.axis('off') # Ocultar completamente los ejes y números
            
        # Subplot 2: Top libros (Barras)
        ax2 = self.figure.add_subplot(122)
        ax2.set_title("Libros más solicitados", color='white', pad=20, fontsize=14)
        setup_ax(ax2)
        
        if conteo_libros:
            top_libros = dict(sorted(conteo_libros.items(), key=lambda item: item[1], reverse=True)[:5])
            bars = ax2.bar(top_libros.keys(), top_libros.values(), color='#2196F3', edgecolor='#1976D2')
            ax2.set_ylabel("Cantidad de Préstamos", color='white')
            # Forzar valores enteros en el eje Y
            ax2.yaxis.get_major_locator().set_params(integer=True)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha="right")
        else:
            ax2.text(0.5, 0.5, "No hay datos para mostrar", color='#888888', ha='center', va='center', fontsize=12)
            ax2.axis('off') # Ocultar completamente los ejes
            
        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()
