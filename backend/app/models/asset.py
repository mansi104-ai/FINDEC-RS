from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String

from app.db import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    asset_type = Column(String, nullable=False)
    description = Column(String, default="")
    risk_level = Column(String, nullable=False, default="moderate")
    risk_score = Column(Float, default=0.0)
    horizon = Column(String, nullable=False, default="medium")
    liquidity = Column(String, nullable=False, default="medium")
    goal_tags = Column(JSON, nullable=False, default=list)
    sector = Column(String, nullable=False, default="diversified")
    return_style = Column(String, nullable=False, default="balanced")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_engine_payload(self) -> dict:
        return {
            "id": self.recommendation_id,
            "name": self.name,
            "type": self.asset_type,
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "horizon": self.horizon,
            "liquidity": self.liquidity,
            "goal_tags": list(self.goal_tags or []),
            "sector": self.sector,
            "return_style": self.return_style,
        }

    def __repr__(self):
        return f"<Asset(id={self.id}, recommendation_id={self.recommendation_id}, name={self.name})>"
