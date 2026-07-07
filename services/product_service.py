from langchain.tools import tool

from woocommerce_local.service import WooCommerceService


@tool
def get_products_tool():
    """
    Get WooCommerce products.
    """

    products = WooCommerceService.get_products().json()

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
def search_product_tool(keyword: str):
    """
    Search products by keyword.
    """

    products = WooCommerceService.search_products(keyword)

    if not products:
        return "No products found."

    return "\n".join(
        f"{p['name']} - ${p['price']}"
        for p in products
    )


@tool
def get_product_by_id(product_id: int):
    """
    Get product details by ID.
    """

    return WooCommerceService.get_product(product_id)
@tool
def get_top_selling_products():
    """
    Get top 5 selling products.
    """
    response =  WooCommerceService.get_orders(params={"per_page": 100})
    orders = response.json()
    product_counts = {}
    for order in orders:
        for item in order["line_items"]:
            product_counts[item["name"]] = product_counts.get(item["name"], 0) + item["quantity"]
    sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    return "\n".join([f"{p[0]} - {p[1]} sold" for p in sorted_products])
@tool
def increase_prices_tool(percent: int):
    """
    Increase all product prices by a percentage.
    """

    response = WooCommerceService.get_products()

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

            WooCommerceService.put(
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
def get_low_stock_products(threshold: int = 5):
    """
    Get products with stock below threshold.
    Returns structured data.
    """
    response = WooCommerceService.get_products(params={"per_page": 100})
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
