#!/usr/bin/env python3
"""Módulo B — Estadística oficial: contexto social y delitos de odio.

Análisis descriptivo independiente del CIS. Consume extractos oficiales ya
armonizados en CSV; nunca combina estas estadísticas agregadas con encuestas.

Formato de entrada (CSV UTF-8):
  data/modulo_b/epa.csv: periodo, grupo, tasa_actividad, tasa_paro, activos_variacion
      grupo: Espanola / Extranjera (o etiquetas equivalentes)
  data/modulo_b/afiliacion.csv: periodo, afiliados_extranjeros, afiliados_total
  data/modulo_b/delitos_odio.csv: anio, provincia, tipologia, hechos
  data/modulo_b/poblacion.csv: anio, provincia, poblacion

Los ficheros no se descargan automáticamente: transcribe/descarga las tablas
primarias citadas y registra URL, fecha de consulta y filtros en su ficha CSV.
El script valida columnas, guarda tablas derivadas y genera PNG si hay datos.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "modulo_b"
DEFAULT_OUT = ROOT / "outputs" / "modulo_b"
SOURCES = {
    "EPA / INE": "https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176918&menu=ultiDatos&idp=1254735976595",
    "Afiliación / Seguridad Social": "https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas",
    "Delitos de odio / Interior": "https://www.interior.gob.es/opencms/es/servicios-al-ciudadano/estadisticas/",
    "Población / INE": "https://www.ine.es/dyngs/INEbase/es/categoria.htm?c=Estadistica_P&cid=1254734710984",
}
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def read_table(path: Path, required: set[str]) -> pd.DataFrame | None:
    if not path.exists():
        logging.warning("No se encontró %s; se omite este bloque.", path)
        return None
    df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path.name}: faltan columnas requeridas {sorted(missing)}")
    return df


def numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    return df


def epa_analysis(data_dir: Path, out_dir: Path) -> None:
    df = read_table(data_dir / "epa.csv", {"periodo", "grupo", "tasa_actividad", "tasa_paro", "activos_variacion"})
    if df is None: return
    df = numeric(df, ["tasa_actividad", "tasa_paro", "activos_variacion"])
    df.to_csv(out_dir / "epa_limpia.csv", index=False)
    for metric, label in [("tasa_actividad", "Tasa de actividad (%)"), ("tasa_paro", "Tasa de paro (%)")]:
        pivot = df.pivot_table(index="periodo", columns="grupo", values=metric, aggfunc="mean").sort_index()
        ax = pivot.plot(marker="o", figsize=(9, 5), color=["#37688d", "#df632b"][:len(pivot.columns)])
        ax.set(title=f"EPA: {label.lower()} por nacionalidad", xlabel="Periodo", ylabel=label)
        ax.grid(axis="y", alpha=.25); ax.legend(title="Grupo", frameon=False)
        plt.tight_layout(); plt.savefig(out_dir / f"epa_{metric}.png", dpi=180); plt.close()


def affiliation_analysis(data_dir: Path, out_dir: Path) -> None:
    df = read_table(data_dir / "afiliacion.csv", {"periodo", "afiliados_extranjeros", "afiliados_total"})
    if df is None: return
    df = numeric(df, ["afiliados_extranjeros", "afiliados_total"])
    df["porcentaje_extranjero"] = 100 * df["afiliados_extranjeros"] / df["afiliados_total"].where(df["afiliados_total"] > 0)
    df = df.sort_values("periodo")
    df.to_csv(out_dir / "afiliacion_resumen.csv", index=False)
    ax = df.plot(x="periodo", y="afiliados_extranjeros", marker="o", legend=False, figsize=(9, 5), color="#df632b")
    ax.set(title="Afiliación extranjera a la Seguridad Social", xlabel="Periodo", ylabel="Personas afiliadas")
    ax.grid(axis="y", alpha=.25); plt.tight_layout(); plt.savefig(out_dir / "afiliacion_extranjera.png", dpi=180); plt.close()


def hate_crimes_analysis(data_dir: Path, out_dir: Path) -> None:
    crimes = read_table(data_dir / "delitos_odio.csv", {"anio", "provincia", "tipologia", "hechos"})
    if crimes is None: return
    crimes = numeric(crimes, ["anio", "hechos"])
    crimes = crimes.dropna(subset=["anio", "hechos"])
    annual = crimes.groupby(["anio", "tipologia"], as_index=False)["hechos"].sum()
    annual.to_csv(out_dir / "delitos_odio_serie.csv", index=False)
    ax = annual.pivot(index="anio", columns="tipologia", values="hechos").sort_index().plot(figsize=(9, 5), marker="o")
    ax.set(title="Hechos registrados como delitos de odio", xlabel="Año", ylabel="Hechos registrados")
    ax.grid(axis="y", alpha=.25); plt.tight_layout(); plt.savefig(out_dir / "delitos_odio_serie.png", dpi=180); plt.close()

    pop = read_table(data_dir / "poblacion.csv", {"anio", "provincia", "poblacion"})
    if pop is None: return
    pop = numeric(pop, ["anio", "poblacion"])
    totals = crimes.groupby(["anio", "provincia"], as_index=False)["hechos"].sum()
    rates = totals.merge(pop, on=["anio", "provincia"], how="left", validate="many_to_one")
    rates["tasa_por_100k"] = 100_000 * rates["hechos"] / rates["poblacion"].where(rates["poblacion"] > 0)
    rates.to_csv(out_dir / "delitos_odio_tasas_provincia.csv", index=False)


def write_sources(out_dir: Path) -> None:
    lines = ["# Fuentes y cautelas — Módulo B", "", "Estadísticas oficiales descriptivas; bloque independiente del CIS.", ""]
    lines += [f"- **{name}:** {url}" for name, url in SOURCES.items()]
    lines += ["", "Registrar en los CSV periodo exacto, tabla, población/unidad, filtros y fecha de extracción.",
              "Las denuncias/hechos registrados no equivalen a incidencia real: hay infradenuncia y cambios de registro.",
              "Actividad no equivale a empleo; nacionalidad no equivale a país de nacimiento.",
              "Las tasas provinciales usan hechos registrados por 100.000 residentes; no permiten inferencias causales."]
    (out_dir / "fuentes_modulo_b.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    epa_analysis(args.data_dir, args.out_dir)
    affiliation_analysis(args.data_dir, args.out_dir)
    hate_crimes_analysis(args.data_dir, args.out_dir)
    write_sources(args.out_dir)
    logging.info("Módulo terminado. Salidas: %s", args.out_dir)
    logging.info("Los bloques sin CSV de entrada se omitieron; no se inventaron cifras.")


if __name__ == "__main__":
    main()
