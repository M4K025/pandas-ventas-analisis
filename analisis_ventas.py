"""
analisis_ventas.py
Análisis completo de ventas usando pandas.
Cubre: lectura, limpieza, exploración, agregaciones, series temporales y exportación.
"""

import pandas as pd
import numpy as np
import os
import sys

# ── Asegurar que src/ esté en el path ──────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from generar_datos import generar_dataset_ventas

OUTPUTS = "outputs"
os.makedirs(OUTPUTS, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# 1. CARGA Y VISTA GENERAL
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  1. CARGA Y VISTA GENERAL")
print("═"*60)

# Generar o leer datos
csv_path = "data/ventas_2024.csv"
if not os.path.exists(csv_path):
    os.makedirs("data", exist_ok=True)
    df_raw = generar_dataset_ventas(1000)
    df_raw.to_csv(csv_path, index=False)

df = pd.read_csv(
    csv_path,
    parse_dates=["fecha"],
    dtype={
        "orden_id":        "int32",
        "ciudad":          "category",
        "producto":        "category",
        "categoria":       "category",
        "canal":           "category",
        "vendedor":        "category",
    },
)

print(f"\nForma del DataFrame : {df.shape[0]:,} filas × {df.shape[1]} columnas")
print(f"Memoria             : {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
print("\nPrimeras filas:")
print(df.head(3).to_string())
print("\nTipos de datos:")
print(df.dtypes)

# ══════════════════════════════════════════════════════════════════════════════
# 2. LIMPIEZA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  2. LIMPIEZA DE DATOS")
print("═"*60)

print("\nValores faltantes antes:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# Rellenar descuento faltante con 0 (sin descuento)
df["descuento_pct"] = df["descuento_pct"].fillna(0)

# Rellenar satisfacción con la mediana
mediana_sat = df["satisfaccion"].median()
df["satisfaccion"] = df["satisfaccion"].fillna(mediana_sat)

# Recalcular total_neto donde descuento era NaN
df["total_neto"] = (df["total_bruto"] * (1 - df["descuento_pct"] / 100)).round(2)

# Eliminar duplicados (por si existen)
n_antes = len(df)
df = df.drop_duplicates(subset=["orden_id"])
print(f"\nDuplicados eliminados : {n_antes - len(df)}")
print("\nValores faltantes después:")
print(df.isnull().sum()[df.isnull().sum() > 0] if df.isnull().sum().any() else "  ✅ Sin valores faltantes")

# ══════════════════════════════════════════════════════════════════════════════
# 3. ESTADÍSTICAS DESCRIPTIVAS
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  3. ESTADÍSTICAS DESCRIPTIVAS")
print("═"*60)

columnas_num = ["precio_unitario", "cantidad", "descuento_pct", "total_bruto", "total_neto", "satisfaccion"]
print(df[columnas_num].describe().round(2).to_string())

# ══════════════════════════════════════════════════════════════════════════════
# 4. ANÁLISIS POR PRODUCTO
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  4. ANÁLISIS POR PRODUCTO")
print("═"*60)

por_producto = (
    df.groupby("producto", observed=True)
    .agg(
        unidades_vendidas=("cantidad", "sum"),
        ordenes=("orden_id", "count"),
        ingresos_netos=("total_neto", "sum"),
        ticket_promedio=("total_neto", "mean"),
        satisfaccion_media=("satisfaccion", "mean"),
    )
    .round(2)
    .sort_values("ingresos_netos", ascending=False)
)

print(por_producto.to_string())

# Guardar
por_producto.to_csv(f"{OUTPUTS}/por_producto.csv")

# ══════════════════════════════════════════════════════════════════════════════
# 5. ANÁLISIS POR CIUDAD Y CANAL
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  5. ANÁLISIS POR CIUDAD Y CANAL")
print("═"*60)

por_ciudad = (
    df.groupby("ciudad", observed=True)["total_neto"]
    .agg(["sum", "mean", "count"])
    .rename(columns={"sum": "ingresos", "mean": "ticket_promedio", "count": "ordenes"})
    .round(2)
    .sort_values("ingresos", ascending=False)
)
print("\nVentas por ciudad:")
print(por_ciudad.to_string())

pivot_ciudad_canal = df.pivot_table(
    values="total_neto",
    index="ciudad",
    columns="canal",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="TOTAL",
    observed=True,
).round(0)

print("\nPivot: Ciudad × Canal (ingresos netos $):")
print(pivot_ciudad_canal.to_string())
pivot_ciudad_canal.to_csv(f"{OUTPUTS}/pivot_ciudad_canal.csv")

# ══════════════════════════════════════════════════════════════════════════════
# 6. ANÁLISIS DE VENDEDORES
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  6. RANKING DE VENDEDORES")
print("═"*60)

por_vendedor = (
    df.groupby("vendedor", observed=True)
    .agg(
        ordenes=("orden_id", "count"),
        ingresos=("total_neto", "sum"),
        satisfaccion_prom=("satisfaccion", "mean"),
        descuento_prom=("descuento_pct", "mean"),
    )
    .round(2)
    .sort_values("ingresos", ascending=False)
)

# Rank de ingresos
por_vendedor["rank"] = por_vendedor["ingresos"].rank(ascending=False).astype(int)
print(por_vendedor.to_string())
por_vendedor.to_csv(f"{OUTPUTS}/ranking_vendedores.csv")

# ══════════════════════════════════════════════════════════════════════════════
# 7. SERIES TEMPORALES
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  7. SERIES TEMPORALES")
print("═"*60)

df_ts = df.set_index("fecha").sort_index()

# Resample mensual
mensual = df_ts["total_neto"].resample("ME").agg(["sum", "count", "mean"]).round(2)
mensual.columns = ["ingresos", "ordenes", "ticket_prom"]
mensual.index = mensual.index.strftime("%Y-%m")

print("\nIngresos mensuales:")
print(mensual.to_string())

# Crecimiento mes a mes
mensual["crecimiento_%"] = mensual["ingresos"].pct_change().mul(100).round(1)
print("\nCrecimiento mensual (%):")
print(mensual[["ingresos", "crecimiento_%"]].to_string())

# Promedio móvil 3 meses
mensual["MA_3m"] = mensual["ingresos"].rolling(3).mean().round(2)
mensual.to_csv(f"{OUTPUTS}/serie_mensual.csv")

# ══════════════════════════════════════════════════════════════════════════════
# 8. ANÁLISIS DE COHORTES (mes de primera compra)
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  8. ANÁLISIS DE COHORTES")
print("═"*60)

# Usar orden_id como proxy de cliente (simplificado: ciudad+vendedor como "cliente")
df["cliente_id"] = df["ciudad"].astype(str) + "_" + df["vendedor"].astype(str)
df["mes_compra"] = df["fecha"].dt.to_period("M")
df["mes_primera"] = df.groupby("cliente_id")["fecha"].transform("min").dt.to_period("M")

cohortes = df.pivot_table(
    values="total_neto",
    index="mes_primera",
    columns="mes_compra",
    aggfunc="sum",
    fill_value=0,
    observed=True,
).round(0)

print("Tabla de cohortes (ingresos por mes de primera compra):")
print(cohortes.iloc[:4, :4].to_string())  # Muestra las primeras 4×4

# ══════════════════════════════════════════════════════════════════════════════
# 9. SEGMENTACIÓN: ABC de productos
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  9. SEGMENTACIÓN ABC DE PRODUCTOS")
print("═"*60)

total_ventas = df["total_neto"].sum()
abc = (
    df.groupby("producto", observed=True)["total_neto"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
abc["participacion_%"] = (abc["total_neto"] / total_ventas * 100).round(2)
abc["acumulado_%"]     = abc["participacion_%"].cumsum().round(2)

def segmento_abc(acum):
    if acum <= 70:  return "A"
    elif acum <= 90: return "B"
    else:            return "C"

abc["segmento"] = abc["acumulado_%"].apply(segmento_abc)
print(abc.to_string(index=False))
abc.to_csv(f"{OUTPUTS}/segmentacion_abc.csv", index=False)

# ══════════════════════════════════════════════════════════════════════════════
# 10. REPORTE FINAL
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  10. RESUMEN EJECUTIVO")
print("═"*60)

mejor_mes    = mensual["ingresos"].idxmax()
peor_mes     = mensual["ingresos"].idxmin()
top_producto = por_producto["ingresos_netos"].idxmax()
top_ciudad   = por_ciudad["ingresos"].idxmax()
top_vendedor = por_vendedor["ingresos"].idxmax()

print(f"""
  📊 Total de órdenes      : {len(df):,}
  💰 Ingresos netos totales: ${df['total_neto'].sum():,.0f}
  🛒 Ticket promedio        : ${df['total_neto'].mean():,.2f}
  ⭐ Satisfacción media     : {df['satisfaccion'].mean():.2f} / 5

  📅 Mejor mes             : {mejor_mes}  (${mensual.loc[mejor_mes,'ingresos']:,.0f})
  📅 Peor mes              : {peor_mes}   (${mensual.loc[peor_mes,'ingresos']:,.0f})

  🏆 Producto top          : {top_producto}
  🏙️  Ciudad top            : {top_ciudad}
  👤 Vendedor top          : {top_vendedor}

  🌐 Canal más usado       : {df['canal'].value_counts().idxmax()}
     ({df['canal'].value_counts(normalize=True).max()*100:.1f}% de órdenes)
""")

print(f"✅ Archivos exportados en /{OUTPUTS}/")
print("   - por_producto.csv")
print("   - pivot_ciudad_canal.csv")
print("   - ranking_vendedores.csv")
print("   - serie_mensual.csv")
print("   - segmentacion_abc.csv")
