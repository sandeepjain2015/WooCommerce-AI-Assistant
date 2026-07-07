from langchain.tools import tool
from datetime import datetime
from woocommerce_local.service import WooCommerceService
@tool
def get_dashboard_stats():
    products = WooCommerceService.get_products(params={"per_page": 100})
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