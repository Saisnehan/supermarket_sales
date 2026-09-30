import ast

with open("app.py", encoding="utf-8") as f:
    code = f.read()

ast.parse(code)
print("Syntax OK")

# New universal-child-selector approach
assert 'data-baseweb="tab"] *' in code,          "universal child selector missing"
assert "-webkit-text-fill-color: #1e293b" in code, "webkit fill colour for inactive missing"
assert "-webkit-text-fill-color: #ffffff" in code, "webkit fill colour for active missing"
assert "visibility: visible" in code,              "visibility override missing"
assert "opacity: 1 !important" in code,            "opacity override missing"
assert "#dde3ec" in code,                          "inactive tab bg missing"
assert "#e8edf2" in code,                          "tab-list bg missing"
assert "#1e293b" in code,                          "inactive text colour missing"
assert "aria-selected" in code,                    "active tab selector missing"
print("All tab-bar selectors present (universal * approach)")

# Untouched sections
assert "kpi-card" in code,          "KPI card CSS missing"
assert "sidebar-title" in code,     "sidebar CSS missing"
assert "app-footer" in code,        "footer CSS missing"
assert "load_data" in code,         "data load function missing"
assert "Calculated Sales" in code,  "sales calc missing"
print("All untouched sections intact")
