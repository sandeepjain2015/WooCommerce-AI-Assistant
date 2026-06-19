from langgraph.prebuilt import create_react_agent

from config.llm import llm

from woocommerce_tools import (
    search_store_docs,
    get_store_summary,
    get_all_coupons,
    get_products_tool
)

tools = [
    search_store_docs,
    get_store_summary,
    get_all_coupons,
    get_products_tool
]

support_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
You are a WooCommerce customer support assistant.

Rules:
- Use search_store_docs for policies, shipping and FAQ questions.
- Use get_coupons for discount questions.
- Use get_products for product questions.
- Use store_summary_tool only when user asks about store performance.
- Answer clearly and professionally.
"""
)