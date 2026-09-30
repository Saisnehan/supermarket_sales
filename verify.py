import os, sys, ast, importlib

SEPARATOR = "-" * 60

def check(n, msg):
    print(f"[CHECK {n}] {msg}")

# ── Check 1: CSV file exists ─────────────────────────────────────────────────
csv = "SuperMarket_Sales_data.csv"
assert os.path.isfile(csv), f"FAIL: {csv} not found in project folder"
check(1, f"CSV exists -> {csv}  ({os.path.getsize(csv):,} bytes)")

# ── Check 2: app.py loads CSV via relative path ──────────────────────────────
with open("app.py", encoding="utf-8") as f:
    src = f.read()

assert "SuperMarket_Sales_data.csv" in src, "FAIL: CSV filename not referenced in app.py"
assert 'CSV_PATH = "SuperMarket_Sales_data.csv"' in src, \
    "FAIL: CSV_PATH not set to the expected relative path"
assert not src.count("C:\\") and not src.count("C:/"), \
    "FAIL: absolute Windows path found in app.py"
check(2, "app.py uses relative path  ->  CSV_PATH = \"SuperMarket_Sales_data.csv\"")

# ── Check 3: requirements.txt has every needed package ───────────────────────
with open("requirements.txt") as f:
    reqs = f.read()

required = ["streamlit", "pandas", "numpy", "plotly"]
for pkg in required:
    assert pkg in reqs, f"FAIL: '{pkg}' missing from requirements.txt"
check(3, "requirements.txt contains: " + ", ".join(required))

# ── Check 4a: Python syntax ──────────────────────────────────────────────────
with open("app.py", encoding="utf-8") as f:
    code = f.read()
ast.parse(code)
check(4, "app.py syntax is valid (ast.parse passed)")

# ── Check 4b: all imports are installed ──────────────────────────────────────
for mod in ["streamlit", "pandas", "numpy", "plotly.express",
            "plotly.graph_objects", "plotly.subplots"]:
    try:
        importlib.import_module(mod)
    except ImportError as e:
        print(f"FAIL: cannot import '{mod}': {e}")
        sys.exit(1)
check("4b", "All imports resolve: streamlit, pandas, numpy, plotly.*")

# ── Check 5: end-to-end data pipeline ────────────────────────────────────────
import pandas as pd
import numpy as np

df = pd.read_csv(csv, sep="\t")
df.columns = df.columns.str.strip()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
for col in ["Quantity", "Unit Price", "Sales", "Rating"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Calculated Sales"] = df["Quantity"] * df["Unit Price"]
df["Month"]    = df["Date"].dt.to_period("M").astype(str)
df["Month_dt"] = df["Date"].dt.to_period("M").dt.to_timestamp()
df["Day"]      = df["Date"].dt.day_name()

assert len(df) == 500,                    f"FAIL: expected 500 rows, got {len(df)}"
assert df["Sales"].isna().sum()   == 0,   "FAIL: NaN in Sales"
assert df["Date"].isna().sum()    == 0,   "FAIL: NaN in Date"
assert df.duplicated().sum()      == 0,   "FAIL: duplicate rows detected"

mismatch = ((df["Sales"] - df["Calculated Sales"]).abs() > 0.01).sum()

check(5, "Data pipeline complete")
print(f"    Rows           : {len(df)}")
print(f"    Columns        : {df.shape[1]}")
print(f"    Missing values : {df.isna().sum().sum()}")
print(f"    Duplicates     : {df.duplicated().sum()}")
print(f"    Sales mismatches (>0.01): {mismatch}")
print(f"    Total Revenue  : Rs {df['Sales'].sum():,.2f}")
print(f"    Categories     : {df['Category'].nunique()} -> {sorted(df['Category'].unique())}")
print(f"    Cities         : {sorted(df['City'].unique())}")
print(f"    Payment types  : {sorted(df['Payment'].unique())}")

print()
print(SEPARATOR)
print("ALL CHECKS PASSED — streamlit run app.py is ready to execute.")
print(SEPARATOR)
