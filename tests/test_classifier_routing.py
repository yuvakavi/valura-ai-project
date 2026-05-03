import json
from src.classifier import classify


def test_classifier_with_fixtures():
    with open("fixtures/test_queries/intent_classification.json", encoding='utf-8-sig') as f:
        data = json.load(f)["queries"]

    correct = 0

    for item in data:
        result = classify(item["query"])
        if result.agent == item["expected_agent"]:
            correct += 1

    accuracy = correct / len(data)

    print(f"\nAccuracy: {accuracy}")

    assert accuracy >= 0.85