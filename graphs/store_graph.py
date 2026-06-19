from langgraph.graph import StateGraph, END

from state.store_state import StoreState
from agents.memory_agent import (
    memory_node
)
from agents.reflection_agent import (
    reflection_node
)
from agents.marketing_agent import (
    marketing_node
)
from agents.ceo_agent import (
    ceo_node
)
from agents.inventory_agent import (
    summary_node,
    top_products_node,
    low_stock_node,
    risk_node,
    stock_router
)
from agents.business_agent import (
    insights_node
)
health_graph = StateGraph(
    StoreState
)
health_graph.add_node(
    "memory",
    memory_node
)

health_graph.set_entry_point(
    "memory"
)

health_graph.add_edge(
    "memory",
    "summary"
)
health_graph.add_node(
    "summary",
    summary_node
)

health_graph.add_node(
    "top_products",
    top_products_node
)

health_graph.add_node(
    "low_stock",
    low_stock_node
)
health_graph.add_node(
    "reflection",
    reflection_node
)
health_graph.add_node(
    "insights",
    insights_node
)
health_graph.add_node(
    "risk",
    risk_node
)
health_graph.add_node(
    "marketing",
    marketing_node
)
health_graph.add_node(
    "ceo",
    ceo_node
)
health_graph.add_edge(
    "summary",
    "top_products"
)

health_graph.add_edge(
    "top_products",
    "low_stock"
)

health_graph.add_conditional_edges(
    "low_stock",
    stock_router
)
health_graph.add_edge(
    "risk",
    "insights"
)

health_graph.add_edge(
    "insights",
    "reflection"
)



health_graph.add_edge(
    "reflection",
    "marketing"
)

health_graph.add_edge(
    "marketing",
    "ceo"
)

health_graph.add_edge(
    "ceo",
    END
)
health_graph = health_graph.compile()