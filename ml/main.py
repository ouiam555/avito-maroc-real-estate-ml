import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# =========================
# DATABASE CONNECTION
# =========================

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "avito_db"
DB_USER = "postgres"
DB_PASSWORD = "ouiamouiam"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
0
# =========================
# LOAD DATA
# =========================

query = "SELECT * FROM ml_schema.obt_avito;"

df = pd.read_sql(query, engine)

print("Dataset shape:", df.shape)
print(df.head())

# =========================
# CLEAN DATA
# =========================

# Remove missing values
df = df.dropna()

# Optional: remove duplicates
df = df.drop_duplicates()

# =========================
# FEATURES / TARGET
# =========================

# Predict price
y = df["prix"]

# Remove useless columns
X = df.drop(columns=[
    "prix",
    "avito_id",
    "lien"
])

# IMPORTANT:
# 'titre' can create too many categories.
# Remove it first for better baseline performance.

if "titre" in X.columns:
    X = X.drop(columns=["titre"])

# =========================
# FEATURE TYPES
# =========================

categorical_features = ["ville"]

numeric_features = [
    "surface",
    "chambres",
    "salle_de_bain",
    "prix_m2"
]

# =========================
# PREPROCESSING
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "num",
            "passthrough",
            numeric_features
        )
    ]
)

# =========================
# TRAIN / TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# LINEAR REGRESSION
# =========================

lr_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LinearRegression())
])

lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)

# =========================
# DECISION TREE
# =========================

tree_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    (
        "model",
        DecisionTreeRegressor(
            max_depth=10,
            random_state=42
        )
    )
])

tree_model.fit(X_train, y_train)

tree_pred = tree_model.predict(X_test)

# =========================
# EVALUATION FUNCTION
# =========================

def evaluate(name, y_true, y_pred):

    mae = mean_absolute_error(y_true, y_pred)

    rmse = np.sqrt(
        mean_squared_error(y_true, y_pred)
    )

    r2 = r2_score(y_true, y_pred)

    print("\n" + "=" * 40)
    print(name)
    print("=" * 40)

    print(f"MAE  : {mae:,.2f}")
    print(f"RMSE : {rmse:,.2f}")
    print(f"R2   : {r2:.4f}")

# =========================
# RESULTS
# =========================

evaluate(
    "Linear Regression",
    y_test,
    lr_pred
)

evaluate(
    "Decision Tree",
    y_test,
    tree_pred
)