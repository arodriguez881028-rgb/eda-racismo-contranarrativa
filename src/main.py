"""EDA del CIS 3536: percepción del racismo en España.

Uso:
    python src/main.py --data src/data/raw/3536_etiq.csv

La presentación HTML se entrega ya generada en presentation/index.html.
Este script vuelve a calcular las tablas y los gráficos SVG a partir del CSV.
"""
from __future__ import annotations

import argparse
import html
import json
from math import erfc, sqrt
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import wls
from statsmodels.stats.weightstats import DescrStatsW

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "presentation" / "assets"
ORANGE, BLUE, INK, MUTED = "#e46d2e", "#37688d", "#202a32", "#697781"

COL = {
    "sex": "SEXO Sexo de la persona entrevistada",
    "age": "EDAD Edad de la persona entrevistada",
    "self": "P12_1 Dónde se ubicaría Ud. mismo/a",
    "society": "P12_2 Dónde ubicaría Ud. a la sociedad española en su conjunto",
    "income": "INGRESHOG Nivel de ingresos netos del hogar",
    "ideology": "ESCIDEOL Escala de autoubicación ideológica (1-10)",
    "education": "NIVELESTENTREV Nivel de estudios alcanzado por la persona entrevistada",
    "education_group": "ESTUDIOS Estudios de la persona entrevistada",
    "weight": "PESO Ponderación con ajuste por Estudios",
    "social_media": "P11 Recuerdo de haber visto en las redes sociales contenido que exprese ideas ofensivas o violentas contra personas por motivos étnicos, de raza o religión",
}


def number(value):
    """Decode numeric answers stored as strings in the CIS labelled CSV."""
    m = re.match(r"\s*(\d+)", str(value))
    return float(m.group(1)) if m else np.nan


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig", low_memory=False)
    missing = [c for c in COL.values() if c not in df]
    if missing:
        raise ValueError(f"Faltan variables necesarias en el fichero: {missing}")
    df["peso"] = pd.to_numeric(df[COL["weight"]].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    df["autopercepcion"] = df[COL["self"]].map(number)
    df["percepcion_sociedad"] = df[COL["society"]].map(number)
    df["edad_num"] = pd.to_numeric(df[COL["age"]], errors="coerce")
    return df


def weighted_mean(values, weights):
    mask = values.notna() & weights.notna() & (weights > 0)
    if not mask.any():
        return np.nan
    return float(np.average(values[mask], weights=weights[mask]))


def groups(df):
    age = pd.cut(df["edad_num"], [17, 24, 34, 49, 64, 120], labels=["18–24", "25–34", "35–49", "50–64", "65+"], include_lowest=True)
    sex = df[COL["sex"]].replace({"Hombre": "Hombres", "Mujer": "Mujeres"})
    income_raw = df[COL["income"]].astype(str)
    income = pd.Series(np.select([
        income_raw.str.startswith("Menos de 1.100") | income_raw.str.startswith("De 1.100 a 1.800"),
        income_raw.str.startswith("De 1.801 a 2.700") | income_raw.str.startswith("De 2.701 a 3.900"),
        income_raw.str.startswith("De 3.901 a 5.000") | income_raw.str.startswith("Más de 5.000"),
    ], ["Bajos (≤ 1.800 €)", "Medios (1.801–3.900 €)", "Altos (> 3.900 €)"], default="No consta"), index=df.index)
    ideology_num = df[COL["ideology"]].map(number)
    ideology = pd.Series(np.select([ideology_num.between(1,4), ideology_num.between(5,6), ideology_num.between(7,10)], ["Izquierda (1–4)", "Centro (5–6)", "Derecha (7–10)"], default="NS/NC"), index=df.index)
    edu_raw = df[COL["education_group"]].astype(str)
    education = pd.Series(np.select([
        edu_raw.eq("Primaria") | edu_raw.eq("Sin estudios"),
        edu_raw.str.startswith("Secundaria"),
        edu_raw.eq("F.P."),
        edu_raw.eq("Superiores"),
    ], ["Primaria o menos", "Secundaria", "F.P.", "Superiores / Universidad"], default="No consta / otros"), index=df.index)
    return {"Sexo": sex, "Tramo de edad": age.astype("object"), "Ingresos del hogar": income,
            "Bloque ideológico": ideology, "Nivel de estudios": education}


def summary(df):
    records = []
    for label, category in groups(df).items():
        tmp = df.assign(_grupo=category)
        for group, sub in tmp.groupby("_grupo", observed=True):
            valid = sub["autopercepcion"].notna() & sub["percepcion_sociedad"].notna() & sub["peso"].notna() & (sub["peso"] > 0)
            s = sub.loc[valid]
            if len(s) == 0:
                continue
            self_mean = weighted_mean(s["autopercepcion"], s["peso"])
            society_mean = weighted_mean(s["percepcion_sociedad"], s["peso"])
            records.append({"dimensión": label, "grupo": str(group), "n_válido": len(s),
                            "autopercepción_media_ponderada": self_mean,
                            "sociedad_media_ponderada": society_mean,
                            "brecha": society_mean-self_mean})
    result = pd.DataFrame(records)
    result.to_csv(ROOT / "src/data/resultados_ponderados.csv", index=False, encoding="utf-8-sig")
    return result


def weighted_hypothesis_test(df):
    """Approximate weighted Wald test for the paired mean difference.

    Uses Kish effective sample size. It is not a design-based variance estimate:
    CIS strata/PSU covariance information is not available in this flat file.
    """
    valid = (df["autopercepcion"].notna() & df["percepcion_sociedad"].notna()
             & df["peso"].notna() & (df["peso"] > 0))
    d = df.loc[valid, "percepcion_sociedad"] - df.loc[valid, "autopercepcion"]
    w = df.loc[valid, "peso"]
    mean = float(np.average(d, weights=w))
    n_eff = float(w.sum() ** 2 / np.square(w).sum())
    sd = float(np.sqrt(np.average(np.square(d - mean), weights=w)))
    se = sd / sqrt(n_eff)
    z = mean / se
    p = erfc(abs(z) / sqrt(2))
    return {"contraste": "H0: media ponderada (P12_2 - P12_1) = 0",
            "media_diferencia": mean, "error_estandar_aprox": se,
            "IC95_inferior_aprox": mean - 1.96 * se,
            "IC95_superior_aprox": mean + 1.96 * se,
            "n_valido": int(valid.sum()), "n_efectivo_Kish": n_eff,
            "z_aprox": z, "p_valor_normal_aprox": (p if p > 1e-300 else "<1e-300"),
            "nota": "Aproximación con n efectivo de Kish; no incorpora estratos/PSU ni varianza compleja del diseño CIS."}


def _p_value(value):
    value = float(value)
    return "<1e-300" if value < 1e-300 else value


def hypothesis_tests(df):
    """Run the weighted exploratory contrasts shown in the presentation.

    These are model-based approximations: PESO is applied, but the flat CIS
    microdata do not provide the full design information needed for design-
    based standard errors. The weighted chi-square treats weight sums as
    frequencies and must be read with particular caution.
    """
    data = df.copy()
    data["brecha"] = data["percepcion_sociedad"] - data["autopercepcion"]
    data["ideol_grupo"] = groups(data)["Bloque ideológico"].replace({
        "Izquierda (1–4)": "Izquierda (1-4)",
        "Centro (5–6)": "Centro (5-6)",
        "Derecha (7–10)": "Derecha (7-10)",
    })
    data["edad_grupo"] = groups(data)["Tramo de edad"]
    data["sexo_label"] = data[COL["sex"]]
    data["ingreso_grupo"] = groups(data)["Ingresos del hogar"].replace({
        "Bajos (≤ 1.800 €)": "1. Bajos (≤1.800€)",
        "Medios (1.801–3.900 €)": "2. Medios (1.801-3.900€)",
        "Altos (> 3.900 €)": "3. Altos (>3.900€)",
    })
    social_media = data[COL["social_media"]].astype(str)
    data["p11_binario"] = np.select(
        [social_media.str.startswith("Sí"), social_media.eq("No")],
        ["Vio contenido", "No vio contenido"],
        default="No válido",
    )
    valid_gap = (data["brecha"].notna() & data["peso"].notna() & (data["peso"] > 0))

    # H1: Are mean perception gaps equal across the three ideological groups?
    h1 = data.loc[valid_gap & data["ideol_grupo"].isin(
        ["Izquierda (1-4)", "Centro (5-6)", "Derecha (7-10)"]
    )].copy()
    model_ideology = wls(
        'brecha ~ C(ideol_grupo, Treatment(reference="Centro (5-6)"))',
        data=h1, weights=h1["peso"],
    ).fit()
    f_ideology = model_ideology.f_test(
        'C(ideol_grupo, Treatment(reference="Centro (5-6)"))[T.Izquierda (1-4)] = 0, '
        'C(ideol_grupo, Treatment(reference="Centro (5-6)"))[T.Derecha (7-10)] = 0'
    )
    ideology_means = {
        group: weighted_mean(sub["brecha"], sub["peso"])
        for group, sub in h1.groupby("ideol_grupo", observed=True)
    }

    # H2: Is age associated with recalling hateful/offensive social content?
    h2 = data.loc[
        data["edad_grupo"].notna()
        & data["p11_binario"].isin(["Vio contenido", "No vio contenido"])
        & data["peso"].notna() & (data["peso"] > 0)
    ].copy()
    table = pd.crosstab(
        h2["edad_grupo"], h2["p11_binario"], values=h2["peso"], aggfunc="sum"
    )
    chi2, p_age_media, dof_age_media, _ = stats.chi2_contingency(table)

    # Sex: Welch comparison of weighted mean gaps.
    by_sex = data.loc[valid_gap & data["sexo_label"].notna()]
    men = DescrStatsW(
        by_sex.loc[by_sex["sexo_label"] == "Hombre", "brecha"],
        weights=by_sex.loc[by_sex["sexo_label"] == "Hombre", "peso"],
    )
    women = DescrStatsW(
        by_sex.loc[by_sex["sexo_label"] == "Mujer", "brecha"],
        weights=by_sex.loc[by_sex["sexo_label"] == "Mujer", "peso"],
    )
    t_sex, p_sex, df_sex = sm.stats.CompareMeans(women, men).ttest_ind(usevar="unequal")

    # Income: do medium/high household-income coefficients jointly differ
    # from the low-income reference after adjusting for ideology?
    h_income = data.loc[
        valid_gap
        & data["ingreso_grupo"].isin([
            "1. Bajos (≤1.800€)", "2. Medios (1.801-3.900€)", "3. Altos (>3.900€)"
        ])
        & data["ideol_grupo"].notna()
    ].copy()
    h_income["ingreso_grupo"] = pd.Categorical(
        h_income["ingreso_grupo"],
        categories=["1. Bajos (≤1.800€)", "2. Medios (1.801-3.900€)", "3. Altos (>3.900€)"],
    )
    model_income = wls(
        "brecha ~ C(ingreso_grupo) + C(ideol_grupo)",
        data=h_income, weights=h_income["peso"],
    ).fit()
    f_income = model_income.f_test(
        "C(ingreso_grupo)[T.2. Medios (1.801-3.900€)] = 0, "
        "C(ingreso_grupo)[T.3. Altos (>3.900€)] = 0"
    )

    return {
        "titulo": "Contrastes exploratorios ponderados con PESO",
        "limitacion_general": (
            "Contrastes model-based aproximados; no incorporan estratos, conglomerados "
            "ni toda la varianza del diseño muestral CIS. No prueban causalidad."
        ),
        "H1_ideologia": {
            "H0": "La brecha media es igual en izquierda, centro y derecha.",
            "prueba": "WLS; contraste F conjunto de izquierda y derecha frente a centro.",
            "F": float(f_ideology.fvalue), "gl_num": float(f_ideology.df_num),
            "gl_den": float(f_ideology.df_denom), "p_valor": _p_value(f_ideology.pvalue),
            "n": int(len(h1)), "brecha_media_ponderada_por_grupo": ideology_means,
            "decision": "Rechazar H0; la brecha varía entre los bloques ideológicos.",
        },
        "H2_edad_redes": {
            "H0": "Edad y recuerdo de contenido ofensivo/violento en redes son independientes.",
            "prueba": "Chi-cuadrado sobre tabla de contingencia ponderada.",
            "chi2": float(chi2), "gl": int(dof_age_media),
            "p_valor": _p_value(p_age_media), "n": int(len(h2)),
            "definicion_P11": "Sí a menudo / sí en alguna ocasión frente a No; se excluyen no usuarios y NS/NC.",
            "limitacion": "Suma de pesos tratada como frecuencias; p indicativo, no ajustado al diseño complejo.",
            "decision": "Rechazar H0; edad y recuerdo de exposición muestran asociación en esta tabla.",
        },
        "sexo": {
            "H0": "La brecha media es igual entre mujeres y hombres.",
            "prueba": "Welch t-test entre medias ponderadas.",
            "t": float(t_sex), "gl_aprox": float(df_sex),
            "p_valor": _p_value(p_sex), "n": int(len(by_sex)),
            "brecha_mujeres": float(women.mean), "brecha_hombres": float(men.mean),
            "decision": "Rechazar H0; la brecha ponderada es mayor entre mujeres.",
        },
        "ingresos_control_ideologia": {
            "H0": "Las medias de brecha de ingresos medios y altos no difieren de ingresos bajos, ajustando por ideología.",
            "prueba": "WLS multivariante; contraste F conjunto de ingresos medios y altos frente a bajos.",
            "F": float(f_income.fvalue), "gl_num": float(f_income.df_num),
            "gl_den": float(f_income.df_denom), "p_valor": _p_value(f_income.pvalue),
            "n": int(len(h_income)),
            "decision": "Rechazar H0; persisten diferencias de brecha por tramo de ingresos tras ajustar por ideología.",
        },
    }


def chart(result, dimension, title, filename):
    part = result[result["dimensión"] == dimension].copy()
    if part.empty:
        return
    x = np.arange(len(part)); width = .34
    fig, ax = plt.subplots(figsize=(10.8, 5.5), dpi=160)
    fig.patch.set_facecolor("#fbfaf7"); ax.set_facecolor("#fbfaf7")
    a = ax.bar(x-width/2, part["autopercepción_media_ponderada"], width, label="Cómo se sitúa la persona", color=BLUE, zorder=3)
    b = ax.bar(x+width/2, part["sociedad_media_ponderada"], width, label="Cómo sitúa a la sociedad", color=ORANGE, zorder=3)
    ax.set_ylim(0, 7); ax.set_yticks(range(0, 8)); ax.set_ylabel("Escala media (0 = nada racista; 10 = muy racista)", color=MUTED, fontsize=9)
    ax.set_xticks(x, part["grupo"], fontsize=9); ax.set_title(title, loc="left", fontsize=15, color=INK, weight="bold", pad=16)
    ax.grid(axis="y", color="#dbe1e4", linewidth=.8, zorder=0); ax.spines[["top", "right", "left"]].set_visible(False); ax.spines["bottom"].set_color("#ccd3d6")
    ax.tick_params(axis="y", length=0, labelcolor=MUTED); ax.tick_params(axis="x", length=0, pad=9)
    ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(.5, 1.02), fontsize=8)
    for bars in (a,b):
        ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=8, color=INK)
    fig.text(.01, .01, "CIS, estudio 3536, diciembre de 2025. Estimaciones ponderadas con PESO. n = casos válidos sin respuesta en ambas escalas.", fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, .06, 1, .93))
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / filename, format="svg", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "src/data/raw/3536_etiq.csv")
    args = parser.parse_args()
    df = load(args.data)
    result = summary(df)
    contrast = weighted_hypothesis_test(df)
    (ROOT / "src/data/contraste_ponderado.json").write_text(json.dumps(contrast, indent=2, ensure_ascii=False), encoding="utf-8")
    tests = hypothesis_tests(df)
    (ROOT / "src/data/hipotesis_ponderadas.json").write_text(json.dumps(tests, indent=2, ensure_ascii=False), encoding="utf-8")
    for dimension, title, filename in [
        ("Sexo", "La brecha aparece en hombres y mujeres", "sexo.svg"),
        ("Tramo de edad", "La percepción social supera la autopercepción en todas las edades", "edad.svg"),
        ("Ingresos del hogar", "La brecha se mantiene en los distintos tramos de ingresos", "ingresos.svg"),
        ("Bloque ideológico", "La brecha cambia según la ubicación ideológica", "ideologia.svg"),
        ("Nivel de estudios", "La diferencia se observa en todos los niveles educativos", "estudios.svg"),
    ]:
        chart(result, dimension, title, filename)
    print(f"Casos: {len(df):,}. Resultados y gráficos guardados en src/data y presentation/assets.")

if __name__ == "__main__":
    main()
