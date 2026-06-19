from langgraph.prebuilt import create_react_agent

from config.llm import llm

from woocommerce_tools import (
    get_store_summary,
    get_top_selling_products,
    get_products_tool
)

analytics_agent = create_react_agent(
    model=llm,
    tools=[
        get_store_summary,
        get_top_selling_products,
        get_products_tool
    ],
    prompt="""
You are a WooCommerce Analytics Expert.

Responsibilities:
- Analyze store performance
- Identify top selling products
- Identify weak products
- Analyze revenue
- Give recommendations

Always provide:
1. Key Findings
2. Risks
3. Opportunities
4. Recommendations
"""
)