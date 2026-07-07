from woocommerce_local.service import WooCommerceService
from langchain.tools import tool
from woocommerce_client import get_wcapi
from datetime import datetime
from woocommerce_local.service import WooCommerceService
from services.dashboard_service import get_dashboard_stats
@tool
def get_today_orders_tool():
    """
    Get today's orders and revenue.
    """
    today = datetime.now().strftime("%Y-%m-%dT00:00:00")
    response =  WooCommerceService.get_orders(params={
            "after": today,
            "per_page": 100
        })
    

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
def get_dashboard_stats_tool():
    """
    Get WooCommerce dashboard statistics.
    """
    
    
    products = WooCommerceService.get_products(params={"per_page": 100}).json()

    today = datetime.now().strftime(
        "%Y-%m-%dT00:00:00"
    )

    orders = WooCommerceService.get_orders(params={
            "after": today,
            "per_page": 100
        }).json()

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
def get_top_selling_products():
    """
    Get top 5 selling products.
    """
    
    response = WooCommerceService.get_orders(
        params={
            "per_page": 100
        }
    )
    orders = response.json()
    product_counts = {}
    for order in orders:
        for item in order["line_items"]:
            product_counts[item["name"]] = product_counts.get(item["name"], 0) + item["quantity"]
    sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    return "\n".join([f"{p[0]} - {p[1]} sold" for p in sorted_products])
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
