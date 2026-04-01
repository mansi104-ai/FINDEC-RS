from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path


DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "findec.db"

DEFAULT_ASSET_SEED = [
    {
        "recommendation_id": "fund-balanced-income",
        "name": "Balanced Income Fund",
        "asset_type": "mutual_fund",
        "description": "Diversified income-oriented mutual fund for medium-term allocation.",
        "risk_level": "moderate",
        "risk_score": 52,
        "horizon": "medium",
        "liquidity": "medium",
        "goal_tags": ["retirement", "passive_investing", "long_term_wealth_creation"],
        "sector": "diversified",
        "return_style": "steady",
    },
    {
        "recommendation_id": "index-nifty-core",
        "name": "Nifty Core Index ETF",
        "asset_type": "etf",
        "description": "Core diversified index ETF for long-term passive allocation.",
        "risk_level": "moderate",
        "risk_score": 48,
        "horizon": "long",
        "liquidity": "high",
        "goal_tags": ["passive_investing", "long_term_wealth_creation", "retirement"],
        "sector": "diversified",
        "return_style": "market_tracking",
    },
    {
        "recommendation_id": "stock-growth-alpha",
        "name": "Growth Alpha Stock Basket",
        "asset_type": "equity",
        "description": "High-growth equity basket with concentrated upside potential.",
        "risk_level": "high",
        "risk_score": 81,
        "horizon": "long",
        "liquidity": "high",
        "goal_tags": ["active_stock_selection", "long_term_wealth_creation"],
        "sector": "technology",
        "return_style": "high_upside",
    },
    {
        "recommendation_id": "debt-short-shield",
        "name": "Short-Term Debt Shield Fund",
        "asset_type": "debt_fund",
        "description": "Short-duration debt fund for capital preservation and liquidity.",
        "risk_level": "low",
        "risk_score": 22,
        "horizon": "short",
        "liquidity": "high",
        "goal_tags": ["short_term_savings", "emergency_buffer"],
        "sector": "fixed_income",
        "return_style": "steady",
    },
    {
        "recommendation_id": "learning-starter-basket",
        "name": "Starter Learning Basket",
        "asset_type": "equity_basket",
        "description": "Guided starter basket for exploratory investing and learning.",
        "risk_level": "moderate",
        "risk_score": 58,
        "horizon": "medium",
        "liquidity": "medium",
        "goal_tags": ["learning_based_exploratory_investing", "active_stock_selection"],
        "sector": "diversified",
        "return_style": "blended",
    },
    {
        "recommendation_id": "dividend-stability-etf",
        "name": "Dividend Stability ETF",
        "asset_type": "etf",
        "description": "Income-focused ETF built around stable dividend-paying companies.",
        "risk_level": "moderate",
        "risk_score": 44,
        "horizon": "long",
        "liquidity": "high",
        "goal_tags": ["retirement", "passive_investing", "long_term_wealth_creation"],
        "sector": "diversified",
        "return_style": "steady",
    },
    {
        "recommendation_id": "bond-ladder-income",
        "name": "Bond Ladder Income Fund",
        "asset_type": "debt_fund",
        "description": "Income-oriented bond ladder for conservative investors needing stability.",
        "risk_level": "low",
        "risk_score": 28,
        "horizon": "medium",
        "liquidity": "medium",
        "goal_tags": ["retirement", "short_term_savings", "passive_investing"],
        "sector": "fixed_income",
        "return_style": "steady",
    },
    {
        "recommendation_id": "global-opportunity-fund",
        "name": "Global Opportunity Fund",
        "asset_type": "mutual_fund",
        "description": "International growth-oriented fund for diversified long-term wealth creation.",
        "risk_level": "high",
        "risk_score": 72,
        "horizon": "long",
        "liquidity": "medium",
        "goal_tags": ["long_term_wealth_creation", "active_stock_selection"],
        "sector": "diversified",
        "return_style": "high_upside",
    },
    {
        "recommendation_id": "tax-saver-equity-fund",
        "name": "Tax Saver Equity Fund",
        "asset_type": "mutual_fund",
        "description": "Tax-efficient equity fund suited for long-term disciplined investing.",
        "risk_level": "moderate",
        "risk_score": 60,
        "horizon": "long",
        "liquidity": "low",
        "goal_tags": ["retirement", "long_term_wealth_creation"],
        "sector": "diversified",
        "return_style": "blended",
    },
    {
        "recommendation_id": "gold-hedge-etf",
        "name": "Gold Hedge ETF",
        "asset_type": "etf",
        "description": "Precious-metals hedge ETF for capital protection and diversification.",
        "risk_level": "low",
        "risk_score": 34,
        "horizon": "medium",
        "liquidity": "high",
        "goal_tags": ["short_term_savings", "retirement", "passive_investing"],
        "sector": "commodities",
        "return_style": "steady",
    },
    {
        "recommendation_id": "sector-rotation-basket",
        "name": "Sector Rotation Basket",
        "asset_type": "equity_basket",
        "description": "Dynamic thematic basket for investors exploring active sector positioning.",
        "risk_level": "high",
        "risk_score": 76,
        "horizon": "medium",
        "liquidity": "medium",
        "goal_tags": ["active_stock_selection", "learning_based_exploratory_investing"],
        "sector": "industrials",
        "return_style": "high_upside",
    },
]


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(_get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def _get_db_path() -> str:
    return os.getenv("FINDEC_ASSET_DB", str(DEFAULT_DB_PATH))


def init_db() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                description TEXT DEFAULT '',
                risk_level TEXT NOT NULL DEFAULT 'moderate',
                risk_score REAL NOT NULL DEFAULT 0,
                horizon TEXT NOT NULL DEFAULT 'medium',
                liquidity TEXT NOT NULL DEFAULT 'medium',
                goal_tags TEXT NOT NULL,
                sector TEXT NOT NULL DEFAULT 'diversified',
                return_style TEXT NOT NULL DEFAULT 'balanced'
            )
            """
        )

        _sync_default_assets(connection)
        connection.commit()


def get_assets() -> list[dict]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT
                recommendation_id,
                name,
                asset_type,
                risk_level,
                risk_score,
                horizon,
                liquidity,
                goal_tags,
                sector,
                return_style
            FROM assets
            ORDER BY id
            """
        ).fetchall()

    return [
        {
            "id": row["recommendation_id"],
            "name": row["name"],
            "type": row["asset_type"],
            "risk_level": row["risk_level"],
            "risk_score": row["risk_score"],
            "horizon": row["horizon"],
            "liquidity": row["liquidity"],
            "goal_tags": json.loads(row["goal_tags"]),
            "sector": row["sector"],
            "return_style": row["return_style"],
        }
        for row in rows
    ]


def replace_assets(assets: list[dict]) -> None:
    with _connect() as connection:
        connection.execute("DELETE FROM assets")
        connection.executemany(
            """
            INSERT INTO assets (
                recommendation_id,
                name,
                asset_type,
                description,
                risk_level,
                risk_score,
                horizon,
                liquidity,
                goal_tags,
                sector,
                return_style
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    asset["recommendation_id"],
                    asset["name"],
                    asset["asset_type"],
                    asset.get("description", ""),
                    asset["risk_level"],
                    asset["risk_score"],
                    asset["horizon"],
                    asset["liquidity"],
                    json.dumps(asset["goal_tags"]),
                    asset["sector"],
                    asset["return_style"],
                )
                for asset in assets
            ],
        )
        connection.commit()


def _sync_default_assets(connection: sqlite3.Connection) -> None:
    connection.executemany(
        """
        INSERT INTO assets (
            recommendation_id,
            name,
            asset_type,
            description,
            risk_level,
            risk_score,
            horizon,
            liquidity,
            goal_tags,
            sector,
            return_style
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(recommendation_id) DO UPDATE SET
            name=excluded.name,
            asset_type=excluded.asset_type,
            description=excluded.description,
            risk_level=excluded.risk_level,
            risk_score=excluded.risk_score,
            horizon=excluded.horizon,
            liquidity=excluded.liquidity,
            goal_tags=excluded.goal_tags,
            sector=excluded.sector,
            return_style=excluded.return_style
        """,
        [
            (
                asset["recommendation_id"],
                asset["name"],
                asset["asset_type"],
                asset["description"],
                asset["risk_level"],
                asset["risk_score"],
                asset["horizon"],
                asset["liquidity"],
                json.dumps(asset["goal_tags"]),
                asset["sector"],
                asset["return_style"],
            )
            for asset in DEFAULT_ASSET_SEED
        ],
    )
