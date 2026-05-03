def stub_response(agent, data):
    return {
        "message": f"{agent} not implemented",
        "intent": data.get("intent"),
        "entities": data.get("entities"),
        "agent": agent
    }
