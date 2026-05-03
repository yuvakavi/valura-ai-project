import sys
import os
from pathlib import Path

import pytest

# Add project root to sys.path so pytest can find src modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Change to project root so fixture paths work correctly
os.chdir(project_root)

# 🔹 Dummy LLM response (mock)
class DummyLLM:
    def generate(self, prompt):
        return {
            "agent": "portfolio_health",
            "entities": {}
        }


@pytest.fixture
def mock_llm():
    return DummyLLM()

