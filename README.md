# Avito Maroc — Machine Learning Pipeline (Part 3)

Price prediction for the Moroccan real estate market using data from Avito.ma

---

## Context

This project is the **third part** of the Avito Maroc data pipeline.

After scraping and cleaning the data (Part 1) and building the Power BI dashboards (Part 2), this part focuses on training machine learning models to predict real estate prices.

The data is extracted from a dedicated ML schema in the Data Warehouse:

| Schema | Purpose |
|--------|---------|
| `bi_schema` | Star schema — used for Power BI dashboards |
| `ml_schema` | One Big Table (OBT) — used for Machine Learning |

All ML transformations are performed **after extraction from the database**, not before.

---

## Pipeline Architecture

```
ml_schema (OBT)
       |
       v
  Data Extraction
       |
       v
  Data Cleaning
  (dropna, drop_duplicates)
       |
       v
  Feature Selection
  (drop avito_id, lien, titre)
       |
       v
  Train / Test Split (80/20)
       |
       v
  Preprocessing
  (OneHotEncoder for ville, passthrough for numeric)
       |
       v
  Model Training
  (Linear Regression / Decision Tree)
       |
       v
  Evaluation
  (MAE, RMSE, R2)
```

---

## Project Structure

```
avito-ml/
│
├── ml_model.py           <- Main ML pipeline script
├── requirements.txt
└── README.md
```

---

## Data Source

The model connects to a **PostgreSQL** database and reads from:

```sql
SELECT * FROM ml_schema.obt_avito;
```

The OBT (One Big Table) contains all real estate features in a flat, consolidated format, already cleaned but not yet transformed for ML.

---

## Features

| Feature | Type | Description |
|---------|------|-------------|
| `ville` | Categorical | City / location |
| `surface` | Numeric | Surface area in m2 |
| `chambres` | Numeric | Number of bedrooms |
| `salle_de_bain` | Numeric | Number of bathrooms |
| `prix_m2` | Numeric | Price per m2 |

Target variable: `prix` (listing price in MAD)

Dropped columns: `avito_id`, `lien`, `titre` (too many categories, degrades baseline performance)

---

## Models

### Linear Regression

A baseline model to establish a performance reference. Trained using a scikit-learn Pipeline combining preprocessing and the estimator.

### Decision Tree Regressor

A non-linear model with `max_depth=10` to capture more complex relationships between features and price.

---

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| MAE | Mean Absolute Error — average prediction error in MAD |
| RMSE | Root Mean Squared Error — penalizes large errors more |
| R2 | Coefficient of determination — proportion of variance explained |

Results are printed to the console for both models.

---

## Preprocessing

Handled via a `ColumnTransformer` inside a scikit-learn `Pipeline`:

- `ville` encoded with `OneHotEncoder(handle_unknown="ignore")`
- Numeric features (`surface`, `chambres`, `salle_de_bain`, `prix_m2`) passed through without scaling

---

## Installation

### 1. Clone the repository

```bash
git clone <repository_url>
cd avito-ml
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### Requirements

```
pandas
numpy
sqlalchemy
psycopg2-binary
scikit-learn
```

---

## Configuration

Update the database credentials in `ml_model.py` before running:

```python
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "avito_db"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
```

---

## Running the Pipeline

```bash
python ml_model.py
```

Expected output:

```
Dataset shape: (XXXXX, X)

========================================
Linear Regression
========================================
MAE  : ...
RMSE : ...
R2   : ...

========================================
Decision Tree
========================================
MAE  : ...
RMSE : ...
R2   : ...
```

---

## Future Improvements

- Add feature engineering: log transformation of prices, surface x rooms interaction, geographic indicators
- Add normalization and standardization of numeric features
- Test additional models: Random Forest, XGBoost, LightGBM
- Hyperparameter tuning with GridSearchCV or RandomizedSearchCV
- Cross-validation for more robust evaluation
- Add a classification model to predict property characteristics
- Export trained models with joblib or pickle
- Automate full pipeline re-execution from OBT
- Add SHAP values for feature importance and model interpretability

---

## Author

Created by Ouiam Elkhalfi

Part 1 — Scraping & Data Cleaning: see Part 1 README  
Part 2 — Power BI Dashboards: see Part 2 README