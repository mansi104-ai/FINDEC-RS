#!/usr/bin/env python
"""Test edge case validations and portfolio recommendations."""

from __future__ import annotations

import os
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from pydantic import ValidationError
from app.agents.recommender import Recommender
from app.schemas.suitability_schema import SuitabilityRequest
from app.services.asset_repository import DEFAULT_ASSET_SEED, init_db, replace_assets


def test_expense_validation():
    """Test that expenses cannot exceed income."""
    print("Testing expense validation...")
    
    try:
        request = SuitabilityRequest(
            age=35,
            income_level="medium",
            monthly_income=50000,
            monthly_expenses=60000,  # More than income - should fail
            income_stability="stable",
            investment_experience="intermediate",
            financial_literacy_level="moderate",
            current_holdings=[],
            current_holdings_value=100000,
            liabilities=50000,
            emergency_fund_months=3,
            financial_goal="long_term_wealth_creation",
            time_horizon_years=10,
            liquidity_needs="medium",
            return_expectations="balanced",
            volatility_comfort=3,
            drawdown_tolerance=3,
            return_preference="balanced",
        )
        print("  ❌ FAIL: Expected validation error but request was accepted")
        return False
    except ValidationError as e:
        print("  ✓ PASS: Validation error caught as expected")
        print(f"     Error: {e.errors()[0]['msg']}")
        return True


def test_portfolio_recommendations():
    """Test that portfolio recommendations are generated."""
    print("\nTesting portfolio recommendations generation...")
    
    db_path = BACKEND_ROOT / "tests" / "test_portfolios.db"
    os.environ["FINDEC_ASSET_DB"] = str(db_path)
    
    try:
        if db_path.exists():
            db_path.unlink()
        
        init_db()
        replace_assets(DEFAULT_ASSET_SEED)
        recommender = Recommender()
        
        payload = {
            "age": 32,
            "income_level": "medium",
            "monthly_income": 80000,
            "monthly_expenses": 40000,
            "income_stability": "stable",
            "investment_experience": "intermediate",
            "financial_literacy_level": "moderate",
            "current_holdings": [],
            "current_holdings_value": 150000,
            "liabilities": 100000,
            "emergency_fund_months": 4,
            "financial_goal": "long_term_wealth_creation",
            "time_horizon_years": 15,
            "liquidity_needs": "medium",
            "return_expectations": "balanced",
            "volatility_comfort": 4,
            "drawdown_tolerance": 3,
            "return_preference": "balanced",
        }
        
        result = recommender.generate_recommendations(payload)
        
        if "portfolio_recommendations" in result:
            portfolios = result["portfolio_recommendations"]
            print(f"  ✓ PASS: Generated {len(portfolios)} portfolio recommendations")
            
            for portfolio in portfolios:
                print(f"\n    Portfolio: {portfolio['portfolio_type']}")
                print(f"    Risk Level: {portfolio['risk_level']}")
                print(f"    Expected Return: {portfolio['expected_return']}")
                print(f"    Allocations:")
                for alloc in portfolio["allocations"]:
                    print(f"      - {alloc['asset_type']}: {alloc['percentage']}%")
            
            return True
        else:
            print("  ❌ FAIL: No portfolio recommendations in response")
            return False
    finally:
        os.environ.pop("FINDEC_ASSET_DB", None)
        if db_path.exists():
            try:
                db_path.unlink()
            except PermissionError:
                pass


def test_dynamic_weights():
    """Test that dynamic weights are applied based on user profile."""
    print("\nTesting dynamic weight application...")
    
    db_path = BACKEND_ROOT / "tests" / "test_weights.db"
    os.environ["FINDEC_ASSET_DB"] = str(db_path)
    
    try:
        if db_path.exists():
            db_path.unlink()
        
        init_db()
        replace_assets(DEFAULT_ASSET_SEED)
        recommender = Recommender()
        
        # Young investor with high savings
        young_payload = {
            "age": 28,
            "income_level": "high",
            "monthly_income": 100000,
            "monthly_expenses": 30000,
            "income_stability": "stable",
            "investment_experience": "intermediate",
            "financial_literacy_level": "moderate",
            "current_holdings": [],
            "current_holdings_value": 100000,
            "liabilities": 0,
            "emergency_fund_months": 6,
            "financial_goal": "long_term_wealth_creation",
            "time_horizon_years": 30,
            "liquidity_needs": "low",
            "return_expectations": "balanced",
            "volatility_comfort": 5,
            "drawdown_tolerance": 5,
            "return_preference": "high_upside",
        }
        
        # Older investor near retirement
        senior_payload = {
            "age": 62,
            "income_level": "high",
            "monthly_income": 100000,
            "monthly_expenses": 70000,
            "income_stability": "stable",
            "investment_experience": "advanced",
            "financial_literacy_level": "advanced",
            "current_holdings": [{"name": "Bonds", "sector": "debt", "value": 500000}],
            "current_holdings_value": 500000,
            "liabilities": 0,
            "emergency_fund_months": 12,
            "financial_goal": "retirement",
            "time_horizon_years": 5,
            "liquidity_needs": "high",
            "return_expectations": "steady",
            "volatility_comfort": 1,
            "drawdown_tolerance": 1,
            "return_preference": "steady",
        }
        
        young_result = recommender.generate_recommendations(young_payload)
        senior_result = recommender.generate_recommendations(senior_payload)
        
        young_top = young_result["recommendations"][0]
        senior_top = senior_result["recommendations"][0]
        
        print(f"\n  Young investor (28y, 70% savings rate):")
        print(f"    Top pick: {young_top['name']} (score: {young_top['suitability_score']})")
        print(f"    Risk band: {young_result['risk_profile']['final_risk_band']}")
        
        print(f"\n  Senior investor (62y, 30% savings rate):")
        print(f"    Top pick: {senior_top['name']} (score: {senior_top['suitability_score']})")
        print(f"    Risk band: {senior_result['risk_profile']['final_risk_band']}")
        
        # Verify that young investor got different recommendations
        if young_top['recommendation_id'] != senior_top['recommendation_id']:
            print(f"\n  ✓ PASS: Different recommendations for different profiles")
            return True
        else:
            print(f"\n  ❌ FAIL: Same recommendation for different profiles")
            return False
    finally:
        os.environ.pop("FINDEC_ASSET_DB", None)
        if db_path.exists():
            try:
                db_path.unlink()
            except PermissionError:
                pass


if __name__ == "__main__":
    print("=" * 50)
    print("Running Validation and Portfolio Tests")
    print("=" * 50)
    
    results = []
    results.append(("Expense Validation", test_expense_validation()))
    results.append(("Portfolio Recommendations", test_portfolio_recommendations()))
    results.append(("Dynamic Weights", test_dynamic_weights()))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    exit_code = 0 if passed == total else 1
    sys.exit(exit_code)
