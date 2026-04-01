from app.services.suitability_engine import SuitabilityEngine


class Recommender:
    """Agent for generating suitability-aware financial recommendations."""

    def __init__(self):
        self.recommendation_engine = SuitabilityEngine()

    def generate_recommendations(self, user_context: dict) -> dict:
        """Generate scored recommendations from the suitability engine."""
        return self.recommendation_engine.evaluate(user_context)

    def rank_recommendations(self, recommendations: list[dict]) -> list[dict]:
        """Rank recommendations by suitability and confidence."""
        return sorted(
            recommendations,
            key=lambda item: (item.get("suitability_score", 0), item.get("confidence_score", 0)),
            reverse=True,
        )
