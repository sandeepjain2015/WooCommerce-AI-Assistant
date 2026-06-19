from langgraph.graph import (
    StateGraph,
    END
)

from state.store_state import StoreState

from agents.support_agent import (
    support_node
)

builder = StateGraph(
    StoreState
)

builder.add_node(
    "support",
    support_node
)

builder.set_entry_point(
    "support"
)

builder.add_edge(
    "support",
    END
)

customer_support_graph = builder.compile()