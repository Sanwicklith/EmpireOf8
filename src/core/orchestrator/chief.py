from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.agents.base_agent import BaseAgent


class ChiefOrchestrator:
    """
    Central orchestrator for the Empire of 8 mastermind engine.

    - Receives natural language queries
    - Selects the most suitable pillar agent (for now: Finance)
    - Delegates work and returns the agent's response
    """

    def __init__(self, agents: List[BaseAgent]) -> None:
        self._agents: List[BaseAgent] = agents
        # Index by pillar for quick lookup (e.g. "finance", "agriculture", etc.)
        self._agents_by_pillar: Dict[str, BaseAgent] = {
            agent.pillar: agent for agent in agents
        }

    async def handle(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        preferred_pillar: Optional[str] = None,
    ) -> str:
        """
        Entry point for handling any request coming from the API / UI.

        :param query: Natural language query or instruction.
        :param context: Optional shared context (user id, timeframe, etc.).
        :param preferred_pillar: Explicit pillar hint (e.g. 'finance').
        """
        context = context or {}

        agent = self._select_agent(query=query, preferred_pillar=preferred_pillar)

        if agent is None:
            # Later we can forward this to a generic LLM / fallback agent.
            return (
                "Orchestrator: No suitable pillar agent is available yet for this "
                "type of request. At this stage only the Finance agent is wired in."
            )

        # In future we can add policy checks, logging, etc. around this call.
        return await agent.handle(query=query, context=context)

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    def _select_agent(
        self,
        query: str,
        preferred_pillar: Optional[str] = None,
    ) -> Optional[BaseAgent]:
        """
        Very simple routing logic for the first version of the mastermind.
        """

        # 1. If the caller has specified a pillar explicitly, honour that.
        if preferred_pillar:
            agent = self._agents_by_pillar.get(preferred_pillar)
            if agent is not None:
                return agent

        q = query.lower()

        # 2. Finance related keywords
        finance_keywords = [
            "finance",
            "money",
            "budget",
            "surplus",
            "cash",
            "piggery",
            "pig",
            "income",
            "expenses",
        ]

        # chief aim / goal style queries are also finance pillar for now
        finance_intent_keywords = [
            "chief aim",
            "definite chief aim",
            "goal",
            "target",
            "million",
            "1,000,000",
            "k1,000,000",
        ]

        if any(kw in q for kw in finance_keywords) or any(
            phrase in q for phrase in finance_intent_keywords
        ):
            return self._agents_by_pillar.get("finance")

        # 3. If there is only one agent registered, default to that agent
        if len(self._agents_by_pillar) == 1:
            return next(iter(self._agents_by_pillar.values()))

        # 4. No match – no agent selected.
        return None

