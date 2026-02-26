"""
generar_datos.py
Genera un dataset sintético de ventas para demostrar el uso de pandas.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generar_dataset_ventas(n_registros: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Genera un DataFrame de ventas sintético con datos realistas.

    Args:
        n_registros: Número de registros a generar
        seed: Semilla aleatoria para reproducibilidad

    Returns:
        DataFrame con datos de ventas
    """
    np.random.seed(seed)

    # Parámetros
    productos = {
        "Laptop":      (1200, 300),
        "Mouse":       (25,   8),
        "Teclado":     (75,   20),
        "Monitor":     (350,  80),
        "Auriculares": (90,   30),
        "Webcam":      (60,   15),
        "USB Hub":     (30,   10),
        "SSD 1TB":     (110,  25),
    }
    ciudades     = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena"]
    vendedores   = ["Andrés C.", "María L.", "Carlos R.", "Sofía M.", "David P."]
    canales      = ["Online", "Tienda Física", "Teléfono"]

    # Fechas (último año)
    fecha_inicio = datetime(2024, 1, 1)
    fechas = [
        fecha_inicio + timedelta(days=int(x))
        for x in np.random.randint(0, 365, n_registros)
    ]

    # Construir registros
    nombres_prod = list(productos.keys())
    precios_base = np.array([productos[p][0] for p in nombres_prod])
    desviaciones  = np.array([productos[p][1] for p in nombres_prod])

    prod_idx   = np.random.randint(0, len(nombres_prod), n_registros)
    productos_sel = [nombres_prod[i] for i in prod_idx]
    precios    = np.abs(
        precios_base[prod_idx] + np.random.normal(0, desviaciones[prod_idx])
    ).round(2)
    cantidades = np.random.randint(1, 6, n_registros)
    descuentos = np.random.choice([0, 5, 10, 15, 20], n_registros, p=[0.5, 0.2, 0.15, 0.1, 0.05])

    total_bruto = (precios * cantidades).round(2)
    total_neto  = (total_bruto * (1 - descuentos / 100)).round(2)

    # Introducir valores faltantes (~3 %)
    idx_nan = np.random.choice(n_registros, size=int(n_registros * 0.03), replace=False)

    df = pd.DataFrame({
        "orden_id":   range(1000, 1000 + n_registros),
        "fecha":      fechas,
        "producto":   productos_sel,
        "categoria":  ["Periférico" if p not in ("Laptop", "Monitor", "SSD 1TB")
                        else "Hardware" for p in productos_sel],
        "precio_unitario": precios,
        "cantidad":   cantidades,
        "descuento_pct": descuentos,
        "total_bruto": total_bruto,
        "total_neto":  total_neto,
        "ciudad":      np.random.choice(ciudades, n_registros),
        "vendedor":    np.random.choice(vendedores, n_registros),
        "canal":       np.random.choice(canales, n_registros, p=[0.55, 0.35, 0.10]),
        "satisfaccion": np.random.choice([1, 2, 3, 4, 5], n_registros,
                                          p=[0.03, 0.07, 0.15, 0.40, 0.35]),
    })

    # Inyectar NaN
    df.loc[idx_nan[:len(idx_nan)//2], "satisfaccion"] = np.nan
    df.loc[idx_nan[len(idx_nan)//2:], "descuento_pct"] = np.nan

    return df.sort_values("fecha").reset_index(drop=True)


if __name__ == "__main__":
    df = generar_dataset_ventas(1000)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/ventas_2024.csv", index=False)
    print(f"✅ Dataset generado: {len(df)} registros")
    print(f"   Columnas : {list(df.columns)}")
    print(f"   Rango    : {df['fecha'].min().date()} → {df['fecha'].max().date()}")
    print(df.head(3).to_string())
