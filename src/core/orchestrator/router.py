from __future__ import annotations

from core.agents.finance_agent import FinanceAgent
from core.orchestrator.chief import ChiefOrchestrator


def build_default_orchestrator() -> ChiefOrchestrator:
    """
    Factory function to construct the default orchestrator with
    the baseline set of pillar agents.

    For now, only the FinanceAgent is registered. As new pillars come online
    (Agriculture, Education, Technology, etc.), they will be added here.
    """
    finance_agent = FinanceAgent()

    agents = [
        finance_agent,
        # TODO: AgricultureAgent(), EducationAgent(), etc.
    ]

    return ChiefOrchestrator(agents=agents)
