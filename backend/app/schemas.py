from pydantic import BaseModel


class HealthResponse(BaseModel):

    status: str
    timestamp: str


class StatisticsResponse(BaseModel):

    total_flows: int
    benign_flows: int
    flagged_flows: int
    analysis_mode: str