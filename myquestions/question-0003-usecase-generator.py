import pandas as pd
import numpy as np

def generar_caso_de_uso_clasificar_envios():
    np.random.seed(None)  # Semilla aleatoria cada ejecución

    n = np.random.randint(6, 15)

    # Generar datos base aleatorios dentro de rangos realistas
    peso_kg                    = np.random.uniform(0.5, 30.0, n).round(1)
    distancia_km               = np.random.randint(50, 1500, n).astype(float)
    dias_transito              = np.random.randint(1, 15, n).astype(float)
    temperatura_almacenamiento = np.random.uniform(10, 40, n).round(1)
    manipulaciones             = np.random.randint(1, 12, n).astype(float)

    df = pd.DataFrame({
        "peso_kg":                    peso_kg,
        "distancia_km":               distancia_km,
        "dias_transito":              dias_transito,
        "temperatura_almacenamiento": temperatura_almacenamiento,
        "manipulaciones":             manipulaciones,
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
        (df_limpio["dias_transito"] >= 10) |
        (df_limpio["manipulaciones"] >= 8),

        (df_limpio["dias_transito"] >= 6) |
        (df_limpio["temperatura_almacenamiento"] >= 30),
    ]
    categorias = ["retraso_critico", "en_riesgo"]

    df_limpio["estado_envio"] = np.select(condiciones, categorias, default="en_tiempo")

    df_limpio = df_limpio.sort_values("dias_transito").reset_index(drop=True)

    input_data  = {"df": df.copy()}
    output_data = df_limpio.copy()

    return input_data, output_data


# --- Ejemplo de uso ---
if __name__ == "__main__":
    input_data, output_data = generar_caso_de_uso_clasificar_envios()
    print("=== INPUT ===")
    print(input_data["df"].to_string())
    print("\n=== OUTPUT ESPERADO ===")
    print(output_data.to_string())
