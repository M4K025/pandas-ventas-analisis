# 📊 Análisis de Ventas con Pandas

> Proyecto práctico de análisis de datos usando la biblioteca **pandas** de Python.  
> Universidad Distrital Francisco José de Caldas — Ingeniería  
> Andrés Felipe Casilimas Bazurto · 20251020068 · Febrero 2026

---

## 🗂️ Estructura del Proyecto

```
pandas-ventas-analisis/
├── data/
│   └── ventas_2024.csv          # Dataset generado automáticamente
├── src/
│   └── generar_datos.py         # Generador de datos sintéticos
├── outputs/                     # CSVs con resultados del análisis
│   ├── por_producto.csv
│   ├── pivot_ciudad_canal.csv
│   ├── ranking_vendedores.csv
│   ├── serie_mensual.csv
│   └── segmentacion_abc.csv
├── analisis_ventas.py           # 🔑 Script principal de análisis
├── requirements.txt
└── README.md
```

---

## 🧠 Conceptos de Pandas Aplicados

| Sección | Técnicas usadas |
|---|---|
| Carga de datos | `pd.read_csv()` con `dtype`, `parse_dates` |
| Limpieza | `fillna()`, `drop_duplicates()`, `isnull()` |
| Exploración | `describe()`, `info()`, `dtypes` |
| Agregaciones | `groupby().agg()` con múltiples funciones |
| Tablas dinámicas | `pivot_table()` con `margins=True` |
| Series temporales | `resample()`, `pct_change()`, `rolling()` |
| Selección | `loc[]`, `iloc[]`, filtros booleanos |
| Funciones | `apply()`, `transform()`, `lambda` |
| Optimización | Tipos `category`, `int32`, `float32` |

---

## ▶️ Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/M4K025/pandas-ventas-analisis.git
cd pandas-ventas-analisis
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el análisis
```bash
python analisis_ventas.py
```

El script **genera automáticamente** el dataset si no existe y exporta todos los resultados en `outputs/`.

---

## 📈 Resultados del Análisis

Con el dataset de **1,000 órdenes** (año 2024):

- 💰 **Ingresos netos totales**: ~$714,970  
- 🛒 **Ticket promedio**: ~$715  
- ⭐ **Satisfacción media**: 3.91 / 5  
- 🏆 **Producto estrella**: Laptop (64.8% de ingresos — Segmento A)  
- 🌐 **Canal dominante**: Online (58.3% de órdenes)

### Segmentación ABC de Productos

| Segmento | Producto | % Ingresos |
|---|---|---|
| **A** | Laptop | 64.8% |
| **B** | Monitor, Auriculares | 20.6% |
| **C** | SSD, Teclado, Webcam, USB Hub, Mouse | 14.6% |

---

## 📦 Dataset

El dataset contiene las columnas:

| Columna | Tipo | Descripción |
|---|---|---|
| `orden_id` | int | ID único de orden |
| `fecha` | datetime | Fecha de la venta |
| `producto` | category | Nombre del producto |
| `categoria` | category | Hardware / Periférico |
| `precio_unitario` | float | Precio por unidad ($) |
| `cantidad` | int | Unidades vendidas |
| `descuento_pct` | float | % de descuento aplicado |
| `total_bruto` | float | Subtotal antes de descuento |
| `total_neto` | float | Total pagado |
| `ciudad` | category | Ciudad de la venta |
| `vendedor` | category | Nombre del vendedor |
| `canal` | category | Online / Tienda Física / Teléfono |
| `satisfaccion` | float | Puntuación 1–5 |

---

## 🔗 Referencias

- [Documentación oficial pandas](https://pandas.pydata.org/docs/)  
- McKinney, W. (2022). *Python for Data Analysis*, 3rd Ed. O'Reilly.  
- [Informe técnico completo (PDF)](./Pandas.pdf) — Casilimas Bazurto, 2026
