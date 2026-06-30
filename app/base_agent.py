from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any

from app.llm_client import call_openai


class BaseAgent(ABC):
    """
    Base class for LLM-powered agents.

    Responsibilities:
    - Build a prompt.
    - Call the LLM.
    - Parse the response.
    - Return structured output.

    Subclasses should own domain-specific prompt construction.
    """

    def run(self, **kwargs) -> Any:
        prompt = self.build_prompt(**kwargs)
        raw_response = call_openai(prompt)
        return self.parse_response(raw_response)

    @abstractmethod
    def build_prompt(self, **kwargs) -> str:
        raise NotImplementedError

    def parse_response(self, raw_response: str) -> Any:
        return raw_response.strip()

    @staticmethod
    def extract_json_object(text: str) -> dict[str, Any]:
        try:
            return json.loads(text)
        except Exception:
            pass

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            raise ValueError("No JSON object found in LLM response.")

        return json.loads(match.group(0))

    @staticmethod
    def extract_json_list(text: str) -> list[Any]:
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data
        except Exception:
            pass

        match = re.search(r"\[.*\]", text, re.DOTALL)

        if not match:
            raise ValueError("No JSON list found in LLM response.")

        return json.loads(match.group(0))