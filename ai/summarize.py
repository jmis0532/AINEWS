def summarize_items(items):
    if not items:
        return "No relevant AI intelligence items were found today."

    categories = {}
    for item in items:
        categories[item.get("category", "general_ai")] = categories.get(item.get("category", "general_ai"), 0) + 1

    category_text = ", ".join(f"{name}: {count}" for name, count in sorted(categories.items()))
    return f"Found {len(items)} relevant AI intelligence items. Category mix: {category_text}."
