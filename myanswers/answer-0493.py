import pandas as pd

def filtrar_y_ordenar(df, min_price, min_rating):
    return df[(df["price"] > min_price) & (df["rating"] >= min_rating)]\
              .sort_values(by="price", ascending=False)
