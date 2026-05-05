from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class HoldingInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sector: str = Field(..., min_length=1, max_length=255)
    value: float = Field(ge=0)


class SuitabilityRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    income_level: str
    monthly_income: float = Field(ge=0, le=100000000)
    monthly_expenses: float = Field(ge=0, le=100000000)
    income_stability: str
    investment_experience: str
    financial_literacy_level: str
    current_holdings: list[HoldingInput] = Field(default_factory=list, max_length=100)
    current_holdings_value: float = Field(ge=0, le=1000000000, default=0)
    liabilities: float = Field(ge=0, le=1000000000, default=0)
    emergency_fund_months: float = Field(ge=0, le=120, default=0)
    financial_goal: str
    time_horizon_years: float = Field(gt=0, le=80)
    liquidity_needs: str
    return_expectations: str
    volatility_comfort: int = Field(ge=1, le=5)
    drawdown_tolerance: int = Field(ge=1, le=5)
    return_preference: str
    portfolio_type: str = Field(default="balanced", description="Type of portfolio: conservative, balanced, aggressive, or growth")

    @field_validator("monthly_expenses", mode="after")
    @classmethod
    def validate_expenses_not_exceed_income(cls, v: float, info) -> float:
        """Validate that monthly expenses do not exceed monthly income."""
        if "monthly_income" in info.data:
            monthly_income = info.data["monthly_income"]
            if v > monthly_income:
                raise ValueError(
                    f"Monthly expenses ({v}) cannot exceed monthly income ({monthly_income}). "
                    f"Please ensure expenses are less than or equal to income."
                )
        return v

    @field_validator("current_holdings_value", mode="after")
    @classmethod
    def validate_holdings_value(cls, v: float, info) -> float:
        """Validate that current holdings value is non-negative."""
        if v < 0:
            raise ValueError("Current holdings value cannot be negative")
        return v

    @field_validator("liabilities", mode="after")
    @classmethod
    def validate_liabilities(cls, v: float, info) -> float:
        """Validate liabilities is non-negative and reasonable."""
        if v < 0:
            raise ValueError("Liabilities cannot be negative")
        if v > 1000000000:
            raise ValueError("Liabilities value too large")
        return v


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


class PortfolioAllocation(BaseModel):
    asset_type: str
    percentage: float = Field(ge=0, le=100)
    rationale: str


class PortfolioRecommendation(BaseModel):
    portfolio_type: str
    expected_return: str
    risk_level: str
    allocations: list[PortfolioAllocation]
    description: str
    suitable_for: list[str]


class SuitabilityResponse(BaseModel):
    normalized_user_profile: dict[str, Any]
    goal_context: dict[str, Any]
    risk_profile: dict[str, Any]
    preference_profile: dict[str, Any]
    recommendations: list[ScoredRecommendation]
    rejected_alternatives: list[RejectedAlternative]
    portfolio_recommendations: list[PortfolioRecommendation]
    engine_summary: str
