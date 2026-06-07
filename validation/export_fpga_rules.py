import joblib

from sklearn.tree import (
    export_text
)

model = joblib.load(
    "validation/dimension_agent.pkl"
)

rules = export_text(

    model,

    feature_names=[

        "loss",

        "phase",

        "jitter",

        "pol"

    ]
)

print()
print("="*80)
print("FPGA RULES")
print("="*80)
print()

print(rules)