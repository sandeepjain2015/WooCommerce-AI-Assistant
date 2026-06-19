from config.llm import llm

def reflection_node(state):

    print("REFLECTION NODE EXECUTED")

    prompt = f"""
Review this business analysis.

Analysis:
{state["insights"]}

Answer:

1. What important thing is missing?
2. What recommendation should be improved?
3. Give one extra recommendation.
"""

    result = llm.invoke(prompt)

    state["reflection"] = result.content

    return state