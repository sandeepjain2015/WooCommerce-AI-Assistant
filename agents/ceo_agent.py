from config.llm import llm


def ceo_node(state):

    print("CEO NODE EXECUTED")

    prompt = f"""
You are the CEO of an e-commerce company.

Store Summary:
{state["summary"]}

Insights:
{state["insights"]}

Reflection:
{state["reflection"]}

Marketing Ideas:
{state["marketing"]}

Your job is to make decisions.

Give:

1. Top 3 Priorities
2. Urgency Level (Low / Medium / High)
3. Expected Business Impact
4. Action Plan for Next 7 Days

Keep it practical and concise.
"""

    result = llm.invoke(prompt)
    state["ceo_report"] = result.content
    state["response"] = result.content
    return state