from langchain.tools import tool

from woocommerce_local.service import WooCommerceService


@tool
def get_orders_tool():
    """
    Get WooCommerce orders.
    """

    orders = WooCommerceService.get_orders()

    result = []

    for order in orders:

        result.append(
            f"""
Order #{order['id']}
Customer: {order['billing']['first_name']} {order['billing']['last_name']}
Total: ${order['total']}
Status: {order['status']}
"""
        )

    return "\n".join(result)


@tool
def get_order_by_id(order_id: int):
    """
    Get order details by ID.
    """

    return WooCommerceService.get_order(order_id)
@tool
def get_today_orders_tool():
    """
    Get today's orders and revenue.
    """

    today = datetime.now().strftime("%Y-%m-%dT00:00:00")
    response = WooCommerceService.get_orders(
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