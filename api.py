from agents import router_agent
from fastapi import FastAPI
from agents.router_node import get_route
from agents.support_agent import support_agent
from agents.marketing_agent import marketing_node
from agents.analytics_node import analytics_node
from database.database import Base
from database.database import engine
import models.user
import models.store
from routes.auth_routes import router as auth_router
import models.user
from woocommerce_tools import (
    get_store_summary,
    get_top_selling_products,
    get_low_stock_products
)
from routes.test_routes import router as test_router
Base.metadata.create_all(bind=engine)
from graphs.store_graph import health_graph    
app = FastAPI()
app.include_router(test_router)
app.include_router(auth_router)
@app.get("/")
def home():

    return {
        "message": "WooCommerce AI Assistant API"
    }




@app.post("/chat")
def chat(message: str):
    history = []
    route = get_route(message)
    if route == "support":

            result = support_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            message
                        )
                    ]
                }
            )

            answer = result["messages"][-1].content

    elif route == "summary":

        answer = get_store_summary.invoke({})
    elif route == "marketing":

        state = {
            "summary": get_store_summary.invoke({}),
            "top_products": get_top_selling_products.invoke({}),
            "low_stock": get_low_stock_products.invoke({})
        }

        result = marketing_node(state)

        answer = result["marketing"]
    elif route == "analytics":

        state = {}

        result = analytics_node(state)

        answer = result["analytics"]
    else:

        result = health_graph.invoke(
            {
                "user_input": message,
                "memory": []
            }
        )
        answer = result["ceo_report"]
    return {
        "route": route,
        "answer": answer
    }
 
Base.metadata.create_all(
	bind=engine
)
