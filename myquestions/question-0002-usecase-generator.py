import pandas as pd
import numpy as np

def generar_caso_de_uso_clasificar_parcelas():
    np.random.seed(None)  # Semilla aleatoria cada ejecución

    n = np.random.randint(6, 15)

    # Generar datos base aleatorios dentro de rangos realistas
    nitrogeno        = np.random.uniform(5, 60, n).round(1)
    humedad          = np.random.uniform(10, 80, n).round(1)
    temperatura      = np.random.uniform(15, 45, n).round(1)
    iaf              = np.random.uniform(0.5, 6.0, n).round(2)
    dias_ultimo_riego = np.random.randint(0, 15, n).astype(float)

    df = pd.DataFrame({
        "nitrogeno":         nitrogeno,
        "humedad":           humedad,
        "temperatura":       temperatura,
        "iaf":               iaf,
        "dias_ultimo_riego": dias_ultimo_riego,
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
    df_limpio = df.drop_duplicates().dropna().reset_index(drop=True)

    condiciones = [
        (df_limpio["nitrogeno"] < 20) |
        (df_limpio["humedad"] < 25),

        (df_limpio["temperatura"] >= 35) |
        (df_limpio["dias_ultimo_riego"] >= 7),
    ]
    categorias = ["urgente", "moderada"]

    df_limpio["intervencion"] = np.select(condiciones, categorias, default="sin_intervencion")

    df_limpio = df_limpio.sort_values("dias_ultimo_riego").reset_index(drop=True)

    input_data  = {"df": df.copy()}
    output_data = df_limpio.copy()

    return input_data, output_data


# --- Ejemplo de uso ---
if __name__ == "__main__":
    input_data, output_data = generar_caso_de_uso_clasificar_parcelas()
    print("=== INPUT ===")
    print(input_data["df"].to_string())
    print("\n=== OUTPUT ESPERADO ===")
    print(output_data.to_string())
