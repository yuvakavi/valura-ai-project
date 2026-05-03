from src.safety import check

def test_safe_query():
    result = check("How to invest in stocks?")
    assert result.blocked == False
import json
from src.safety import check


def test_safety_with_fixtures():
    with open("fixtures/test_queries/safety_pairs.json", encoding='utf-8-sig') as f:
        data = json.load(f)["pairs"]

    correct = 0

    for item in data:
        result = check(item["query"])

        if result.blocked == item["should_block"]:
            correct += 1

    accuracy = correct / len(data)

    print(f"\nSafety Accuracy: {accuracy}")

    assert accuracy >= 0.95