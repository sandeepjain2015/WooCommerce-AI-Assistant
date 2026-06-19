from config.llm import llm
from woocommerce_tools import (
    get_store_summary,
    get_top_selling_products,
    get_low_stock_products
)

def summary_node(state):

    summary = get_store_summary.invoke({})

    state["summary"] = summary

    return state
def top_products_node(state):

    top_products = (
        get_top_selling_products.invoke({})
    )

    state["top_products"] = top_products

    return state
def low_stock_node(state):
    print("LOW STOCK NODE EXECUTED")
    low_stock = (
        get_low_stock_products.invoke({})
    )

    state["low_stock"] = low_stock

    return state
def risk_node(state):

    print("RISK NODE EXECUTED")

    products = state["low_stock"]["products"]

    prompt = f"""
Analyze inventory risks.

Low stock products:

{products}
"""

    result = llm.invoke(prompt)

    state["risks"] = result.content

    return state
  
def stock_router(state):
    print("STOCK ROUTER EXECUTED")

    low_stock = state["low_stock"]
    print("LOW STOCK ==========================",low_stock)

    if state["low_stock"]["has_low_stock"]:
        return "risk"

    return "insights"