import json
import shutil

from pathlib import Path

from backend.app.ml.predict import NetShieldPredictor


# ==========================================
# PROJECT PATHS
# ==========================================

ROOT = Path(__file__).resolve().parent

OUTPUT = ROOT / "frontend" / "public" / "data"

OUTPUT.mkdir(parents=True, exist_ok=True)

FEATURE_FILE = (
    ROOT
    / "tests"
    / "compatibility"
    / "netshield_features.json"
)

VALIDATION_FILE = (
    ROOT
    / "tests"
    / "compatibility"
    / "extended"
    / "reports"
    / "validation_summary.json"
)


# ==========================================
# LOAD SYNTHETIC FEATURES
# ==========================================

with open(FEATURE_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

if isinstance(data, dict):
    data = data.get("flows", [data])


# ==========================================
# GENERATE DEMONSTRATION PREDICTIONS
# ==========================================

predictor = NetShieldPredictor()

records = []

for item in data:

    features = item.get("features", item)

    if float(features.get("Flow Duration", 0)) <= 0:
        continue

    result = predictor.predict(features)

    records.append({
        "source_file": "Synthetic demonstration",
        "features": features,
        "label": result["label"],
        "probability": result["attack_probability"],
        "model": result["model"]
    })

if not records:
    raise ValueError("No valid synthetic records found.")


# ==========================================
# EXPORT DEMONSTRATION DATA
# ==========================================

with open(
    OUTPUT / "predictions.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        records,
        file,
        indent=4,
        allow_nan=False
    )


# ==========================================
# EXPORT VALIDATION REPORT
# ==========================================

shutil.copyfile(
    VALIDATION_FILE,
    OUTPUT / "validation.json"
)


# ==========================================
# EXPORT MODEL PERFORMANCE
# ==========================================

metrics = {
    "algorithm": "Random Forest",
    "dataset": "CIC-IDS2017",
    "features": 9,
    "accuracy": 99.95,
    "precision": 99.97,
    "recall": 99.94,
    "f1_score": 99.96,
    "evaluation_type": "Random held-out test split",
    "independent_real_world_validation": False
}

with open(
    OUTPUT / "metrics.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(metrics, file, indent=4)


# ==========================================
# COMPLETION MESSAGE
# ==========================================

print("=" * 55)
print("       NETSHIELD DEMONSTRATION EXPORT")
print("=" * 55)

print("Exported records:", len(records))
print("Output folder:", OUTPUT)

print("\nFiles generated:")
print("1. predictions.json")
print("2. validation.json")
print("3. metrics.json")

print("\nExport completed successfully!")