from ..agents.portfolio_health import run as portfolio_run
from ..agents.stubs import stub_response


def route(agent_name: str, data: dict):
    """
    Routes request to correct agent
    """
    print(f"DEBUG ROUTER: agent_name={agent_name}, data={data}")

    if agent_name == "portfolio_health":
        user = data.get("user", {})
        print(f"DEBUG ROUTER: passing user={user} to portfolio_health")
        return portfolio_run(user)

    # All other agents (stub)
    return stub_response(agent_name, data)
