from langchain.tools import tool
from datetime import datetime
from woocommerce_local.service import WooCommerceService

def get_dashboard_stats():
    products = WooCommerceService.get_products(
        params={"per_page": 100}
    )
    if products.status_code != 200:
        products = []
    else:
        products = products.json()
    today = datetime.now().strftime(
        "%Y-%m-%dT00:00:00"
    )
    orders = WooCommerceService.get_orders(
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
def search_store_docs(keyword: str):
    """
    Simulates searching store documents (policies, FAQs, etc.).

    For now, returns placeholder data.
    """

    print(f">>> SEARCHING STORE DOCS: {keyword}")

    # Replace this with actual document search later
    return f"""
Search Results for "{keyword}":

- Payment Methods: We accept Visa, Mastercard, Amex, PayPal.
- Return Policy: 30-day returns for unused items.
- Shipping: Orders ship within 24 hours. Free shipping over $50.
"""

