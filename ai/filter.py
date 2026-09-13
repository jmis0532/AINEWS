def filter_items(items, keywords):
    if not keywords:
        return items

    lowered_keywords = [keyword.lower() for keyword in keywords]
    filtered = []
    for item in items:
        text = " ".join([
            item.get("title", ""),
            item.get("summary", ""),
            item.get("source", ""),
        ]).lower()
        if any(keyword in text for keyword in lowered_keywords):
            filtered.append(item)
    return filtered
