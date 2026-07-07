# agents/router_node.py

from config.llm import llm

print("LLM ID:", id(llm))
def get_route(question):

    prompt = f"""
You are an intelligent WooCommerce router.

Question:
{question}

Routes:

support:
Customer support questions about the store including:

- return policy
- shipping policy
- refund policy
- exchange policy
- payment methods
- account creation
- login
- registration
- guest checkout
- order tracking
- delivery
- FAQs
- store policies
- customer account
- placing orders
- canceling orders
- coupons
- discounts

Any question about store policies, customer help, FAQs,
or shopping experience should ALWAYS be routed to support.

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

products:
- what products do you sell
- show products
- product catalog
- available products
- list products
- product information

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
