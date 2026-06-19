from config.llm import llm
def insights_node(state):
    print("INSIGHTS NODE EXECUTED")
    prompt = f"""
You are a WooCommerce business analyst.

Store Summary:
{state['summary']}

Top Products:
{state['top_products']}

Low Stock:
{state['low_stock']}

Generate:

1. Key Findings

2. Risks

3. Opportunities

4. Recommendations
"""

    result = llm.invoke(prompt)

    state["insights"] = result.content

    return state