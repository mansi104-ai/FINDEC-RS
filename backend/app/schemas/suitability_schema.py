from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HoldingInput(BaseModel):
    name: str
    sector: str
    value: float = Field(ge=0)


class SuitabilityRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    income_level: str
    monthly_income: float = Field(ge=0)
    monthly_expenses: float = Field(ge=0)
    income_stability: str
    investment_experience: str
    financial_literacy_level: str
    current_holdings: list[HoldingInput] = Field(default_factory=list)
    current_holdings_value: float = Field(ge=0, default=0)
    liabilities: float = Field(ge=0, default=0)
    emergency_fund_months: float = Field(ge=0, default=0)
    financial_goal: str
    time_horizon_years: float = Field(gt=0)
    liquidity_needs: str
    return_expectations: str
    volatility_comfort: int = Field(ge=1, le=5)
    drawdown_tolerance: int = Field(ge=1, le=5)
    return_preference: str


class ScoredRecommendation(BaseModel):
    recommendation_id: str
    name: str
    asset_type: str
    suitability_score: float
    suitability_label: str
    explanation_summary: str
    risk_warnings: list[str]
    confidence_score: float
    content_match_score: float
    rationale_factors: list[str]
    next_best_action: str


class RejectedAlternative(BaseModel):
    recommendation_id: str
    name: str
    reason: str


class SuitabilityResponse(BaseModel):
    normalized_user_profile: dict[str, Any]
    goal_context: dict[str, Any]
    risk_profile: dict[str, Any]
    preference_profile: dict[str, Any]
    recommendations: list[ScoredRecommendation]
    rejected_alternatives: list[RejectedAlternative]
    engine_summary: str
