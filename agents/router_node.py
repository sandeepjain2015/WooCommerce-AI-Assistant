# agents/router_node.py

from config.llm import llm


def get_route(question):

    prompt = f"""
You are an intelligent WooCommerce router.

Question:
{question}

Routes:

support:
- return policy
- shipping
- FAQ
- payment methods
- coupons
- coupon codes
- discounts
- best discount
- available offers
- promo codes
- products

summary:
- store summary
- dashboard overview

analytics:
- revenue analysis
- top products
- sales performance
- inventory analysis

inventory:
- out of stock products
- low stock products
- inventory report
- stock status
- restocking recommendations

marketing:
- marketing ideas
- campaigns
- promotions
- email marketing
- Facebook ads

ceo:
- action plan
- business strategy
- growth plan
- priorities
- business risks
- next steps
- what should I do

Return ONLY ONE WORD:

support
summary
analytics
marketing
ceo
general
"""

    result = llm.invoke(prompt)
    route = result.content.strip().lower()

    print("QUESTION =", question)
    print("ROUTE =", route)
    return route