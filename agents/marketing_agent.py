from config.llm import llm
from langgraph.prebuilt import create_react_agent

def marketing_node(state):

    print("MARKETING NODE EXECUTED")

    prompt = f"""
Store Summary:
{state["summary"]}

Top Products:
{state["top_products"]}

Low Stock:
{state["low_stock"]}

Create:

1. Coupon Idea
2. Bundle Idea
3. Email Campaign
4. Facebook Ad Idea
"""

    result = llm.invoke(prompt)

    state["marketing"] = result.content

    return state

marketing_agent = create_react_agent(
    model=llm,
    tools=[],
    prompt="""
You are a WooCommerce Marketing Expert.

Generate:
- Coupon ideas
- Bundle ideas
- Email campaigns
- Facebook ad ideas
"""
)