class BiasDetector:
    """Agent for detecting financial biases"""
    
    def __init__(self):
        self.bias_factors = []
    
    def detect_bias(self, data: dict) -> dict:
        """Analyze data for potential biases"""
        bias_score = 15
        factors = []

        if data.get("recent_trades", 0) >= 8 or data.get("portfolio_turnover") == "high":
            bias_score += 25
            factors.append("overconfidence")

        if data.get("panic_sell_history"):
            bias_score += 20
            factors.append("loss_aversion")

        if data.get("sector_concentration", 0) >= 0.35:
            bias_score += 15
            factors.append("confirmation_bias")

        if data.get("follows_trending_assets"):
            bias_score += 15
            factors.append("herding")

        if bias_score < 35:
            risk_level = "low"
        elif bias_score < 65:
            risk_level = "medium"
        else:
            risk_level = "high"

        return {
            "bias_score": bias_score,
            "risk_level": risk_level,
            "factors": factors
        }
    
    def generate_report(self, analysis: dict) -> str:
        """Generate bias analysis report"""
        return f"Bias Analysis: {analysis}"
