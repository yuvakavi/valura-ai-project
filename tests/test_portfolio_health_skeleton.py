from src.agents.portfolio_health import run

def test_empty_portfolio():
    result = run({})
    assert "disclaimer" in result