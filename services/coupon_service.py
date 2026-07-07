from langchain.tools import tool
import random
from woocommerce_local.service import WooCommerceService

@tool
def create_coupon_tool(percent: int):
    """
    Create a WooCommerce percentage coupon.
    """
    
    coupon_code = f"AI{percent}OFF{random.randint(100,999)}"

    response = WooCommerceService.post(
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
def get_all_coupons():
    """
    Get all coupons.
    """
    
    response = WooCommerceService.get_coupons()
    coupons = response.json()
    return "\n".join([f"{c['code']} - {c['amount']}%" for c in coupons])
