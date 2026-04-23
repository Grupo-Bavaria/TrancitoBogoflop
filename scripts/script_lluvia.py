import requests
import pandas as pd
import time
from io import StringIO

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
URL            = "https://www.datos.gov.co/resource/m84s-22dd.csv"
LIMIT          = 25000      # páginas más pequeñas = menos cortes
MAX_REINTENTOS = 5          # reintentos por página
ESPERA_BASE    = 10         # segundos entre reintento (se duplica cada vez)
ANIOS = [2017, 2018, 2020, 2021, 2022]   # 2019 excluido por datos erróneos


def descargar_pagina(params, intento=1):
    """Descarga una página con reintentos exponenciales."""
    try:
        r = requests.get(URL, params=params, timeout=90)
        if r.status_code == 200:
            return r.text
        else:
            print(f"    ⚠ HTTP {r.status_code}: {r.text[:200]}")
            return None
    except Exception as e:
        if intento <= MAX_REINTENTOS:
            espera = ESPERA_BASE * (2 ** (intento - 1))
            print(f"    ⚠ Error (intento {intento}/{MAX_REINTENTOS}): {type(e).__name__}")
            print(f"    ⏳ Esperando {espera}s antes de reintentar...")
            time.sleep(espera)
            return descargar_pagina(params, intento + 1)
        else:
            print(f"    ✖ Falló tras {MAX_REINTENTOS} intentos. Se saltará esta página.")
            return None


# ─────────────────────────────────────────────
# PASO 1: Descargar año por año para evitar
#         cortes del servidor en descargas grandes
# ─────────────────────────────────────────────
todos_los_chunks = []

for anio in ANIOS:
    print(f"\n{'='*50}")
    print(f"  Descargando año {anio}...")
    print(f"{'='*50}")

    offset = 0
    chunks_anio = []

    while True:
        params = {
            "$where": (
                f"departamento='BOGOTA D.C.' "
                f"AND fechaobservacion >= '{anio}-01-01T00:00:00' "
                f"AND fechaobservacion <= '{anio}-12-31T23:59:59'"
            ),
            "$select": "fechaobservacion, valorobservado, codigoestacion",
            "$limit":  LIMIT,
            "$offset": offset,
            "$order":  "fechaobservacion"
        }

        print(f"  Offset {offset:,}...", end=" ", flush=True)
        texto = descargar_pagina(params)

        if texto is None:
            print("SALTADO")
            break

        chunk = pd.read_csv(StringIO(texto))

        if len(chunk) == 0:
            print("fin.")
            break

        chunks_anio.append(chunk)
        print(f"{len(chunk):,} filas")

        if len(chunk) < LIMIT:
            break

        offset += LIMIT
        time.sleep(1)   # pausa corta entre páginas para no saturar el servidor

    if chunks_anio:
        df_anio = pd.concat(chunks_anio, ignore_index=True)
        print(f"  ✅ Año {anio}: {len(df_anio):,} filas totales")
        todos_los_chunks.append(df_anio)
    else:
        print(f"  ✖ Año {anio}: sin datos")

if not todos_los_chunks:
    raise RuntimeError("No se descargaron datos. Verifica conexión.")

df = pd.concat(todos_los_chunks, ignore_index=True)
print(f"\n{'='*50}")
print(f"Total filas crudas: {len(df):,}")

# ─────────────────────────────────────────────
# PASO 2: Limpiar y convertir tipos
# ─────────────────────────────────────────────
df["fechaobservacion"] = pd.to_datetime(df["fechaobservacion"], errors="coerce")

df["valorobservado"] = (
    df["valorobservado"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)
df["valorobservado"] = pd.to_numeric(df["valorobservado"], errors="coerce")

antes = len(df)
df = df.dropna(subset=["fechaobservacion", "valorobservado"])
df = df[df["valorobservado"] >= 0]
print(f"Filas descartadas (nulos/negativos): {antes - len(df):,}")

df["fecha_dia"] = df["fechaobservacion"].dt.date
df["anio"]      = df["fechaobservacion"].dt.year
df["mes"]       = df["fechaobservacion"].dt.month

# ─────────────────────────────────────────────
# PASO 3: Agregar lecturas → días → meses
#
# Cada fila = mm caídos en ~10 minutos (pluviómetro basculante)
# Paso 3a: suma lecturas del día por estación → mm diarios por estación
# Paso 3b: promedio entre estaciones por día  → valor representativo de Bogotá
# Paso 3c: suma de días del mes              → precipitación mensual (mm)
# ─────────────────────────────────────────────
diario_por_estacion = (
    df.groupby(["codigoestacion", "fecha_dia", "anio", "mes"], as_index=False)
    ["valorobservado"].sum()
    .rename(columns={"valorobservado": "mm_dia"})
)

diario_bogota = (
    diario_por_estacion
    .groupby(["fecha_dia", "anio", "mes"], as_index=False)
    ["mm_dia"].mean()
    .rename(columns={"mm_dia": "mm_dia_promedio"})
)

mensual = (
    diario_bogota
    .groupby(["anio", "mes"], as_index=False)
    ["mm_dia_promedio"].sum()
    .rename(columns={"mm_dia_promedio": "precipitacion_mm"})
)

mensual["precipitacion_mm"] = mensual["precipitacion_mm"].round(1)
mensual = mensual.sort_values(["anio", "mes"]).reset_index(drop=True)

# ─────────────────────────────────────────────
# PASO 4: Guardar
# ─────────────────────────────────────────────
output = "lluvia_mensual_bogota.csv"
mensual.to_csv(output, index=False)

print(f"\n✅ Guardado: {output}")
print(f"   {len(mensual)} meses procesados\n")
print(mensual.to_string(index=False))