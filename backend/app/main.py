import json

from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database.database import (
    initialize_database,
    get_results,
    get_statistics
)

from backend.app.services.offline_analysis import (
    run_offline_analysis
)

from backend.app.schemas import (
    HealthResponse,
    StatisticsResponse
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@asynccontextmanager
async def lifespan(app):

    initialize_database()

    print("NetShield Database Initialized!")

    yield


app = FastAPI(
    title="NetShield",
    description="Offline Network Security Analysis Dashboard",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


@app.get("/")
def home():

    return {
        "project": "NetShield",
        "status": "running",
        "version": "1.0.0",
        "mode": "Offline demonstration"
    }


@app.get(
    "/api/health",
    response_model=HealthResponse
)
def health():

    return {
        "status": "healthy",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }


@app.get(
    "/api/statistics",
    response_model=StatisticsResponse
)
def statistics():

    return get_statistics()


@app.get("/api/flows")
def flows():

    return get_results()


@app.get("/api/alerts")
def alerts():

    return [
        row for row in get_results()
        if row["label"] == "ATTACK"
    ]


@app.post("/api/analyze")
def analyze():

    try:

        return run_offline_analysis()

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/api/validation")
def validation():

    report_path = (
        PROJECT_ROOT
        / "tests"
        / "compatibility"
        / "extended"
        / "reports"
        / "validation_summary.json"
    )

    if not report_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Validation report not found."
        )

    with open(
        report_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


@app.get("/api/model")
def model_information():

    return {
        "algorithm": "Random Forest",
        "dataset": "CIC-IDS2017",
        "features": 9,
        "evaluation_type": "Random held-out test split",
        "accuracy": 99.95,
        "precision": 99.97,
        "recall": 99.94,
        "f1_score": 99.96,
        "independent_real_world_validation": False
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )