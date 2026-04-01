from __future__ import annotations

import os
import sys
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


SCENARIOS = [
    (
        "Passive Long-Term",
        {
            "financial_goal": "passive_investing",
            "time_horizon_years": 12,
            "return_preference": "balanced",
            "liquidity_needs": "medium",
        },
        "index-nifty-core",
    ),
    (
        "Short-Term Capital Preservation",
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
        "Aggressive Active Investor",
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
        "Learning Explorer",
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


def main() -> None:
    db_path = BACKEND_ROOT / "scripts" / "evaluation_findec.db"
    os.environ["FINDEC_ASSET_DB"] = str(db_path)

    try:
        if db_path.exists():
            db_path.unlink()

        init_db()
        replace_assets(DEFAULT_ASSET_SEED)
        recommender = Recommender()

        correct = 0

        print("Recommendation Quality Evaluation")
        print("=" * 36)

        for label, overrides, expected_top in SCENARIOS:
            result = recommender.generate_recommendations(make_payload(**overrides))
            top = result["recommendations"][0]
            actual_top = top["recommendation_id"]
            is_correct = actual_top == expected_top
            if is_correct:
                correct += 1

            print(f"\nScenario: {label}")
            print(f"Expected top: {expected_top}")
            print(f"Actual top:   {actual_top}")
            print(f"Suitability:  {top['suitability_score']:.2f}")
            print(f"Content fit:  {top['content_match_score']:.2f}")
            print(f"Risk band:    {result['risk_profile']['final_risk_band']}")
            print(f"Status:       {'PASS' if is_correct else 'FAIL'}")
            print("Top 3:")
            for item in result["recommendations"][:3]:
                print(
                    f"  - {item['recommendation_id']}: "
                    f"score={item['suitability_score']:.2f}, "
                    f"content={item['content_match_score']:.2f}, "
                    f"label={item['suitability_label']}"
                )

        accuracy = correct / len(SCENARIOS)
        print("\nSummary")
        print("-" * 36)
        print(f"Top-1 benchmark accuracy: {accuracy:.2%}")
        print(f"Scenarios passed: {correct}/{len(SCENARIOS)}")
    finally:
        os.environ.pop("FINDEC_ASSET_DB", None)
        if db_path.exists():
            try:
                db_path.unlink()
            except PermissionError:
                pass


if __name__ == "__main__":
    main()
