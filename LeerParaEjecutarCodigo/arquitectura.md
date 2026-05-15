# Arquitectura del Sistema (SGBD Event-Driven)

## 1. Patrón Arquitectónico
El sistema emplea una arquitectura Orientada a Eventos apoyada en un patrón similar a MVC (Modelo-Vista-Controlador), separando responsabilidades:
- **UI (`ui/`)**: La Vista. Gestiona los widgets de PySide6 (`MainWindow`, `ChartsPanel`). Despacha eventos UI.
- **Repositorios (`repositories/`)**: Data Access Layer. `SQLRepository` para transacciones (SQLite) y `MongoRepository` para bitácora NoSQL (MongoDB).
- **Hilos (`threads/`)**: Clases basadas en `QThread` para concurrencia. Evitan bloqueos en la GUI en operaciones de E/S.
- **Servicios (`services/`)**: Lógica de negocio pura (ej. `FileManager` para JSON/XML).
- **Eventos (`events/`)**: `EventDispatcher` implementa el patrón Observador para coordinar eventos propios del programador.

## 2. Mapa de Eventos Implementados
1. **Load Event**: Registro de carga en MongoDB al iniciar.
2. **Timer Event**: Actualización de reloj cada segundo.
3. **Focus Event**: Captura de foco en campo ISBN para auditoría.
4. **Keyboard Event**: Tecla `ESC` para cierre seguro de la aplicación.
5. **Mouse Event**: Registro de clics globales para trazabilidad de usuario.
6. **Destroy Event**: Registro de cierre en Mongo antes de liberar memoria.
7. **Custom Event**: `LIBRO_AGREGADO`. Desacopla la UI de los logs de Mongo.
8. **GUI Events**: Botones de **Eliminar** (CRUD), **Importar** (Archivos) y **Sincronizar** (Hilos).

## 3. Flujo Híbrido y Concurrencia
- **SQL (Transaccional)**: Gestión de Libros y Préstamos. Soporta CRUD completo.
- **MongoDB (Auditoría)**: Bitácora de eventos con modo resiliente (offline).
- **Multithreading**:
  - `ExportWorker`: Maneja exportación masiva XML/JSON.
  - `MongoSyncWorker`: Simula sincronización de datos con servicios externos/cloud.
