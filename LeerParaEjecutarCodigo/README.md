# SGBD-ExamenParcial2 - Sistema de Gestión de Biblioteca Digital

Este proyecto es la solución al **Examen Práctico 2**, el cual implementa una arquitectura Orientada a Eventos (Event-Driven) para un Sistema de Gestión de Biblioteca.

## Integrantes del Equipo
- Christopher Mercado Salcedo
- Jose Luis Diaz Ibarra
- Ivan Aguirre Mora
- Leonardo Javier Navarro Esquivel

## Características Principales
- **Arquitectura Event-Driven**: Implementación de eventos de mouse, teclado, foco, tiempo (timers), carga, destrucción y eventos personalizados.
- **GUI Moderna**: Desarrollada en **PySide6** (Qt) con diseño responsivo, temas oscuros y barra de estado dinámica.
- **CRUD Completo**: Gestión total de libros (Alta, Baja, Consulta) desde la interfaz gráfica.
- **Concurrencia (Hilos)**: 
  - **Worker 1**: Exportación de datos masivos.
  - **Worker 2**: Sincronización simulada con la nube (Cloud Sync).
- **Persistencia Híbrida**: 
  - **SQLite**: Gestión transaccional de libros y usuarios.
  - **MongoDB**: Bitácora de auditoría y logs de sistema (con modo offline resiliente).
- **Formatos de Intercambio**: Soporte completo para importación y exportación en **JSON y XML**.
- **Visualización de Datos**: Gráficas de Matplotlib integradas (Pastel y Barras) que se alimentan de datos reales.

---

## 🚀 Guía de Ejecución

### 1. Requisitos Previos
- **Python 3.10+**

### 2. Instalación de Dependencias
Abre tu terminal y ejecuta el siguiente comando para instalar todo de una vez:
```bash
pip install PySide6 pymongo matplotlib dnspython
```
*O si prefieres usar el archivo de requerimientos:*
```bash
pip install -r LeerParaEjecutarCodigo/requirements.txt
```

### 3. Ejecutar el Proyecto
En la terminal, ejecuta:
```bash
python main.py
```

### 3. Flujo de Prueba Sugerido para Evaluación
1. **Importar Datos**: Ve a "Respaldos" e importa el archivo `respaldo_examen.xml` (ubicado en Descargas).
2. **Gestionar Libros**: Agrega un nuevo libro o elimina uno existente para validar el CRUD.
3. **Registrar Préstamo**: Selecciona un libro y presiona "Registrar Préstamo".
4. **Ver Gráficas**: Ve a la pestaña "Estadísticas" para ver el análisis de los datos ingresados.
5. **Sincronizar**: Usa el botón de "Sincronizar Cloud" para demostrar el uso de múltiples hilos.

## Estructura del Proyecto
- `ui/`: Vistas y widgets gráficos (PySide6).
- `repositories/`: Capa de acceso a datos (SQLite y MongoDB).
- `threads/`: Manejo de concurrencia y workers en segundo plano.
- `events/`: Despachador de eventos personalizados (Observer Pattern).
- `services/`: Lógica de serialización JSON/XML.
- `LeerParaEjecutarCodigo/`: Documentación oficial y bitácora de prompts.
