from __future__ import annotations

from statistics import mean
from typing import Any

from app.services.asset_repository import get_assets


class SuitabilityEngine:
    """Rule-based suitability engine for recommendation scoring."""

    def evaluate(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized_profile = self._build_user_profile(payload)
        goal_context = self._map_goal_and_horizon(payload)
        risk_context = self._assess_risk(payload, normalized_profile, goal_context)
        preference_profile = self._build_preference_profile(payload, normalized_profile, goal_context, risk_context)
        asset_universe = get_assets()

        recommendations = [
            self._score_asset(asset, normalized_profile, goal_context, risk_context, preference_profile)
            for asset in asset_universe
        ]

        accepted = [item for item in recommendations if item["suitability_label"] != "low_fit"]
        rejected = [item for item in recommendations if item["suitability_label"] == "low_fit"]
        accepted.sort(key=lambda item: item["suitability_score"], reverse=True)
        rejected.sort(key=lambda item: item["suitability_score"], reverse=True)

        portfolio_recommendations = self._generate_portfolio_recommendations(
            normalized_profile, goal_context, risk_context, preference_profile
        )

        return {
            "normalized_user_profile": normalized_profile,
            "goal_context": goal_context,
            "risk_profile": risk_context,
            "preference_profile": preference_profile,
            "recommendations": accepted,
            "rejected_alternatives": [
                {
                    "recommendation_id": item["recommendation_id"],
                    "name": item["name"],
                    "reason": item["explanation_summary"],
                }
                for item in rejected
            ],
            "portfolio_recommendations": portfolio_recommendations,
            "engine_summary": self._build_engine_summary(accepted, rejected, risk_context),
        }

    def _build_user_profile(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            monthly_income = max(float(payload.get("monthly_income", 0)), 0.0)
            monthly_expenses = max(float(payload.get("monthly_expenses", 0)), 0.0)
            emergency_months = max(float(payload.get("emergency_fund_months", 0)), 0.0)
            liabilities = max(float(payload.get("liabilities", 0)), 0.0)
            holdings_value = max(float(payload.get("current_holdings_value", 0)), 0.0)
        except (ValueError, TypeError):
            monthly_income = 0.0
            monthly_expenses = 0.0
            emergency_months = 0.0
            liabilities = 0.0
            holdings_value = 0.0

        # Ensure emergency_months is reasonable (0-120 months = 10 years max)
        emergency_months = min(emergency_months, 120.0)
        
        savings_capacity = max(monthly_income - monthly_expenses, 0.0)
        savings_rate = (savings_capacity / monthly_income) if monthly_income > 0 else 0.0
        savings_rate = min(savings_rate, 1.0)  # Cap at 100%
        
        # Debt to income ratio - cap at reasonable maximum to prevent extreme values
        if monthly_income > 0:
            debt_to_income = min(liabilities / (monthly_income * 12), 10.0)
        else:
            debt_to_income = 1.0

        profile_score = mean(
            [
                self._score_income_stability(payload.get("income_stability", "variable")),
                min(savings_rate * 100, 100),
                min((emergency_months / 6) * 100, 100),
                max(0, min(100 - (debt_to_income * 100), 100)),  # Bound to 0-100
                self._score_experience(payload.get("investment_experience", "beginner")),
                self._score_literacy(payload.get("financial_literacy_level", "basic")),
            ]
        )

        return {
            "age": int(payload.get("age", 30)),
            "income_level": payload.get("income_level", "medium"),
            "income_stability": payload.get("income_stability", "variable"),
            "monthly_savings_capacity": round(savings_capacity, 2),
            "savings_rate": round(min(savings_rate, 1.0), 2),
            "investment_experience": payload.get("investment_experience", "beginner"),
            "financial_literacy_level": payload.get("financial_literacy_level", "basic"),
            "current_holdings": payload.get("current_holdings", []) or [],
            "current_holdings_value": holdings_value,
            "liabilities": liabilities,
            "debt_to_income_ratio": round(min(debt_to_income, 10.0), 2),
            "emergency_fund_months": round(emergency_months, 1),
            "profile_strength_score": round(min(profile_score, 100.0), 2),
        }

    def _map_goal_and_horizon(self, payload: dict[str, Any]) -> dict[str, Any]:
        time_horizon_years = float(payload.get("time_horizon_years", 3))
        liquidity_needs = payload.get("liquidity_needs", "medium")

        if time_horizon_years < 2:
            horizon_bucket = "short"
        elif time_horizon_years < 5:
            horizon_bucket = "medium"
        else:
            horizon_bucket = "long"

        liquidity_score_map = {"low": 25, "medium": 55, "high": 85}
        return {
            "goal_category": payload.get("financial_goal", "long_term_wealth_creation"),
            "horizon_bucket": horizon_bucket,
            "target_time_horizon_years": time_horizon_years,
            "liquidity_sensitivity_score": liquidity_score_map.get(liquidity_needs, 55),
            "return_expectations": payload.get("return_expectations", "balanced"),
        }

    def _assess_risk(
        self,
        payload: dict[str, Any],
        profile: dict[str, Any],
        goal_context: dict[str, Any],
    ) -> dict[str, Any]:
        # Calculate risk capacity score with safe division
        emergency_fund_score = min((profile["emergency_fund_months"] / 6) * 100, 100) if profile["emergency_fund_months"] > 0 else 0
        holdings_score = min((profile["current_holdings_value"] / 100000) * 100, 100) if profile["current_holdings_value"] > 0 else 0
        debt_score = max(0, min(100 - (profile["debt_to_income_ratio"] * 100), 100))
        
        risk_capacity_score = mean(
            [
                self._score_income_stability(profile["income_stability"]),
                emergency_fund_score,
                holdings_score,
                debt_score,
                100 - goal_context["liquidity_sensitivity_score"],
            ]
        )
        
        # Bound risk capacity score to 0-100
        risk_capacity_score = max(0, min(risk_capacity_score, 100))

        risk_tolerance_score = mean(
            [
                self._map_scale(payload.get("volatility_comfort", 3)),
                self._map_scale(payload.get("drawdown_tolerance", 3)),
                self._score_return_preference(payload.get("return_preference", "balanced")),
            ]
        )
        
        # Bound risk tolerance score to 0-100
        risk_tolerance_score = max(0, min(risk_tolerance_score, 100))

        combined = round(risk_capacity_score * 0.55 + risk_tolerance_score * 0.45, 2)
        combined = max(0, min(combined, 100))  # Ensure 0-100 range
        
        if combined < 40:
            risk_band = "conservative"
        elif combined < 70:
            risk_band = "moderate"
        else:
            risk_band = "aggressive"

        return {
            "risk_capacity_score": round(max(0, min(risk_capacity_score, 100)), 2),
            "risk_tolerance_score": round(max(0, min(risk_tolerance_score, 100)), 2),
            "final_risk_band": risk_band,
        }

    def _calculate_dynamic_weights(
        self,
        profile: dict[str, Any],
        goal_context: dict[str, Any],
        risk_context: dict[str, Any],
    ) -> dict[str, float]:
        """Calculate dynamic weights based on user profile characteristics.
        
        Different factors carry different importance for different people:
        - Young users with stable income: Higher weight on risk_alignment and content_match
        - Older users: Higher weight on goal_match and stability factors
        - High-experience users: Higher weight on content_match
        - High-debt users: Higher weight on goal_match and liquidity_match
        - Conservative profiles: Higher weight on goal_match and liquidity_match
        """
        age = profile["age"]
        experience = profile["investment_experience"]
        debt_to_income = profile["debt_to_income_ratio"]
        savings_rate = profile["savings_rate"]
        emergency_funds = profile["emergency_fund_months"]
        risk_band = risk_context["final_risk_band"]
        
        # Start with baseline weights
        weights = {
            "goal_match": 0.23,
            "horizon_match": 0.14,
            "liquidity_match": 0.12,
            "risk_alignment": 0.24,
            "content_match": 0.19,
            "concentration": 0.08,
        }
        
        # Adjustment for age
        if age < 35:
            # Young users: can afford more risk, emphasize growth potential
            weights["risk_alignment"] += 0.08
            weights["content_match"] += 0.05
            weights["goal_match"] -= 0.05
            weights["liquidity_match"] -= 0.08
        elif age > 55:
            # Near/at retirement: preserve capital, emphasize stability
            weights["goal_match"] += 0.08
            weights["liquidity_match"] += 0.05
            weights["risk_alignment"] -= 0.05
            weights["content_match"] -= 0.08
        
        # Adjustment for experience level
        if experience == "advanced":
            weights["content_match"] += 0.06
            weights["goal_match"] -= 0.03
            weights["horizon_match"] -= 0.03
        elif experience == "beginner":
            weights["goal_match"] += 0.05
            weights["liquidity_match"] += 0.04
            weights["content_match"] -= 0.06
            weights["concentration"] -= 0.03
        
        # Adjustment for debt burden
        if debt_to_income > 0.5:
            # High debt: need to be more careful with risk
            weights["goal_match"] += 0.06
            weights["liquidity_match"] += 0.04
            weights["risk_alignment"] -= 0.05
            weights["content_match"] -= 0.05
        
        # Adjustment for savings capacity
        if savings_rate > 0.4:
            # High savings: can take on more investment risk
            weights["risk_alignment"] += 0.04
            weights["content_match"] += 0.03
            weights["liquidity_match"] -= 0.07
        elif savings_rate < 0.1:
            # Low savings: need liquid, safe investments
            weights["liquidity_match"] += 0.08
            weights["goal_match"] += 0.03
            weights["risk_alignment"] -= 0.06
            weights["content_match"] -= 0.05
        
        # Adjustment for emergency fund status
        if emergency_funds < 2:
            weights["liquidity_match"] += 0.08
            weights["risk_alignment"] -= 0.06
        elif emergency_funds > 6:
            weights["risk_alignment"] += 0.05
            weights["liquidity_match"] -= 0.04
        
        # Adjustment for conservative risk band
        if risk_band == "conservative":
            weights["goal_match"] += 0.05
            weights["liquidity_match"] += 0.03
            weights["risk_alignment"] -= 0.04
            weights["content_match"] -= 0.04
        elif risk_band == "aggressive":
            weights["risk_alignment"] += 0.05
            weights["content_match"] += 0.04
            weights["goal_match"] -= 0.04
            weights["liquidity_match"] -= 0.05
        
        # Normalize weights to sum to 1.0
        total = sum(weights.values())
        normalized = {k: v / total for k, v in weights.items()}
        
        return normalized

    def _score_asset(
        self,
        asset: dict[str, Any],
        profile: dict[str, Any],
        goal_context: dict[str, Any],
        risk_context: dict[str, Any],
        preference_profile: dict[str, Any],
    ) -> dict[str, Any]:
        rationale_factors = []
        risk_warnings = []

        goal_match = 100 if goal_context["goal_category"] in asset["goal_tags"] else 45
        if goal_match == 100:
            rationale_factors.append("Matches the stated investment goal.")
        else:
            risk_warnings.append("Goal alignment is limited for this recommendation.")

        horizon_match = 100 if goal_context["horizon_bucket"] == asset["horizon"] else 55
        if horizon_match == 100:
            rationale_factors.append("Fits the target investment horizon.")
        else:
            risk_warnings.append("Time horizon fit is only partial.")

        liquidity_match = self._score_liquidity_match(
            goal_context["liquidity_sensitivity_score"], asset["liquidity"]
        )
        if liquidity_match >= 70:
            rationale_factors.append("Liquidity needs stay within a manageable range.")
        else:
            risk_warnings.append("Liquidity needs may clash with the asset profile.")

        risk_alignment = self._score_risk_alignment(asset["risk_score"], risk_context["final_risk_band"])
        if risk_alignment >= 75:
            rationale_factors.append("Risk level stays within the investor's risk band.")
        else:
            risk_warnings.append("Risk level stretches the investor's current capacity.")

        concentration_penalty = self._sector_penalty(asset, profile["current_holdings"])
        if concentration_penalty > 0:
            risk_warnings.append("Adds concentration to an already represented sector.")
        else:
            rationale_factors.append("Does not materially worsen sector concentration.")

        content_match_score = self._score_content_match(asset, preference_profile)
        if content_match_score >= 75:
            rationale_factors.append("Asset features are closely aligned with the investor preference profile.")
        elif content_match_score < 50:
            risk_warnings.append("Asset characteristics are only weakly aligned with learned user preferences.")

        # Get dynamic weights based on user profile
        weights = self._calculate_dynamic_weights(profile, goal_context, risk_context)
        
        suitability_score = round(
            goal_match * weights["goal_match"]
            + horizon_match * weights["horizon_match"]
            + liquidity_match * weights["liquidity_match"]
            + risk_alignment * weights["risk_alignment"]
            + content_match_score * weights["content_match"]
            + (100 - concentration_penalty) * weights["concentration"],
            2,
        )

        if suitability_score >= 75:
            label = "high_fit"
        elif suitability_score >= 55:
            label = "medium_fit"
        else:
            label = "low_fit"

        explanation_summary = self._build_explanation(asset, goal_context, risk_context, label, risk_warnings)
        confidence_score = round(
            min(
                0.98,
                (
                    profile["profile_strength_score"] / 100 * 0.45
                    + suitability_score / 100 * 0.45
                    + (1 - min(len(risk_warnings), 3) * 0.1)
                ) * 0.55,
            ),
            2,
        )

        next_best_action = (
            "Proceed with a gradual allocation and monitor portfolio balance."
            if label == "high_fit"
            else "Review goal, liquidity, and risk constraints before allocating more capital."
        )

        if not risk_warnings:
            risk_warnings.append("No immediate suitability warning identified by the current rule set.")

        return {
            "recommendation_id": asset["id"],
            "name": asset["name"],
            "asset_type": asset["type"],
            "suitability_score": suitability_score,
            "suitability_label": label,
            "explanation_summary": explanation_summary,
            "risk_warnings": risk_warnings,
            "confidence_score": confidence_score,
            "content_match_score": round(content_match_score, 2),
            "rationale_factors": rationale_factors,
            "next_best_action": next_best_action,
        }

    def _build_preference_profile(
        self,
        payload: dict[str, Any],
        profile: dict[str, Any],
        goal_context: dict[str, Any],
        risk_context: dict[str, Any],
    ) -> dict[str, Any]:
        experience = profile["investment_experience"]
        if experience == "beginner":
            complexity_preference = "simple"
        elif experience == "advanced":
            complexity_preference = "advanced"
        else:
            complexity_preference = "moderate"

        diversification_preference = (
            "high"
            if profile["financial_literacy_level"] == "basic" or risk_context["final_risk_band"] == "conservative"
            else "medium"
        )

        return {
            "preferred_goal": goal_context["goal_category"],
            "preferred_horizon": goal_context["horizon_bucket"],
            "preferred_liquidity": goal_context["liquidity_sensitivity_score"],
            "preferred_return_style": payload.get("return_preference", "balanced"),
            "preferred_asset_type": self._preferred_asset_type(goal_context["goal_category"], risk_context["final_risk_band"]),
            "complexity_preference": complexity_preference,
            "diversification_preference": diversification_preference,
        }

    def _build_engine_summary(
        self,
        accepted: list[dict[str, Any]],
        rejected: list[dict[str, Any]],
        risk_context: dict[str, Any],
    ) -> str:
        top_pick = accepted[0]["name"] if accepted else "No recommendation"
        return (
            f"Engine finished with a {risk_context['final_risk_band']} risk band. "
            f"Top current fit: {top_pick}. Rejected alternatives: {len(rejected)}."
        )

    def _build_explanation(
        self,
        asset: dict[str, Any],
        goal_context: dict[str, Any],
        risk_context: dict[str, Any],
        label: str,
        risk_warnings: list[str],
    ) -> str:
        if label == "high_fit":
            return (
                f"{asset['name']} is suitable because it matches the {goal_context['goal_category']} goal, "
                f"fits a {risk_context['final_risk_band']} risk profile, and stays aligned with the planned horizon."
            )
        return (
            f"{asset['name']} is less suitable because it creates one or more mismatches across goal, "
            f"risk, or liquidity constraints. Main concern: {risk_warnings[0]}"
        )

    def _score_income_stability(self, income_stability: str) -> float:
        return {"low": 30, "variable": 50, "medium": 65, "high": 85, "stable": 85}.get(
            income_stability, 50
        )

    def _score_experience(self, experience: str) -> float:
        return {"beginner": 35, "intermediate": 65, "advanced": 85}.get(experience, 35)

    def _score_literacy(self, literacy: str) -> float:
        return {"basic": 35, "moderate": 65, "advanced": 85}.get(literacy, 35)

    def _map_scale(self, value: Any) -> float:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            numeric = 3.0
        bounded = min(max(numeric, 1.0), 5.0)
        return (bounded - 1) / 4 * 100

    def _score_return_preference(self, preference: str) -> float:
        return {"steady": 30, "balanced": 60, "high_upside": 85}.get(preference, 60)

    def _score_content_match(self, asset: dict[str, Any], preference_profile: dict[str, Any]) -> float:
        goal_similarity = 100 if preference_profile["preferred_goal"] in asset["goal_tags"] else 35
        horizon_similarity = 100 if preference_profile["preferred_horizon"] == asset["horizon"] else 50
        return_style_similarity = self._return_style_similarity(
            preference_profile["preferred_return_style"], asset["return_style"]
        )
        asset_type_similarity = self._asset_type_similarity(
            preference_profile["preferred_asset_type"], asset["type"]
        )
        diversification_similarity = self._diversification_similarity(
            preference_profile["diversification_preference"], asset["sector"]
        )

        return round(
            goal_similarity * 0.30
            + horizon_similarity * 0.20
            + return_style_similarity * 0.20
            + asset_type_similarity * 0.20
            + diversification_similarity * 0.10,
            2,
        )

    def _preferred_asset_type(self, goal_category: str, risk_band: str) -> str:
        if goal_category in {"short_term_savings", "emergency_buffer"}:
            return "debt_fund"
        if goal_category == "passive_investing":
            return "etf"
        if goal_category == "active_stock_selection":
            return "equity" if risk_band == "aggressive" else "equity_basket"
        if goal_category == "learning_based_exploratory_investing":
            return "equity_basket"
        return "mutual_fund" if risk_band == "conservative" else "etf"

    def _return_style_similarity(self, preferred: str, asset_style: str) -> float:
        if preferred == "steady":
            return {"steady": 100, "market_tracking": 65, "blended": 60, "high_upside": 30}.get(asset_style, 50)
        if preferred == "high_upside":
            return {"high_upside": 100, "blended": 75, "market_tracking": 60, "steady": 35}.get(asset_style, 55)
        return {"blended": 90, "market_tracking": 85, "steady": 70, "high_upside": 70}.get(asset_style, 65)

    def _asset_type_similarity(self, preferred: str, asset_type: str) -> float:
        if preferred == asset_type:
            return 100
        related = {
            "mutual_fund": {"etf": 75, "debt_fund": 65},
            "etf": {"mutual_fund": 75, "equity_basket": 60},
            "equity": {"equity_basket": 80, "etf": 55},
            "equity_basket": {"equity": 80, "etf": 60},
            "debt_fund": {"mutual_fund": 65},
        }
        return related.get(preferred, {}).get(asset_type, 40)

    def _diversification_similarity(self, preference: str, sector: str) -> float:
        if preference == "high":
            return 100 if sector == "diversified" else 45
        return 85 if sector == "diversified" else 70

    def _score_liquidity_match(self, liquidity_sensitivity: int, asset_liquidity: str) -> float:
        asset_scores = {"low": 25, "medium": 60, "high": 90}
        return max(0, 100 - abs(liquidity_sensitivity - asset_scores.get(asset_liquidity, 60)))

    def _score_risk_alignment(self, asset_risk_score: int, risk_band: str) -> float:
        band_target = {"conservative": 25, "moderate": 55, "aggressive": 80}
        return max(0, 100 - abs(asset_risk_score - band_target.get(risk_band, 55)) * 1.4)

    def _sector_penalty(self, asset: dict[str, Any], holdings: list[dict[str, Any]]) -> int:
        if asset["sector"] == "diversified":
            return 0
        sector_matches = sum(1 for holding in holdings if holding.get("sector") == asset["sector"])
        return min(sector_matches * 25, 75)

    def _generate_portfolio_recommendations(
        self,
        profile: dict[str, Any],
        goal_context: dict[str, Any],
        risk_context: dict[str, Any],
        preference_profile: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Generate dynamic portfolio recommendations based on user profile."""
        risk_band = risk_context["final_risk_band"]
        age = profile["age"]
        time_horizon = goal_context["target_time_horizon_years"]
        savings_rate = profile["savings_rate"]
        
        recommendations = []
        
        # Generate age-appropriate portfolio
        if age < 40 and time_horizon > 5:
            recommendations.append(self._create_portfolio(
                "growth_oriented",
                "8-12% annually",
                "high",
                [
                    ("equity", 70, "High growth potential for long-term wealth building"),
                    ("debt_fund", 20, "Stable income and portfolio balancing"),
                    ("alternatives", 10, "Diversification and inflation protection"),
                ],
                "Ideal for young investors with long time horizons who can tolerate volatility"
            ))
        
        # Generate balanced portfolio
        recommendations.append(self._create_portfolio(
            "balanced",
            "6-8% annually",
            "moderate",
            [
                ("equity", 50, "Capital growth component"),
                ("debt_fund", 35, "Income and stability"),
                ("alternatives", 15, "Diversification and inflation hedge"),
            ],
            "Suitable for most investors seeking a balance between growth and stability"
        ))
        
        # Generate conservative portfolio
        if risk_band in ("conservative", "moderate") or age > 50:
            recommendations.append(self._create_portfolio(
                "capital_preservation",
                "4-5% annually",
                "low",
                [
                    ("debt_fund", 60, "Principal preservation focus"),
                    ("equity", 25, "Limited growth exposure"),
                    ("alternatives", 15, "Inflation protection"),
                ],
                "Focuses on preserving capital with modest growth potential"
            ))
        
        # Generate income-focused portfolio if high liquidity needs
        if goal_context["liquidity_sensitivity_score"] > 70:
            recommendations.append(self._create_portfolio(
                "income_focused",
                "4-6% annually",
                "low-moderate",
                [
                    ("debt_fund", 50, "Regular dividend/interest income"),
                    ("equity", 30, "Dividend-paying stocks and funds"),
                    ("alternatives", 20, "Real assets and yield generation"),
                ],
                "Emphasizes current income generation and liquidity"
            ))
        
        # Generate aggressive portfolio if high savings rate and young age
        if savings_rate > 0.3 and age < 45 and time_horizon > 7:
            recommendations.append(self._create_portfolio(
                "aggressive_growth",
                "12-15% annually",
                "very high",
                [
                    ("equity", 85, "Maximum growth exposure"),
                    ("alternatives", 15, "Emerging markets and high-growth sectors"),
                ],
                "Maximum growth focus for investors comfortable with significant volatility"
            ))
        
        return recommendations

    def _create_portfolio(
        self,
        portfolio_type: str,
        expected_return: str,
        risk_level: str,
        allocations: list[tuple[str, float, str]],
        description: str,
    ) -> dict[str, Any]:
        """Helper method to create portfolio recommendation objects."""
        return {
            "portfolio_type": portfolio_type,
            "expected_return": expected_return,
            "risk_level": risk_level,
            "allocations": [
                {
                    "asset_type": asset_type,
                    "percentage": percentage,
                    "rationale": rationale,
                }
                for asset_type, percentage, rationale in allocations
            ],
            "description": description,
            "suitable_for": self._determine_suitable_profiles(portfolio_type),
        }

    def _determine_suitable_profiles(self, portfolio_type: str) -> list[str]:
        """Determine which investor profiles are suitable for each portfolio type."""
        profiles = {
            "growth_oriented": ["young_investor", "long_horizon", "risk_tolerant", "growth_focused"],
            "balanced": ["moderate_investor", "diversification_seeking", "moderate_risk"],
            "capital_preservation": ["conservative", "near_retirement", "risk_averse", "stability_focused"],
            "income_focused": ["income_seeking", "high_liquidity_needs", "retiree"],
            "aggressive_growth": ["high_risk_tolerance", "young", "high_savings_rate", "maximum_growth"],
        }
        return profiles.get(portfolio_type, ["general_investor"])
