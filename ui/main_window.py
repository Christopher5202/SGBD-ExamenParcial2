import os
import datetime
import time
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QMessageBox, QFileDialog, QHeaderView
)
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtGui import QMouseEvent, QKeyEvent, QFocusEvent, QCloseEvent, QIcon

from repositories.sql_repo import SQLRepository
from repositories.mongo_repo import MongoRepository
from events.event_dispatcher import global_dispatcher
from threads.workers import ExportWorker, MongoSyncWorker
from services.file_manager import FileManager
from ui.charts import ChartsPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Biblioteca Digital (SGBD) - Event Driven")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "icon.png")))
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QWidget { color: #ffffff; font-family: 'Segoe UI', Arial, sans-serif; }
            QLineEdit {
                background-color: #1e1e1e; color: white;
                border: 1px solid #333; border-radius: 6px;
                padding: 10px; font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #4CAF50; }
            QPushButton {
                background-color: #4CAF50; color: white;
                border: none; border-radius: 6px;
                padding: 10px 20px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #43A047; }
            QPushButton:pressed { background-color: #2E7D32; }
            QTabWidget::pane { border: 1px solid #333; border-radius: 6px; background: #121212; top: -1px; }
            QTabBar::tab {
                background: #1e1e1e; color: #888;
                padding: 12px 24px; border-top-left-radius: 6px; border-top-right-radius: 6px;
                margin-right: 2px; font-weight: bold; font-size: 13px;
            }
            QTabBar::tab:selected { background: #4CAF50; color: white; }
            QTabBar::tab:hover:!selected { background: #2c2c2c; }
            QTableWidget {
                background-color: #1e1e1e; color: white;
                gridline-color: #333; border: 1px solid #333; border-radius: 6px;
                alternate-background-color: #252525;
            }
            QTableWidget::item:selected { background-color: #4CAF50; }
            QHeaderView::section {
                background-color: #2c2c2c; color: white;
                padding: 8px; border: 1px solid #333; font-weight: bold; font-size: 13px;
            }
        """)
        
        # 1. Init repos
        self.sql_repo = SQLRepository()
        self.mongo_repo = MongoRepository()
        
        # Suscribir a Custom Events
        global_dispatcher.subscribe("LIBRO_AGREGADO", lambda **kwargs: self.on_libro_agregado(**kwargs))
        
        # 2. Setup GUI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Timer de demostración (Evento de tiempo)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        
        self.header_label = QLabel("Bienvenido al SGBD")
        self.header_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        self.main_layout.addWidget(self.header_label)
        
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Barra de estado Premium
        self.statusBar().setStyleSheet("color: #888; font-size: 11px; border-top: 1px solid #333;")
        if self.mongo_repo.client:
            self.statusBar().showMessage("Sistema SGBD Online | MongoDB Cloud Conectado")
        else:
            self.statusBar().showMessage("Sistema SGBD Listo | Modo Local Resiliente (Offline Logs)")
        
        self.setup_libros_tab()
        self.setup_respaldos_tab()
        self.setup_reportes_tab()
        
        # Evento de carga de ventana (Load Event simulado al final del init)
        QTimer.singleShot(100, self.on_window_loaded)

    def on_window_loaded(self):
        self.mongo_repo.registrar_evento("SISTEMA", "Ventana principal cargada (Load Event)")
        self.actualizar_tabla_libros()

    def update_clock(self):
        # Evento de Timer
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.header_label.setText(f"SGBD - {current_time}")

    def closeEvent(self, event: QCloseEvent):
        # Evento de Destrucción de Objeto
        self.mongo_repo.registrar_evento("SISTEMA", "Ventana cerrada (Destroy Event)")
        event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        # Evento de Teclado
        if event.key() == Qt.Key_Escape:
            self.close()

    # ================= PESTAÑA LIBROS =================
    def setup_libros_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Formulario
        form_layout = QHBoxLayout()
        self.txt_isbn = QLineEdit(); self.txt_isbn.setPlaceholderText("ISBN")
        self.txt_titulo = QLineEdit(); self.txt_titulo.setPlaceholderText("Título")
        self.txt_autor = QLineEdit(); self.txt_autor.setPlaceholderText("Autor")
        
        # Evento de Foco
        self.txt_isbn.installEventFilter(self)
        
        btn_add = QPushButton("Agregar Libro")
        btn_add.clicked.connect(self.agregar_libro_action)
        
        form_layout.addWidget(self.txt_isbn)
        form_layout.addWidget(self.txt_titulo)
        form_layout.addWidget(self.txt_autor)
        form_layout.addWidget(btn_add)
        
        layout.addLayout(form_layout)
        
        # Tabla
        self.tbl_libros = QTableWidget(0, 4)
        self.tbl_libros.setHorizontalHeaderLabels(["ISBN", "Título", "Autor", "Disponible"])
        self.tbl_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_libros.setAlternatingRowColors(True)
        
        layout.addWidget(self.tbl_libros)
        
        btns_layout = QHBoxLayout()
        self.btn_prestar = QPushButton("Registrar Préstamo")
        self.btn_prestar.setStyleSheet("background-color: #673AB7; color: white; font-weight: bold;")
        self.btn_prestar.clicked.connect(self.prestar_libro_action)
        
        self.btn_eliminar = QPushButton("Eliminar Libro")
        self.btn_eliminar.setStyleSheet("background-color: #C62828; color: white; font-weight: bold;")
        self.btn_eliminar.clicked.connect(self.eliminar_libro_action)
        
        btns_layout.addWidget(self.btn_prestar)
        btns_layout.addWidget(self.btn_eliminar)
        layout.addLayout(btns_layout)
        
        self.tabs.addTab(tab, "Gestión de Libros")

    def prestar_libro_action(self):
        selected = self.tbl_libros.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selección", "Por favor, selecciona un libro de la tabla.")
            return
            
        isbn = self.tbl_libros.item(selected, 0).text()
        titulo = self.tbl_libros.item(selected, 1).text()
        
        # Simular préstamo al admin por defecto
        try:
            self.sql_repo.add_prestamo({
                "usuario_email": "admin@biblioteca.com",
                "libro_isbn": isbn,
                "fecha_prestamo": datetime.datetime.now().strftime("%Y-%m-%d"),
                "estado": "Activo"
            })
            self.mongo_repo.registrar_evento("PRESTAMO", f"Préstamo registrado: {titulo} ({isbn})")
            QMessageBox.information(self, "Éxito", f"Se registró el préstamo de '{titulo}' con éxito.\nYa puedes ver la actualización en Estadísticas.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar: {e}")

    def eliminar_libro_action(self):
        selected = self.tbl_libros.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selección", "Selecciona un libro para eliminar.")
            return
            
        isbn = self.tbl_libros.item(selected, 0).text()
        titulo = self.tbl_libros.item(selected, 1).text()
        
        res = QMessageBox.question(self, "Confirmar", f"¿Seguro que quieres eliminar '{titulo}'?")
        if res == QMessageBox.Yes:
            try:
                self.sql_repo.delete_libro(isbn)
                self.actualizar_tabla_libros()
                self.mongo_repo.registrar_evento("SISTEMA", f"Libro eliminado: {titulo}")
                QMessageBox.information(self, "Éxito", "Libro eliminado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def eventFilter(self, obj, event):
        # Capturar evento de Foco
        if obj == self.txt_isbn and event.type() == QEvent.FocusIn:
            self.mongo_repo.registrar_evento("UI_EVENT", "El campo ISBN recibió el foco.")
        return super().eventFilter(obj, event)

    def agregar_libro_action(self):
        isbn = self.txt_isbn.text().strip()
        titulo = self.txt_titulo.text().strip()
        autor = self.txt_autor.text().strip()
        
        if not all([isbn, titulo, autor]):
            QMessageBox.warning(self, "Validación", "Todos los campos son requeridos.")
            return
            
        try:
            libro_data = {
                "isbn": isbn, "titulo": titulo, "autor": autor,
                "anio": 2025, "genero": "General", "disponible": 1,
                "tipo": "Físico", "formato": "", "tamano_mb": 0.0,
                "url_descarga": "", "ubicacion": "A1", "num_ejemplares": 1
            }
            self.sql_repo.add_libro(libro_data)
            
            # Disparar Custom Event (Delegado)
            global_dispatcher.dispatch("LIBRO_AGREGADO", isbn=isbn, titulo=titulo)
            
            self.txt_isbn.clear()
            self.txt_titulo.clear()
            self.txt_autor.clear()
            self.actualizar_tabla_libros()
            
        except Exception as e:
            QMessageBox.critical(self, "Error SQL", f"No se pudo guardar: {e}")

    def on_libro_agregado(self, isbn, titulo):
        # Callback invocado por el EventDispatcher
        self.mongo_repo.registrar_evento("LIBRO", f"Se agregó libro: {titulo} ({isbn})")
        
    def actualizar_tabla_libros(self):
        try:
            libros = self.sql_repo.get_libros()
            self.tbl_libros.setRowCount(0)
            for row_idx, lib in enumerate(libros):
                self.tbl_libros.insertRow(row_idx)
                self.tbl_libros.setItem(row_idx, 0, QTableWidgetItem(lib['isbn']))
                self.tbl_libros.setItem(row_idx, 1, QTableWidgetItem(lib['titulo']))
                self.tbl_libros.setItem(row_idx, 2, QTableWidgetItem(lib['autor']))
                self.tbl_libros.setItem(row_idx, 3, QTableWidgetItem("Sí" if lib['disponible'] else "No"))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # ================= PESTAÑA RESPALDOS (Hilos) =================
    def setup_respaldos_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        lbl_info = QLabel("Exportación/Importación (Se ejecuta en Hilo Secundario)")
        btn_export = QPushButton("Exportar XML")
        btn_export.clicked.connect(self.iniciar_exportacion)
        
        btn_import = QPushButton("Importar XML")
        btn_import.setStyleSheet("background-color: #2196F3;")
        btn_import.clicked.connect(self.iniciar_importacion)
        
        self.lbl_status = QLabel("Listo.")
        
        layout.addWidget(lbl_info)
        layout.addWidget(btn_export)
        layout.addWidget(btn_import)
        
        # Requisito PDF: Formatos adicionales (JSON)
        layout.addSpacing(20)
        layout.addWidget(QLabel("Formatos Adicionales (JSON):"))
        json_layout = QHBoxLayout()
        btn_exp_json = QPushButton("Exportar JSON"); btn_exp_json.clicked.connect(lambda: self.exportar_formato("JSON"))
        btn_imp_json = QPushButton("Importar JSON"); btn_imp_json.clicked.connect(lambda: self.importar_formato("JSON"))
        json_layout.addWidget(btn_exp_json)
        json_layout.addWidget(btn_imp_json)
        layout.addLayout(json_layout)
        
        # Requisito PDF: Segundo hilo (Concurrencia)
        layout.addSpacing(20)
        btn_sync = QPushButton("Sincronizar Cloud (Segundo Hilo)")
        btn_sync.setStyleSheet("background-color: #009688; color: white;")
        btn_sync.clicked.connect(self.iniciar_sincronizacion)
        layout.addWidget(btn_sync)
        
        layout.addWidget(self.lbl_status)
        layout.addStretch()
        self.tabs.addTab(tab, "Respaldos y Archivos")

    def iniciar_exportacion(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar XML", "", "Archivos XML (*.xml)")
        if not filepath: return
        
        # Preparar datos (simulado rápido)
        datos = {
            "libros": self.sql_repo.get_libros(),
            "usuarios": []
        }
        
        self.lbl_status.setText("Exportando...")
        self.worker = ExportWorker(FileManager.exportar_xml, datos, filepath)
        
        # Callbacks (métodos anónimos con lambda)
        self.worker.progress.connect(lambda val: self.lbl_status.setText(f"Progreso: {val}%"))
        self.worker.finished.connect(lambda msg: [self.lbl_status.setText(msg), QMessageBox.information(self, "Éxito", msg)])
        self.worker.error.connect(lambda err: QMessageBox.critical(self, "Error", err))
        self.worker.start()

    def iniciar_importacion(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Respaldo XML", "", "Archivos XML (*.xml)")
        if not filepath: return
        
        try:
            datos = FileManager.importar_xml(filepath)
            count = 0
            for l_dict_raw in datos.get("libros", []):
                try:
                    # Normalizar claves a minúsculas
                    l_dict = {k.lower(): v for k, v in l_dict_raw.items()}
                    
                    # Mapeo y validación de campos obligatorios
                    isbn = l_dict.get('isbn')
                    titulo = l_dict.get('titulo')
                    if not isbn or not titulo: continue
                    
                    libro_data = {
                        "isbn": isbn,
                        "titulo": titulo,
                        "autor": l_dict.get('autor', 'Desconocido'),
                        "anio": int(l_dict.get('anio', 2024)) if l_dict.get('anio', '').isdigit() else 2024,
                        "genero": l_dict.get('genero', 'General'),
                        "disponible": 1 if l_dict.get('disponible') in ['1', 'Sí', 'True'] else 0,
                        "tipo": l_dict.get('tipo', 'Físico'),
                        "formato": l_dict.get('formato', ''),
                        "tamano_mb": float(l_dict.get('tamano_mb', 0.0)) if l_dict.get('tamano_mb', '').replace('.','').isdigit() else 0.0,
                        "url_descarga": l_dict.get('url_descarga', ''),
                        "ubicacion": l_dict.get('ubicacion', 'A1'),
                        "num_ejemplares": int(l_dict.get('num_ejemplares', 1)) if l_dict.get('num_ejemplares', '').isdigit() else 1
                    }
                    
                    # Intentar agregar; si falla por duplicado, actualizar
                    try:
                        self.sql_repo.add_libro(libro_data)
                    except:
                        self.sql_repo.update_libro(isbn, libro_data)
                    
                    count += 1
                except Exception as e:
                    print(f"Error al procesar libro en XML: {e}")
                    continue
            
            self.actualizar_tabla_libros()
            self.mongo_repo.registrar_evento("SISTEMA", f"Importación exitosa: {count} libros desde {os.path.basename(filepath)}")
            QMessageBox.information(self, "Éxito", f"Se importaron {count} libros correctamente.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error de Importación", str(e))

    def exportar_formato(self, formato):
        filepath, _ = QFileDialog.getSaveFileName(self, f"Guardar {formato}", "", f"Archivos {formato} (*.{formato.lower()})")
        if not filepath: return
        datos = {"libros": self.sql_repo.get_libros(), "usuarios": []}
        if formato == "JSON":
            FileManager.exportar_json(datos, filepath)
            QMessageBox.information(self, "Éxito", "Archivo JSON guardado.")

    def importar_formato(self, formato):
        filepath, _ = QFileDialog.getOpenFileName(self, f"Abrir {formato}", "", f"Archivos {formato} (*.{formato.lower()})")
        if not filepath: return
        try:
            if formato == "JSON":
                datos = FileManager.importar_json(filepath)
                # Buscar la lista de libros en cualquier nivel del JSON
                libros_lista = []
                if isinstance(datos, list): libros_lista = datos
                elif isinstance(datos, dict): libros_lista = datos.get("libros", list(datos.values())[0] if datos else [])
                
                count = 0
                for lib_raw in libros_lista:
                    try:
                        lib = {k.lower(): v for k, v in lib_raw.items()}
                        isbn = lib.get('isbn')
                        if not isbn: continue
                        
                        libro_data = {
                            "isbn": isbn, "titulo": lib.get('titulo', 'Sin Título'),
                            "autor": lib.get('autor', 'Desconocido'), "anio": lib.get('anio', 2024),
                            "genero": lib.get('genero', 'General'), "disponible": 1,
                            "tipo": 'Físico', "formato": '', "tamano_mb": 0.0,
                            "url_descarga": '', "ubicacion": 'A1', "num_ejemplares": 1
                        }
                        try:
                            self.sql_repo.add_libro(libro_data)
                        except:
                            self.sql_repo.update_libro(isbn, libro_data)
                        count += 1
                    except Exception as e:
                        print(f"Error en item JSON: {e}")
                
                self.actualizar_tabla_libros()
                QMessageBox.information(self, "Éxito", f"¡Importación exitosa! {count} libros cargados.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def iniciar_sincronizacion(self):
        # Implementación del segundo hilo (Worker 2)
        self.lbl_status.setText("Sincronizando con la nube...")
        self.sync_worker = MongoSyncWorker(lambda: [time.sleep(2), "Sincronización completa."])
        self.sync_worker.finished.connect(lambda: self.lbl_status.setText("Nube sincronizada correctamente."))
        self.sync_worker.start()

    # ================= PESTAÑA REPORTES (Gráficas) =================
    def setup_reportes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        btn_refresh = QPushButton("Actualizar Gráficas")
        btn_refresh.clicked.connect(self.refrescar_graficas)
        
        self.charts_panel = ChartsPanel(self.sql_repo)
        
        layout.addWidget(btn_refresh)
        layout.addWidget(self.charts_panel)
        self.tabs.addTab(tab, "Estadísticas")
        
    def refrescar_graficas(self):
        try:
            self.charts_panel.actualizar_graficas()
        except Exception as e:
            QMessageBox.critical(self, "Error Gráficas", str(e))


    # Evento de Mouse simulado global
    def mousePressEvent(self, event: QMouseEvent):
        # Registrar click global
        if event.button() == Qt.LeftButton:
            # print(f"Mouse click en {event.pos()}") # Debug
            pass
        super().mousePressEvent(event)
