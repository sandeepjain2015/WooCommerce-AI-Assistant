from langgraph.prebuilt import create_react_agent
from langchain.tools import tool

from config.llm import llm

from agents.support_agent import support_agent
from agents.marketing_agent import marketing_agent
from agents.ceo_agent import ceo_agent
from agents.analytics_agent import analytics_agent


@tool
def support_tool(question: str):
    """
    Handle customer support questions.
    """

    print("SUPPORT AGENT SELECTED")

    result = support_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ]
        }
    )

    return result["messages"][-1].content


@tool
def marketing_tool(question: str):
    """
    Handle marketing questions.
    """

    print("MARKETING AGENT SELECTED")

    result = marketing_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ]
        }
    )

    return result["messages"][-1].content


@tool
def ceo_tool(question: str):
    """
    Handle CEO and strategy questions.
    """

    print("CEO AGENT SELECTED")

    result = ceo_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ]
        }
    )

    return result["messages"][-1].content


@tool
def analytics_tool(question: str):
    """
    Handle analytics and reporting questions.
    """

    print("ANALYTICS AGENT SELECTED")

    result = analytics_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ]
        }
    )

    return result["messages"][-1].content


supervisor_agent = create_react_agent(
    model=llm,
    tools=[
        support_tool,
        marketing_tool,
        ceo_tool,
        analytics_tool
    ],
    prompt="""
You are a Supervisor Agent.

Your job is to select the correct specialist agent.

Use:

support_tool:
- shipping questions
- return policy
- FAQs
- customer support
- coupons
- discounts

marketing_tool:
- marketing ideas
- campaigns
- promotions
- increase sales
- email marketing

ceo_tool:
- business strategy
- growth plan
- risks
- action plan
- business recommendations

analytics_tool:
- revenue analysis
- sales reports
- top selling products
- store performance
- analytics

Always delegate to exactly one tool.
"""
)