import json
import os
import time
import logging

from pathlib import Path
from threading import Lock
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


# ==========================================
# PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("NetShield")


# ==========================================
# ANALYSIS REQUEST PROTECTION
# ==========================================

analysis_lock = Lock()

last_analysis_time = float("-inf")

ANALYSIS_COOLDOWN = 10


# ==========================================
# APPLICATION LIFESPAN
# ==========================================

@asynccontextmanager
async def lifespan(app):

    initialize_database()

    logger.info("NetShield Database Initialized!")

    yield

    logger.info("NetShield Backend Stopped!")


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="NetShield",
    description="Offline Network Security Analysis Dashboard",
    version="1.0.0",
    lifespan=lifespan
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

frontend_url = os.getenv("FRONTEND_URL")

if frontend_url:
    allowed_origins.append(
        frontend_url.strip().rstrip("/")
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "project": "NetShield",
        "status": "running",
        "version": "1.0.0",
        "mode": "Offline demonstration"
    }


# ==========================================
# HEALTH ENDPOINT
# ==========================================

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


# ==========================================
# STATISTICS ENDPOINT
# ==========================================

@app.get(
    "/api/statistics",
    response_model=StatisticsResponse
)
def statistics():

    return get_statistics()


# ==========================================
# NETWORK FLOWS ENDPOINT
# ==========================================

@app.get("/api/flows")
def flows():

    return get_results()


# ==========================================
# SECURITY ALERTS ENDPOINT
# ==========================================

@app.get("/api/alerts")
def alerts():

    return [
        row for row in get_results()
        if row["label"] == "ATTACK"
    ]


# ==========================================
# OFFLINE ANALYSIS ENDPOINT
# ==========================================

@app.post("/api/analyze")
def analyze():

    global last_analysis_time

    if not analysis_lock.acquire(blocking=False):

        raise HTTPException(
            status_code=429,
            detail="Analysis is already running."
        )

    try:

        current_time = time.monotonic()

        if (
            current_time - last_analysis_time
            < ANALYSIS_COOLDOWN
        ):

            raise HTTPException(
                status_code=429,
                detail="Please wait 10 seconds before running another analysis."
            )

        last_analysis_time = current_time

        result = run_offline_analysis()

        logger.info("Offline analysis completed.")

        return result

    except HTTPException:

        raise

    except Exception:

        logger.exception("Offline analysis failed.")

        raise HTTPException(
            status_code=500,
            detail="Offline analysis failed. Check backend logs."
        )

    finally:

        analysis_lock.release()


# ==========================================
# FEATURE VALIDATION ENDPOINT
# ==========================================

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

    try:

        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (OSError, json.JSONDecodeError):

        logger.exception("Unable to read validation report.")

        raise HTTPException(
            status_code=500,
            detail="Unable to load validation report."
        )


# ==========================================
# MACHINE LEARNING MODEL ENDPOINT
# ==========================================

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


# ==========================================
# APPLICATION STARTUP
# ==========================================

if __name__ == "__main__":

    import uvicorn

    port = int(os.getenv("PORT", "8000"))

    host = (
        "0.0.0.0"
        if os.getenv("RENDER") == "true"
        else "127.0.0.1"
    )

    uvicorn.run(
        app,
        host=host,
        port=port
    )