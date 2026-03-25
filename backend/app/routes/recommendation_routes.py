from fastapi import APIRouter
from app.schemas.recommendation_schema import RecommendationSchema

router = APIRouter()

@router.get("/{user_id}")
async def get_recommendations(user_id: int):
    """Get recommendations for a user"""
    return {
        "user_id": user_id,
        "recommendations": [
            {
                "id": 1,
                "title": "Review Investment Portfolio",
                "description": "Based on your profile, we recommend reviewing your investment allocations",
                "category": "portfolio",
                "confidence": 0.85
            }
        ]
    }

@router.post("/")
async def create_recommendation(recommendation: RecommendationSchema):
    """Create a new recommendation"""
    return {"status": "created", "recommendation": recommendation}

@router.get("/{user_id}/bias-profile")
async def get_bias_profile(user_id: int):
    """Get bias profile for a user"""
    return {
        "user_id": user_id,
        "bias_score": 45.5,
        "risk_level": "medium",
        "factors": ["anchoring", "confirmation_bias", "status_quo_bias"]
    }
