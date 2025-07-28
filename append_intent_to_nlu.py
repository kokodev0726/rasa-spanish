import yaml

def append_intent(intent_name, examples):
    file = "data/nlu.yml"
    with open(file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for intent in data.get("nlu", []):
        if intent["intent"] == intent_name:
            return  # Already exists

    formatted_examples = "\n".join([f"- {ex}" for ex in examples])
    data["nlu"].append({"intent": intent_name, "examples": formatted_examples})

    with open(file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)