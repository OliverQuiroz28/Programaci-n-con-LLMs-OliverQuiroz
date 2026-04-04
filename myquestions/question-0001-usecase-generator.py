import pandas as pd
import numpy as np

def generar_caso_de_uso_clasificar_estado_turbina():
    np.random.seed(None)  # Semilla aleatoria cada ejecución

    n = np.random.randint(6, 15)

    # Generar datos base aleatorios
    frecuencia_vibracion  = np.random.uniform(20, 100, n).round(1)
    temperatura_rodamiento = np.random.uniform(50, 100, n).round(1)
    amplitud_oscilacion   = np.random.uniform(0.1, 3.0, n).round(2)
    voltaje               = np.random.uniform(210, 230, n).round(1)
    horas_operacion       = np.random.randint(100, 2000, n).astype(float)

    df = pd.DataFrame({
        "frecuencia_vibracion":   frecuencia_vibracion,
        "temperatura_rodamiento": temperatura_rodamiento,
        "amplitud_oscilacion":    amplitud_oscilacion,
        "voltaje":                voltaje,
        "horas_operacion":        horas_operacion,
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
        (df_limpio["frecuencia_vibracion"] >= 80) |
        (df_limpio["temperatura_rodamiento"] >= 90),

        (df_limpio["frecuencia_vibracion"] >= 50) |
        (df_limpio["temperatura_rodamiento"] >= 70),
    ]
    categorias = ["critico", "advertencia"]

    df_limpio["nivel_alerta"] = np.select(condiciones, categorias, default="normal")

    df_limpio = df_limpio.sort_values("horas_operacion").reset_index(drop=True)

    input_data = {"df": df.copy()}
    output_data = df_limpio.copy()

    return input_data, output_data


# --- Ejemplo de uso ---
if __name__ == "__main__":
    input_data, output_data = generar_caso_de_uso_clasificar_estado_turbina()
    print("=== INPUT ===")
    print(input_data["df"].to_string())
    print("\n=== OUTPUT ESPERADO ===")
    print(output_data.to_string())
