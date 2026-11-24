import joblib
import numpy as np
import pandas as pd

from pathlib import Path


# ==========================================
# NETSHIELD - ML PREDICTION ENGINE
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "netshield_rf_model.joblib"
)


class NetShieldPredictor:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Trained model not found: {MODEL_PATH}"
            )

        # Load only trusted model files created locally.
        model_data = joblib.load(MODEL_PATH)

        self.model = model_data["model"]
        self.features = model_data["features"]

        print("NetShield ML Model Loaded Successfully!")

    def predict(self, flow_data):

        if not isinstance(flow_data, dict):
            raise TypeError(
                "Flow data must be a dictionary."
            )

        missing = [
            feature
            for feature in self.features
            if feature not in flow_data
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        values = {}

        for feature in self.features:

            value = float(flow_data[feature])

            if not np.isfinite(value):
                raise ValueError(
                    f"Invalid value for {feature}"
                )

            if value < 0:
                raise ValueError(
                    f"Negative value for {feature}"
                )

            values[feature] = value

        X = pd.DataFrame(
            [values],
            columns=self.features
        )

        prediction = int(
            self.model.predict(X)[0]
        )

        probabilities = self.model.predict_proba(X)[0]

        classes = list(self.model.classes_)

        attack_index = classes.index(1)

        attack_probability = float(
            probabilities[attack_index]
        )

        result = {
            "prediction": prediction,
            "label": (
                "ATTACK"
                if prediction == 1
                else "BENIGN"
            ),
            "attack_probability": round(
                attack_probability,
                4
            ),
            "model": "Random Forest",
            "status": "success"
        }

        return result


# ==========================================
# TEST PREDICTION
# ==========================================

def main():

    print("=" * 55)
    print("       NETSHIELD ML PREDICTION ENGINE")
    print("=" * 55)

    predictor = NetShieldPredictor()

    # Demonstration input only.
    # These values are not a validated traffic sample.
    sample_flow = {
        "Flow Duration": 100000,
        "Total Fwd Packets": 20,
        "Total Backward Packets": 10,
        "Total Length of Fwd Packets": 12000,
        "Total Length of Bwd Packets": 5000,
        "Flow Bytes/s": 170000,
        "Flow Packets/s": 300,
        "SYN Flag Count": 2,
        "ACK Flag Count": 10
    }

    result = predictor.predict(sample_flow)

    print("\nPrediction Results:")
    print("-" * 55)

    print("Classification:", result["label"])

    print(
        "Attack Probability:",
        f"{result['attack_probability'] * 100:.2f}%"
    )

    print("Prediction Status:", result["status"])

    print("\nPrediction completed successfully!")


if __name__ == "__main__":
    main()