from agents.support_agent import support_agent
from context.request_context import (
    set_current_user,
    set_db,
    clear_context
)

from agents.router_node import get_route

from agents.analytics_node import analytics_node
from agents.marketing_agent import marketing_node

from graphs.store_graph import health_graph
from services.store_service import get_store_summary
from services.product_service import (
    get_products_tool,
    get_top_selling_products,
    get_low_stock_products
)
from config.llm import llm


class ChatService:

    @staticmethod
    def chat(
        message,
        current_user,
        db
    ):

        set_current_user(current_user)
        set_db(db)

        try:

            route = get_route(message)

            print("ROUTE =", route)

            if route == "summary":

                return get_store_summary.invoke({})
            elif route == "support":

                result = support_agent.invoke({
                    "messages": [
                        (
                            "user",
                            message
                        )
                    ]
                })

                return result["messages"][-1].content
            elif route == "marketing":

                state = {

                    "summary": get_store_summary.invoke({}),

                    "top_products": get_top_selling_products.invoke({}),

                    "low_stock": get_low_stock_products.invoke({})
                }

                result = marketing_node(state)

                return result["marketing"]

            elif route == "analytics":

                result = analytics_node({})

                return result["analytics"]
            elif route == "products":

                return get_products_tool.invoke({})

            elif route == "general":

                return llm.invoke(message).content

            else:

                result = health_graph.invoke({

                    "user_input": message,

                    "memory": []

                })

                return result["ceo_report"]

        finally:

            clear_context()
