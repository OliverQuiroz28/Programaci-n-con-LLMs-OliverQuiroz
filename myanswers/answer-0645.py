import pandas as pd

def calcular_antiguedad_salarial(df):
    df = df.copy()
    df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'])
    df['antiguedad_anios'] = ((pd.Timestamp.today() - df['fecha_ingreso']).dt.days / 365.25).round(2)
    df = df[df['activo'] == True]
    resultado = df.groupby('departamento').agg(
        salario_promedio=('salario', lambda x: round(x.mean(), 2)),
        antiguedad_promedio=('antiguedad_anios', lambda x: round(x.mean(), 2)),
        n_empleados=('empleado_id', 'count')
    ).reset_index().sort_values('salario_promedio', ascending=False).reset_index(drop=True)
    return resultado
