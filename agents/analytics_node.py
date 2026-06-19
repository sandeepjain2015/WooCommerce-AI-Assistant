from config.llm import llm

from woocommerce_tools import (
    get_store_summary,
    get_top_selling_products,
    get_low_stock_products
)


def analytics_node(state):

    print("ANALYTICS NODE EXECUTED")

    summary = get_store_summary.invoke({})

    products = get_top_selling_products.invoke({})

    low_stock = get_low_stock_products.invoke({})

    prompt = f"""
You are a WooCommerce business analyst.

Store Summary:
{summary}

Top Products:
{products}

Low Stock:
{low_stock}

Generate:

1. Revenue Analysis
2. Key Findings
3. Risks
4. Opportunities
5. Recommendations

Keep it concise and business-focused.
"""

    result = llm.invoke(prompt)

    state["analytics"] = result.content

    return state