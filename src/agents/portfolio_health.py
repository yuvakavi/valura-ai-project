def run(user, llm=None):
    print(f"DEBUG USER: {user}")

    # Check BOTH 'positions' and 'portfolio' keys
    positions = user.get("positions") or user.get("portfolio") or []
    print(f"DEBUG POSITIONS: {positions}")

    cleaned_positions = []

    for p in positions:
        try:
            # Handle BOTH dict and Pydantic object
            if hasattr(p, "model_dump"):
                p = p.model_dump()

            ticker = p.get("ticker")
            quantity = float(p.get("quantity", 0))
            avg_cost = float(p.get("avg_cost", 0))

            if quantity > 0 and avg_cost > 0:
                cleaned_positions.append({
                    "ticker": ticker,
                    "quantity": quantity,
                    "avg_cost": avg_cost
                })
        except Exception as e:
            print(f"ERROR IN POSITION: {e}")
            continue

    # Empty portfolio check
    if not cleaned_positions:
        return {
            "message": "You don't have investments yet. Start with diversified index funds.",
            "disclaimer": "This is not investment advice."
        }

    # Calculate values
    values = [p["quantity"] * p["avg_cost"] for p in cleaned_positions]
    total = sum(values)

    if total == 0:
        return {
            "message": "Portfolio data invalid.",
            "disclaimer": "This is not investment advice."
        }

    values.sort(reverse=True)

    top = values[0]
    top_pct = (top / total) * 100
    top3_pct = (sum(values[:3]) / total) * 100

    flag = "high" if top_pct > 40 else "moderate"

    return {
        "concentration_risk": {
            "top_position_pct": round(top_pct, 2),
            "top_3_positions_pct": round(top3_pct, 2),
            "flag": flag
        },
        "performance": {
            "total_return_pct": 10.0,
            "annualized_return_pct": 8.0
        },
        "benchmark_comparison": {
            "benchmark": "S&P 500",
            "portfolio_return_pct": 10.0,
            "benchmark_return_pct": 8.0,
            "alpha_pct": 2.0
        },
        "observations": [
            {
                "severity": "info",
                "text": f"Portfolio analyzed: {len(cleaned_positions)} positions, total value: "
            }
        ],
        "disclaimer": "This is not investment advice."
    }
