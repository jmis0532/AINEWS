import os

from openai import OpenAI


def _fallback_summary(items):
    if not items:
        return "今天沒有找到符合條件的 AI 情報。"

    categories = {}
    for item in items:
        category = item.get("category", "general_ai")
        categories[category] = categories.get(category, 0) + 1

    category_text = "、".join(
        f"{name.replace('_', ' ')}：{count} 則" for name, count in sorted(categories.items())
    )
    return f"今天找到 {len(items)} 則相關 AI 情報。分類分布為：{category_text}。"


def _format_items_for_prompt(items):
    blocks = []
    for index, item in enumerate(items, start=1):
        blocks.append(
            "\n".join([
                f"{index}. 標題：{item.get('title', 'Untitled')}",
                f"來源：{item.get('source', '')}",
                f"分類：{item.get('category', 'general_ai')}",
                f"發布時間：{item.get('published', '')}",
                f"連結：{item.get('url', '')}",
                f"原始摘要：{item.get('summary', '').strip()}",
            ])
        )
    return "\n\n".join(blocks)


def summarize_items(items, prompt=None):
    if not items:
        return "今天沒有找到符合條件的 AI 情報。"

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_summary(items)

    client = OpenAI(api_key=api_key)
    system_prompt = prompt or (
        "你是 AI 情報分析助理。請用繁體中文整理每日 AI 情報，語氣清楚、務實，避免誇大。"
    )
    user_prompt = f"""
請根據以下資料，產生一份繁體中文摘要。請包含：

1. 今日重點：3 到 5 個重點條列
2. 重要程度：用高 / 中 / 低標示整體重要性，並說明原因
3. 值得關注原因：說明這些消息對產品、研究、開發者或產業可能代表什麼
4. 建議追蹤：列出最值得點開閱讀的 3 則來源標題

資料如下：
{_format_items_for_prompt(items)}
"""

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"),
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.output_text.strip()
    except Exception as exc:
        return _fallback_summary(items) + f"\n\nAI 摘要暫時無法產生：{exc}"
