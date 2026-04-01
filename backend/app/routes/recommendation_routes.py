from fastapi import APIRouter

from app.agents.bias_detector import BiasDetector
from app.agents.recommender import Recommender
from app.schemas.recommendation_schema import RecommendationSchema
from app.schemas.suitability_schema import SuitabilityRequest, SuitabilityResponse

router = APIRouter()
recommender = Recommender()
bias_detector = BiasDetector()

@router.get("/{user_id}")
async def get_recommendations(user_id: int):
    """Get a demo suitability-backed recommendation set for a user."""
    demo_request = SuitabilityRequest(
        age=31,
        income_level="medium",
        monthly_income=90000,
        monthly_expenses=50000,
        income_stability="stable",
        investment_experience="intermediate",
        financial_literacy_level="moderate",
        current_holdings=[
            {"name": "Large Cap Fund", "sector": "diversified", "value": 180000},
            {"name": "Tech Growth Fund", "sector": "technology", "value": 60000},
        ],
        current_holdings_value=240000,
        liabilities=120000,
        emergency_fund_months=5,
        financial_goal="long_term_wealth_creation",
        time_horizon_years=8,
        liquidity_needs="medium",
        return_expectations="balanced",
        volatility_comfort=3,
        drawdown_tolerance=3,
        return_preference="balanced",
    )
    result = recommender.generate_recommendations(demo_request.model_dump())
    result["user_id"] = user_id
    return result

@router.post("/")
async def create_recommendation(recommendation: RecommendationSchema):
    """Create a new recommendation"""
    return {"status": "created", "recommendation": recommendation}

@router.get("/{user_id}/bias-profile")
async def get_bias_profile(user_id: int):
    """Get a rule-based bias profile for a demo user."""
    analysis = bias_detector.detect_bias(
        {
            "recent_trades": 9,
            "portfolio_turnover": "high",
            "panic_sell_history": True,
            "sector_concentration": 0.42,
        }
    )
    analysis["user_id"] = user_id
    return analysis


@router.post("/suitability", response_model=SuitabilityResponse)
async def evaluate_suitability(request: SuitabilityRequest):
    """Evaluate suitability for a user profile and return ranked recommendations."""
    return recommender.generate_recommendations(request.model_dump())
