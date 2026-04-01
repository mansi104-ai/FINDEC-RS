from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.agents.recommender import Recommender
from app.services.asset_repository import DEFAULT_ASSET_SEED, init_db, replace_assets


def make_payload(**overrides):
    payload = {
        "age": 31,
        "income_level": "medium",
        "monthly_income": 90000,
        "monthly_expenses": 50000,
        "income_stability": "stable",
        "investment_experience": "intermediate",
        "financial_literacy_level": "moderate",
        "current_holdings": [
            {"name": "Large Cap Fund", "sector": "diversified", "value": 180000},
            {"name": "Tech Growth Fund", "sector": "technology", "value": 60000},
        ],
        "current_holdings_value": 240000,
        "liabilities": 120000,
        "emergency_fund_months": 5,
        "financial_goal": "long_term_wealth_creation",
        "time_horizon_years": 8,
        "liquidity_needs": "medium",
        "return_expectations": "balanced",
        "volatility_comfort": 3,
        "drawdown_tolerance": 3,
        "return_preference": "balanced",
    }
    payload.update(overrides)
    return payload


class RecommendationQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = str(BACKEND_ROOT / "tests" / "test_findec.db")
        db_file = Path(cls.db_path)
        if db_file.exists():
            db_file.unlink()
        os.environ["FINDEC_ASSET_DB"] = cls.db_path
        init_db()
        replace_assets(DEFAULT_ASSET_SEED)
        cls.recommender = Recommender()

    @classmethod
    def tearDownClass(cls):
        os.environ.pop("FINDEC_ASSET_DB", None)
        db_file = Path(cls.db_path)
        if db_file.exists():
            try:
                db_file.unlink()
            except PermissionError:
                pass

    def evaluate(self, **overrides):
        return self.recommender.generate_recommendations(make_payload(**overrides))

    def test_top_pick_accuracy_for_benchmark_personas(self):
        scenarios = [
            (
                "passive long-term",
                {
                    "financial_goal": "passive_investing",
                    "time_horizon_years": 12,
                    "return_preference": "balanced",
                    "liquidity_needs": "medium",
                },
                "index-nifty-core",
            ),
            (
                "short-term capital preservation",
                {
                    "financial_goal": "short_term_savings",
                    "time_horizon_years": 1,
                    "liquidity_needs": "high",
                    "return_preference": "steady",
                    "volatility_comfort": 1,
                    "drawdown_tolerance": 1,
                    "current_holdings": [],
                    "current_holdings_value": 20000,
                },
                "debt-short-shield",
            ),
            (
                "aggressive active investor",
                {
                    "financial_goal": "active_stock_selection",
                    "time_horizon_years": 10,
                    "return_preference": "high_upside",
                    "volatility_comfort": 5,
                    "drawdown_tolerance": 5,
                    "investment_experience": "advanced",
                    "financial_literacy_level": "advanced",
                    "current_holdings": [{"name": "Infra ETF", "sector": "industrials", "value": 150000}],
                },
                "stock-growth-alpha",
            ),
            (
                "learning explorer",
                {
                    "financial_goal": "learning_based_exploratory_investing",
                    "time_horizon_years": 3,
                    "return_preference": "balanced",
                    "volatility_comfort": 3,
                    "drawdown_tolerance": 3,
                    "investment_experience": "beginner",
                    "financial_literacy_level": "basic",
                    "current_holdings": [],
                },
                "learning-starter-basket",
            ),
        ]

        correct = 0
        for label, overrides, expected_top in scenarios:
            with self.subTest(label=label):
                result = self.evaluate(**overrides)
                actual_top = result["recommendations"][0]["recommendation_id"]
                self.assertEqual(actual_top, expected_top)
                correct += 1

        accuracy = correct / len(scenarios)
        self.assertGreaterEqual(accuracy, 1.0)

    def test_conservative_profile_rejects_high_risk_growth_basket(self):
        result = self.evaluate(
            financial_goal="short_term_savings",
            time_horizon_years=1,
            liquidity_needs="high",
            return_preference="steady",
            volatility_comfort=1,
            drawdown_tolerance=1,
            current_holdings=[],
            current_holdings_value=10000,
            liabilities=300000,
            emergency_fund_months=1,
        )

        rejected_ids = {item["recommendation_id"] for item in result["rejected_alternatives"]}
        self.assertIn("stock-growth-alpha", rejected_ids)

    def test_content_based_signal_is_visible_in_scored_output(self):
        result = self.evaluate(
            financial_goal="active_stock_selection",
            return_preference="high_upside",
            volatility_comfort=5,
            drawdown_tolerance=5,
            investment_experience="advanced",
            financial_literacy_level="advanced",
            current_holdings=[],
        )

        top = result["recommendations"][0]
        self.assertIn("content_match_score", top)
        self.assertGreaterEqual(top["content_match_score"], 70)
        self.assertEqual(result["preference_profile"]["preferred_asset_type"], "equity")


if __name__ == "__main__":
    unittest.main()
