"""Genera un conjunto de datos SINTÉTICO de eventos de alarma para los laboratorios.

Los datos son inventados: no proceden de ningún sistema real ni de ningún cliente.
Uso:  python generar_datos.py [--filas 5000] [--salida data/eventos_alarma.csv]
"""
import argparse
import os

import numpy as np
import pandas as pd

PROVINCIAS = {
    "Madrid": 0.24, "Barcelona": 0.20, "Valencia": 0.11, "Sevilla": 0.08, "Málaga": 0.07,
    "Bizkaia": 0.06, "Alicante": 0.06, "Zaragoza": 0.05, "Murcia": 0.05, "A Coruña": 0.04,
    "Asturias": 0.04,
}
TIPOS = {"intrusion": 0.38, "apertura_puerta": 0.22, "boton_panico": 0.07,
         "incendio_humo": 0.08, "sabotaje": 0.05, "bateria_baja": 0.12, "perdida_conexion": 0.08}
DISPOSITIVOS = {"detector_movimiento": 0.40, "contacto_magnetico": 0.25, "camara": 0.15,
                "detector_humo": 0.08, "panel": 0.12}
# Probabilidad base de falsa alarma por tipo de evento
P_FALSA = {"intrusion": 0.55, "apertura_puerta": 0.62, "boton_panico": 0.30, "incendio_humo": 0.40,
           "sabotaje": 0.25, "bateria_baja": 0.80, "perdida_conexion": 0.70}
# Tiempo medio de respuesta (segundos) por tipo
T_MEDIO = {"intrusion": 45, "apertura_puerta": 60, "boton_panico": 25, "incendio_humo": 30,
           "sabotaje": 40, "bateria_baja": 300, "perdida_conexion": 240}


def generar(filas: int = 5000, semilla: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    inicio = pd.Timestamp("2026-01-01")
    segundos = rng.integers(0, 334 * 24 * 3600, filas)  # 1 de enero a 30 de noviembre
    fechas = inicio + pd.to_timedelta(segundos, unit="s")
    provincia = rng.choice(list(PROVINCIAS), filas, p=list(PROVINCIAS.values()))
    tipo = rng.choice(list(TIPOS), filas, p=list(TIPOS.values()))
    dispositivo = rng.choice(list(DISPOSITIVOS), filas, p=list(DISPOSITIVOS.values()))
    hora = pd.DatetimeIndex(fechas).hour
    noche = (hora < 7) | (hora >= 22)
    p = np.array([P_FALSA[t] for t in tipo]) - 0.10 * noche + 0.08 * (dispositivo == "detector_movimiento")
    falsa = rng.random(filas) < np.clip(p, 0.05, 0.95)
    t = np.array([T_MEDIO[x] for x in tipo]) * rng.lognormal(0, 0.35, filas)
    t = np.where(falsa, t * 1.15, t).round().astype(int)
    df = pd.DataFrame({
        "id_evento": [f"EV{n:07d}" for n in range(1, filas + 1)],
        "fecha_hora": pd.DatetimeIndex(fechas).strftime("%Y-%m-%d %H:%M:%S"),
        "provincia": provincia,
        "tipo_evento": tipo,
        "dispositivo": dispositivo,
        "tiempo_resp_s": t,
        "falsa_alarma": falsa,
    })
    return df.sort_values("fecha_hora").reset_index(drop=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--filas", type=int, default=5000)
    ap.add_argument("--salida", default="data/eventos_alarma.csv")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.salida) or ".", exist_ok=True)
    df = generar(a.filas)
    salida = df.assign(falsa_alarma=df["falsa_alarma"].map({True: "true", False: "false"}))
    salida.to_csv(a.salida, index=False)
    print(f"Generado {a.salida} con {len(df)} filas")
