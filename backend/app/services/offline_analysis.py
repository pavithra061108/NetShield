import json

from pathlib import Path

from backend.app.ml.predict import NetShieldPredictor

from backend.app.database.database import (
    initialize_database,
    save_result
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

FEATURE_FILE = (
    PROJECT_ROOT
    / "tests"
    / "compatibility"
    / "netshield_features.json"
)


def run_offline_analysis():

    initialize_database()

    if not FEATURE_FILE.exists():

        raise FileNotFoundError(
            "Synthetic feature file not found."
        )

    with open(
        FEATURE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        flows = json.load(file)

    predictor = NetShieldPredictor()

    results = []
    skipped = 0

    for features in flows:

        if features["Flow Duration"] <= 0:

            skipped += 1
            continue

        prediction = predictor.predict(features)

        record_id = save_result(
            FEATURE_FILE.name,
            features,
            prediction
        )

        results.append({
            "id": record_id,
            "features": features,
            **prediction
        })

    return {
        "status": "success",
        "mode": "Offline synthetic demonstration",
        "processed": len(results),
        "skipped": skipped,
        "results": results
    }