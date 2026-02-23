import pandas as pd


HEROES = ["olenthero", "thorgin", "amalyria", "basajorn", "lamyreth", "sugarth"]


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    # 1. POTENCIA BRUTA DEL EQUIPO
    df["total_vida_equipo"] = 0.0
    df["total_mana_equipo"] = 0.0
    df["total_fisico_equipo"] = 0.0
    df["total_agilidad_equipo"] = 0.0
    df["tamano_equipo"] = 0

    for hero in HEROES:
        en_equipo = df[f"{hero}_en_equipo"]
        df["total_vida_equipo"] += df[f"{hero}_vida"] * en_equipo
        df["total_mana_equipo"] += df[f"{hero}_mana"] * en_equipo
        df["total_fisico_equipo"] += df[f"{hero}_fisico"] * en_equipo
        df["total_agilidad_equipo"] += df[f"{hero}_agilidad"] * en_equipo
        df["tamano_equipo"] += en_equipo

    # 2. RATIOS Y EQUILIBRIO
    df["ratio_vida_mana"] = df["total_vida_equipo"] / (df["total_mana_equipo"] + 0.001)
    df["ratio_fisico_agilidad"] = df["total_fisico_equipo"] / (df["total_agilidad_equipo"] + 0.001)
    df["promedio_vida"] = df["total_vida_equipo"] / (df["tamano_equipo"] + 0.001)

    # 3. SINERGIAS ESPECÍFICAS
    tiene_tanque = (df["basajorn_en_equipo"] == 1) | (df["thorgin_en_equipo"] == 1)
    tiene_healer = df["amalyria_en_equipo"] == 1
    df["sinergia_tanque_healer"] = (tiene_tanque & tiene_healer).astype(int)

    df["sinergia_full_magic"] = (
        (df["olenthero_en_equipo"] == 1) & (df["amalyria_en_equipo"] == 1)
    ).astype(int)

    df["equipo_rapido"] = (
        df["total_agilidad_equipo"] > df["total_fisico_equipo"]
    ).astype(int)

    return df
