from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAgent(ABC):
    """
    Abstract base class for all pillar agents in the Empire of 8 mastermind engine.

    Every concrete agent must implement the `handle` method.
    """

    # Machine-friendly identifiers (can be overridden by subclasses)
    name: str = "base_agent"
    pillar: str = "generic"

    @abstractmethod
    async def handle(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Process a natural language query and return a response.

        :param query: The user / COA request in natural language.
        :param context: Optional shared context (financial snapshot, objectives, etc.).
        :return: A response string for now (can later evolve to a structured object).
        """
        raise NotImplementedError("Subclasses must implement `handle`.")
