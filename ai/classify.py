def classify_item(item):
    text = " ".join([
        item.get("source", ""),
        item.get("title", ""),
        item.get("summary", ""),
    ]).lower()

    if any(word in text for word in ["openai", "chatgpt", "gpt", "codex"]):
        return "openai_platform"
    if any(word in text for word in ["gemini", "vertex ai", "google cloud", "google ai"]):
        return "google_gemini_cloud"
    if any(word in text for word in ["aws", "bedrock", "sagemaker", "agentcore"]):
        return "aws_bedrock"
    if any(word in text for word in ["azure ai", "azure openai", "microsoft foundry", "foundry"]):
        return "azure_ai"
    if any(word in text for word in ["cloud", "infrastructure", "gpu", "data center", "llm platform"]):
        return "cloud_llm_platforms"
    if any(word in text for word in ["regulation", "policy", "law", "safety"]):
        return "policy_and_safety"
    if any(word in text for word in ["github", "open source", "repository"]):
        return "open_source"
    if any(word in text for word in ["model", "benchmark", "eval"]):
        return "models_and_research"
    if any(word in text for word in ["agent", "workflow", "automation"]):
        return "agents_and_products"
    return "general_ai"
