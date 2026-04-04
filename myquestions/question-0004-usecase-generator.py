import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def generar_caso_de_uso_clasificar_frentes_mineros():
    np.random.seed(None)  # Semilla aleatoria cada ejecución

    n = np.random.randint(6, 15)

    # Generar datos base aleatorios dentro de rangos realistas
    polvo_aire        = np.random.uniform(1.0, 12.0, n).round(1)
    gases_toxicos     = np.random.uniform(5.0, 80.0, n).round(1)
    temperatura_tunel = np.random.uniform(20.0, 50.0, n).round(1)
    ruido_db          = np.random.uniform(70.0, 110.0, n).round(1)
    horas_operacion   = np.random.randint(1, 12, n).astype(float)

    df = pd.DataFrame({
        "polvo_aire":        polvo_aire,
        "gases_toxicos":     gases_toxicos,
        "temperatura_tunel": temperatura_tunel,
        "ruido_db":          ruido_db,
        "horas_operacion":   horas_operacion,
    })

    # Insertar duplicados aleatorios (1 o 2)
    n_dups = np.random.randint(1, 3)
    idx_dup = np.random.choice(df.index, size=n_dups, replace=False)
    df = pd.concat([df, df.iloc[idx_dup]], ignore_index=True)

    # Insertar nulos aleatorios (1 o 2)
    n_nulos = np.random.randint(1, 3)
    for _ in range(n_nulos):
        fila = np.random.randint(0, len(df))
        col  = np.random.choice(df.columns)
        df.at[fila, col] = np.nan

    # --- Calcular output esperado ---

    # 1. Limpieza
    df_limpio = df.drop_duplicates().dropna().reset_index(drop=True)

    # 2. Asignar nivel_riesgo sobre valores ORIGINALES
    condiciones = [
        (df_limpio["gases_toxicos"] >= 50) |
        (df_limpio["temperatura_tunel"] >= 38),

        (df_limpio["polvo_aire"] >= 5) |
        (df_limpio["ruido_db"] >= 90),
    ]
    categorias = ["peligroso", "precaucion"]
    df_limpio["nivel_riesgo"] = np.select(condiciones, categorias, default="seguro")

    # 3. Ordenar por horas_operacion original antes de escalar
    df_limpio = df_limpio.sort_values("horas_operacion").reset_index(drop=True)

    # 4. Escalar columnas numéricas con MinMaxScaler
    cols_numericas = ["polvo_aire", "gases_toxicos", "temperatura_tunel",
                      "ruido_db", "horas_operacion"]
    scaler = MinMaxScaler()
    df_limpio[cols_numericas] = scaler.fit_transform(df_limpio[cols_numericas])
    df_limpio[cols_numericas] = df_limpio[cols_numericas].round(4)

    input_data  = {"df": df.copy()}
    output_data = df_limpio.copy()

    return input_data, output_data


# --- Ejemplo de uso ---
if __name__ == "__main__":
    input_data, output_data = generar_caso_de_uso_clasificar_frentes_mineros()
    print("=== INPUT ===")
    print(input_data["df"].to_string())
    print("\n=== OUTPUT ESPERADO ===")
    print(output_data.to_string())
