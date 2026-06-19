import os
import re
from langchain.tools import tool
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
from woocommerce_client import wcapi
from memory.memory_manager import (
    load_memory,
    save_memory
)
from agents.router_agent import route_question
from rag.rag_chain import (
    retriever
)
import random
WC_URL = os.getenv("WC_URL")
CK = os.getenv("WC_CONSUMER_KEY")
CS = os.getenv("WC_CONSUMER_SECRET")
@tool
def get_products_tool():
    """
    Get WooCommerce products.
    """

    response = wcapi.get("products")

    if response.status_code != 200:
        return response.text

    products = response.json()

    result = []

    for p in products:

        result.append(
            f"""
ID: {p['id']}
Name: {p['name']}
Price: {p['price']}
Stock: {p['stock_status']}
"""
        )

    return "\n".join(result)
@tool
def get_orders_tool():
    """
    Get WooCommerce orders.
    """

    response = wcapi.get("orders")

    if response.status_code != 200:
        return response.text

    orders = response.json()

    result = []

    for order in orders:

        result.append(
            f"""
Order #{order['id']}
Customer: {order['billing']['first_name']}
Total: {order['total']}
Status: {order['status']}
"""
        )

    return "\n".join(result)
@tool
def get_today_orders_tool():
    """
    Get today's orders and revenue.
    """

    today = datetime.now().strftime("%Y-%m-%dT00:00:00")

    response = wcapi.get(
        "orders",
        params={
            "after": today,
            "per_page": 100
        }
    )

    if response.status_code != 200:
        return response.text

    orders = response.json()

    total_orders = len(orders)

    total_sales = sum(
        float(order["total"])
        for order in orders
    )

    return f"""
Today's Orders: {total_orders}
Today's Revenue: ${total_sales:.2f}
"""
@tool
def create_coupon_tool(percent: int):
    """
    Create a WooCommerce percentage coupon.
    """

    coupon_code = f"AI{percent}OFF{random.randint(100,999)}"

    response = wcapi.post(
        "coupons",
        {
            "code": coupon_code,
            "discount_type": "percent",
            "amount": str(percent)
        }
    )

    if response.status_code not in [200, 201]:
        return response.text

    coupon = response.json()

    return f"""
Coupon Created

Code: {coupon['code']}
Discount: {coupon['amount']}%
ID: {coupon['id']}
"""
@tool
def increase_prices_tool(percent: int):
    """
    Increase all product prices by a percentage.
    """

    response = wcapi.get("products")

    products = response.json()

    updated = 0

    for p in products:

        try:

            old_price = float(
                p["regular_price"] or p["price"]
            )

            new_price = round(
                old_price * (1 + percent / 100),
                2
            )

            wcapi.put(
                f"products/{p['id']}",
                {
                    "regular_price": str(new_price)
                }
            )

            updated += 1

        except Exception:
            pass

    return f"Updated {updated} products."
@tool
def search_product_tool(keyword: str):
    """
    Search products by keyword.
    """

    response = wcapi.get(
        "products",
        params={
            "search": keyword
        }
    )

    products = response.json()

    if not products:
        return "No products found."

    return "\n".join(
        [
            f"{p['name']} - ${p['price']}"
            for p in products
        ]
    )
@tool
def get_dashboard_stats_tool():
    """
    Get WooCommerce dashboard statistics.
    """

    products = wcapi.get(
        "products",
        params={"per_page": 100}
    ).json()

    today = datetime.now().strftime(
        "%Y-%m-%dT00:00:00"
    )

    orders = wcapi.get(
        "orders",
        params={
            "after": today,
            "per_page": 100
        }
    ).json()

    revenue = sum(
        float(o.get("total", 0))
        for o in orders
    )

    return {
        "products": len(products),
        "orders": len(orders),
        "revenue": revenue
    }
@tool
def get_low_stock_products(threshold: int = 5):
    """
    Get products with stock below threshold.
    Returns structured data.
    """

    response = wcapi.get(
        "products",
        params={"per_page": 100}
    )

    if response.status_code != 200:
        return {
            "has_low_stock": False,
            "products": [],
            "message": response.text
        }

    products = response.json()

    low_stock = []

    for p in products:

        qty = p.get("stock_quantity")

        if qty is not None and qty <= threshold:

            low_stock.append({
                "id": p["id"],
                "name": p["name"],
                "stock": qty,
                "price": p["price"]
            })

    return {
        "has_low_stock": len(low_stock) > 0,
        "count": len(low_stock),
        "products": low_stock
    }
@tool
def get_product_by_id(product_id: int):
    """
    Get product details by ID.
    """
    response = wcapi.get(f"products/{product_id}")
    return response.json()
@tool
def get_order_by_id(order_id: int):
    """
    Get order details by ID.
    """
    response = wcapi.get(f"orders/{order_id}")
    return response.json()
@tool
def get_top_selling_products():
    """
    Get top 5 selling products.
    """
    response = wcapi.get("orders", params={"per_page": 100})
    orders = response.json()
    product_counts = {}
    for order in orders:
        for item in order["line_items"]:
            product_counts[item["name"]] = product_counts.get(item["name"], 0) + item["quantity"]
    sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    return "\n".join([f"{p[0]} - {p[1]} sold" for p in sorted_products])
@tool
def get_all_coupons():
    """
    Get all coupons.
    """
    response = wcapi.get("coupons")
    coupons = response.json()
    return "\n".join([f"{c['code']} - {c['amount']}%" for c in coupons])
def get_dashboard_stats():

    products = wcapi.get(
        "products",
        params={"per_page": 100}
    ).json()

    today = datetime.now().strftime(
        "%Y-%m-%dT00:00:00"
    )

    orders = wcapi.get(
        "orders",
        params={
            "after": today,
            "per_page": 100
        }
    ).json()

    revenue = sum(
        float(o.get("total", 0))
        for o in orders
    )

    return {
        "products": len(products),
        "orders": len(orders),
        "revenue": revenue
    }
@tool
def get_dashboard_stats_new():
    """
    Get WooCommerce dashboard statistics.
    """
    stats = get_dashboard_stats()
    return {
        "products": stats["products"],
        "orders": stats["orders"],
        "revenue": stats["revenue"]
    }
@tool
def get_store_summary():
    """
    Get a high-level summary of the WooCommerce store.
    """
    print(">>> STORE SUMMARY TOOL CALLED")
    stats = get_dashboard_stats()

    return f"""
Store Summary

Products: {stats['products']}
Orders Today: {stats['orders']}
Revenue Today: ${stats['revenue']:.2f}
"""
@tool
def get_memory():
    """
    Get previous user interactions.
    """

    memory = load_memory()

    if not memory:
        return "No memory found."

    return "\n".join(memory)
@tool
def search_store_docs(question: str):
    """
    Search store policies and FAQs.
    
    """

    route = route_question(question)

    print("ROUTE =", route)

    if route == "return":
        docs = retriever.invoke(question)

    elif route == "shipping":
        docs = retriever.invoke(question)

    else:
        docs = retriever.invoke(question)

    return "\n\n".join(
        [doc.page_content for doc in docs]
    )