from langgraph.graph import (
    StateGraph,
    END
)

from state.store_state import StoreState

from agents.router_node import router_node

from agents.business_agent import insights_node
from agents.reflection_agent import reflection_node
from agents.marketing_agent import marketing_node
from agents.ceo_agent import ceo_node

from agents.analytics_node import analytics_node

from graphs.router import route_decision


builder = StateGraph(StoreState)

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "business",
    insights_node
)

builder.add_node(
    "reflection",
    reflection_node
)

builder.add_node(
    "marketing",
    marketing_node
)

builder.add_node(
    "ceo",
    ceo_node
)

builder.add_node(
    "analytics",
    analytics_node
)

builder.set_entry_point(
    "router"
)

builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "analytics": "analytics",
        "marketing": "business",
        "ceo": "business"
    }
)

builder.add_edge(
    "business",
    "reflection"
)

builder.add_edge(
    "reflection",
    "marketing"
)

builder.add_edge(
    "marketing",
    "ceo"
)

builder.add_edge(
    "analytics",
    END
)

builder.add_edge(
    "ceo",
    END
)

intelligent_graph = builder.compile()