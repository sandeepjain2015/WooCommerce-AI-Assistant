from langgraph.graph import END
from woocommerce_tools import increase_prices_tool  # or tool version if using .invoke()

# 1. Approval Node
def approval_node(state):

    print("APPROVAL NODE EXECUTED")

    state["approval"] = "no"   # later replace with LLM decision

    return state


# 2. Execute Node
def execute_price_node(state):

    print("EXECUTE PRICE NODE EXECUTED")

    state["response"] = increase_prices_tool.invoke({ "percent": 10 })   # direct function OR tool

    return state


# 3. Router
def approval_router(state):

    print("APPROVAL ROUTER EXECUTED")

    if state["approval"] == "yes":
        return "execute"

    return END