def classify_item(item):
    text = " ".join([item.get("title", ""), item.get("summary", "")]).lower()

    if any(word in text for word in ["regulation", "policy", "law", "safety"]):
        return "policy_and_safety"
    if any(word in text for word in ["github", "open source", "repository"]):
        return "open_source"
    if any(word in text for word in ["model", "benchmark", "eval"]):
        return "models_and_research"
    if any(word in text for word in ["agent", "workflow", "automation"]):
        return "agents_and_products"
    return "general_ai"
