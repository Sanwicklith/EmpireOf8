from __future__ import annotations

from typing import Any, Dict, Optional

from .base_agent import BaseAgent


class FinanceAgent(BaseAgent):
    """
    Finance pillar agent.

    For this first MVP it works with a small in-memory snapshot of
    your chief aim, monthly surplus, and piggery projection.
    """

    name: str = "finance_agent"
    pillar: str = "finance"

    def __init__(self) -> None:
        # These values will later be replaced by live reads from the DB / dashboards.
        self._chief_aim: str = (
            "By the 17th of May 2026, I will be in full and legal possession "
            "of at least K1,000,000 ZMW in liquid or easily convertible assets."
        )

        # Current working estimate of surplus (ZMW / month).
        self._monthly_surplus: int = 34_800

        # High-level projection for the piggery business.
        self._piggery_projection: str = (
            "Projected gross revenue of approximately ZMW 1,500,000 from about "
            "500 piglets at ZMW 3,000 each in the first full cycle (around Apr–May 2026), "
            "with reinvestment planned into the next cycle."
        )

    async def handle(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        q = query.lower()

        # Chief Aim / goal queries
        if "chief aim" in q or "definite chief aim" in q or "goal" in q:
            return (
                "Finance Agent – Definite Chief Aim:\n\n"
                f"{self._chief_aim}\n\n"
                "Target date: 17 May 2026."
            )

        # Monthly surplus / cash-flow queries
        if "surplus" in q or "cash left" in q or "extra money" in q:
            return (
                "Finance Agent – Monthly Surplus:\n\n"
                f"Current working estimate is about ZMW {self._monthly_surplus:,.0f} "
                "per month in surplus, after fixed expenses."
            )

        # Piggery projection queries
        if "piggery" in q or "pig" in q:
            return (
                "Finance Agent – Piggery Projection:\n\n"
                f"{self._piggery_projection}"
            )

        # Default fallback for unrecognised finance questions (MVP stage)
        return (
            "Finance Agent here. I currently handle:\n"
            "- Your Definite Chief Aim in the finance pillar\n"
            "- Monthly surplus estimates\n"
            "- High-level piggery revenue projections\n\n"
            "Try asking about your 'chief aim', 'surplus', or 'piggery'."
        )
