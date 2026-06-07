import pandas as pd

from sklearn.tree import (
    DecisionTreeClassifier
)

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

import joblib

df = pd.read_csv(
    "validation/dimension_training_data.csv"
)

X = df[

    [

        "loss_db",

        "phase_noise_rad",

        "timing_jitter_ps",

        "polarization_drift_deg"

    ]

]

y = df["optimal_d"]

X_train, X_test, y_train, y_test = (

    train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42
    )

)

model = DecisionTreeClassifier(

    max_depth=8,

    random_state=42
)

model.fit(

    X_train,

    y_train
)

pred = model.predict(
    X_test
)

print()
print("="*80)
print("DIMENSION AGENT")
print("="*80)

print()

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        pred
    )
)

print()

print(
    classification_report(
        y_test,
        pred
    )
)

print()

print(
    confusion_matrix(
        y_test,
        pred
    )
)

print()

print(
    "Feature Importance"
)

for name,imp in zip(

    X.columns,

    model.feature_importances_
):

    print(
        f"{name:<25}"
        f"{imp:.4f}"
    )

joblib.dump(

    model,

    "validation/dimension_agent.pkl"
)

print()
print(
    "Model Saved"
)