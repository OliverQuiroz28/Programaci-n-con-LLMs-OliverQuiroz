import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Lasso

def seleccionar_features_polinomiales(df, feature_cols, target_col, degree, alpha):
    X = df[feature_cols]
    y = df[target_col]
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X)
    lasso = Lasso(alpha=alpha, random_state=42)
    lasso.fit(X_poly, y)
    return np.where(lasso.coef_ != 0)[0]
