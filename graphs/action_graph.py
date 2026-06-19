from langgraph.graph import StateGraph, END
from state.store_state import StoreState

from agents.action_agent import (
    approval_node,
    execute_price_node,
    approval_router
)

action_graph = StateGraph(StoreState)

action_graph.add_node("approval", approval_node)
action_graph.add_node("execute", execute_price_node)

action_graph.set_entry_point("approval")

action_graph.add_conditional_edges(
    "approval",
    approval_router
)

action_graph.add_edge("execute", END)

action_graph = action_graph.compile()