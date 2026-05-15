# Log de Prompts - Examen Práctico 2 (SGBD)

**Equipo:**
- Christopher Mercado Salcedo
- Jose Luis Diaz Ibarra
- Ivan Aguirre Mora
- Leonardo Javier Navarro Esquivel

---

## Prompt 1: Reorganización del repositorio y base SQL (Tarea 3.1 y 4.1)
- **LLM Usada:** Agent Code LLM (Gemini 3.1 Pro)
- **Integrante:** Christopher Mercado Salcedo
- **Fecha/Hora:** 09/Mayo/2026
- **Prompt Enviado:** 
  > *Mi app ya tiene modelo Libro y repo Git previo; añade handlers de foco, temporizador y exportación JSON/XML. Necesito una propuesta de reorganización del repositorio para una versión con GUI, eventos, SQL, Mongo y workers en hilos. Dame la estructura de carpetas, comandos Git recomendados.*
- **Respuesta Resumida:** La IA propuso crear las carpetas `ui/`, `controllers/`, `events/`, `threads/`, `repositories/` y separó la responsabilidad de SQL en `sql_repo.py` usando `sqlite3`.
- **Código Adoptado/Modificado:** Adoptamos la clase `SQLRepository` para manejar la DB transaccional y movimos `main_window.py` a `ui/`. Modificamos las consultas para usar diccionarios y `sqlite3.Row` para facilitar la inyección a la UI.
- **Correcciones del Equipo:** Agregamos `IF NOT EXISTS` a las tablas y modificamos el esquema para que coincida exactamente con los atributos del objeto Libro y Usuario.
- **Tema del Curso Implementado:** SQL y Arquitectura de Software.

---

## Prompt 2: Eventos y GUI PySide6 (Tarea 3.2, 3.4 y 4.4)
- **LLM Usada:** Agent Code LLM
- **Integrante:** Jose Luis Diaz Ibarra
- **Fecha/Hora:** 09/Mayo/2026
- **Prompt Enviado:**
  > *Crea una ventana con Treeview, callbacks y SQL parametrizado, sin bloquear la interfaz. Necesito una lista concreta de eventos: mouse, teclado, temporizador, carga, foco, destrucción y un evento personalizado para cuando se agregue un libro. Dame ejemplos de handlers.*
- **Respuesta Resumida:** Generó el `MainWindow` en PySide6. Agregó `eventFilter` para el foco, `keyPressEvent` para el teclado (Escape cierra la app), y `QTimer` para el reloj. 
- **Código Adoptado/Modificado:** Integramos el `QTableWidget` en lugar de Treeview de Tkinter para un aspecto más moderno, validamos campos vacíos con `QMessageBox` (try/except).
- **Correcciones del Equipo:** Cambiamos los nombres de los métodos a español y enlazamos el Custom Event a nuestro propio despachador (`EventDispatcher`).
- **Tema del Curso Implementado:** Programación Orientada a Eventos y GUI.

---

## Prompt 3: Delegados y Hilos / Workers (Tarea 3.3 y 3.6)
- **LLM Usada:** Agent Code LLM
- **Integrante:** Ivan Aguirre Mora
- **Fecha/Hora:** 09/Mayo/2026
- **Prompt Enviado:**
  > *Tu solución mezcla UI y SQL en la exportación; refactórala con controlador, worker thread y evento personalizado al guardar para que la GUI no se congele al exportar a XML.*
- **Respuesta Resumida:** Creó `ExportWorker` heredando de `QThread`. Implementó señales (`progress`, `finished`, `error`) y sugirió usar lambdas en la vista para recibir las señales.
- **Código Adoptado/Modificado:** Creamos el archivo `threads/workers.py` e implementamos los delegados anónimos (lambdas) directamente en el método `iniciar_exportacion` de la ventana.
- **Correcciones del Equipo:** Agregamos una simulación de carga con `time.sleep` en el hilo para demostrar empíricamente que la GUI sigue responsiva.
- **Tema del Curso Implementado:** Hilos (Threads), Delegados y Métodos Anónimos.

---

## Prompt 4: MongoDB y Gráficas Matplotlib (Tarea 4.2 y 4.5)
- **LLM Usada:** Agent Code LLM
- **Integrante:** Leonardo Javier Navarro Esquivel
- **Fecha/Hora:** 09/Mayo/2026
- **Prompt Enviado:**
  > *Quiero mostrar estadísticas de mi sistema de biblioteca en Python con una tabla y dos gráficas usando Matplotlib. También, ayúdame a usar Mongo para guardar la bitácora de eventos con try/except para que no truene si Mongo está apagado.*
- **Respuesta Resumida:** Implementó `MongoRepository` con PyMongo usando timeout de 2000ms. Y creó un `FigureCanvasQTAgg` con dos subplots para libros prestados y estado de préstamos.
- **Código Adoptado/Modificado:** Adaptamos la gráfica de barras para que lea las entidades directo desde `sql_repo` filtradas por estado. Integramos `mongo_repo.registrar_evento` en el `closeEvent` y `on_window_loaded`.
- **Correcciones del Equipo:** Manejo de la excepción `ServerSelectionTimeoutError` para permitir que el sistema funcione offline (solo SQL) sin congelarse, demostrando resiliencia.
- **Tema del Curso Implementado:** Mongo DB, Gráficos de Datos y Excepciones.

---

## Prompt 5: Resiliencia y Modo Offline (Tarea 3.5)
- **LLM Usada:** Agent Code LLM
- **Integrante:** Christopher Mercado Salcedo
- **Fecha/Hora:** 15/Mayo/2026
- **Prompt Enviado:**
-   > *Mi app lanza advertencias de MongoDB si no está instalado. Haz que el error sea silencioso y que el sistema use un "Modo Local Resiliente" para que no se vea feo en el examen.*
- **Respuesta Resumida:** Modificó el bloque try/except en `mongo_repo.py` para silenciar el log de advertencia y actualizó la barra de estado de la UI para informar el modo local.
- **Tema del Curso Implementado:** Tratamiento de Excepciones.

---

## Prompt 6: Concurrencia y Serialización Completa (Tarea 3.6, 3.7 y 4.3)
- **LLM Usada:** Agent Code LLM
- **Integrante:** Jose Luis Diaz Ibarra
- **Fecha/Hora:** 15/Mayo/2026
- **Prompt Enviado:**
-   > *La rúbrica pide dos hilos y soporte para JSON además de XML. Añade un segundo worker para sincronización y botones para importar/exportar JSON desde la GUI.*
- **Respuesta Resumida:** Implementó `MongoSyncWorker` como un hilo genérico y añadió la lógica de delegados para JSON en `main_window.py`.
- **Tema del Curso Implementado:** Hilos (Threads) y Manejo de Archivos.

---

## Prompt 7: CRUD Completo e Integración Final (Tarea 4.1, 4.4 y 4.6)
- **LLM Usada:** Agent Code LLM
- **Integrante:** Leonardo Javier Navarro Esquivel
- **Fecha/Hora:** 15/Mayo/2026
- **Prompt Enviado:**
-   > *Falta la 'D' del CRUD. Añade un botón para eliminar libros y deja el sistema limpio borrando los botones de prueba para que el profesor lo use desde cero.*
- **Respuesta Resumida:** Añadió `eliminar_libro_action` con cuadros de diálogo de confirmación y limpió la interfaz para producción.
- **Tema del Curso Implementado:** SQL CRUD y Entrega de Software.
