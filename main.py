from email import message
import re
from langgraph.checkpoint.memory import MemorySaver
from pprint import pprint
import gradio as gr
from config.llm import llm
from graphs.store_graph import health_graph
from graphs.action_graph import action_graph
from state.default_state import get_initial_state

from langgraph.prebuilt import create_react_agent
from agents.support_agent import support_agent
from agents.marketing_agent import marketing_node
from agents.router_node import get_route
from agents.analytics_node import analytics_node
from woocommerce_tools import (
    get_products_tool,
    get_orders_tool,
    get_today_orders_tool,
    create_coupon_tool,
    increase_prices_tool,
    search_product_tool,
    get_low_stock_products,
    get_product_by_id,
    get_order_by_id,
    get_top_selling_products,
    get_all_coupons,
    get_store_summary,
    get_memory,
    search_store_docs,
    get_dashboard_stats_new
)
tools = [
    get_products_tool,
    get_orders_tool,
    get_today_orders_tool,
    create_coupon_tool,
    increase_prices_tool,
    search_product_tool,
    get_low_stock_products,
    get_product_by_id,
    get_order_by_id,
    get_top_selling_products,
    get_all_coupons,
    get_store_summary,
    get_memory,
    search_store_docs,
    get_dashboard_stats_new
]

memory = MemorySaver()
chat_memory = []
result = action_graph.invoke(
    {
        "user_input": "Increase prices",
        "approval": "",
        "response": ""
    }
)





CUSTOM_CSS = """
body {
    background:#0f172a;
}

.gradio-container {
    background:#0f172a;
}

.sidebar {
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    min-height:700px;
}

.card {
    background:#1e293b;
    border-radius:15px;
    padding:20px;
    text-align:center;
    color:white;
    box-shadow:0px 4px 12px rgba(0,0,0,.3);
}

.card h1{
    font-size:32px;
    margin:0;
}

.card h3{
    color:#94a3b8;
    margin-bottom:10px;
}

.chatbot {
    border-radius:15px;
}

footer {
    display:none;
}
.kpi-card {
    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    border-radius: 20px;

    padding: 20px;

    color: white;

    text-align: center;

    box-shadow:
        0 8px 20px rgba(99,102,241,0.3);

    transition: all 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-5px);

    box-shadow:
        0 12px 25px rgba(99,102,241,0.5);
}

.kpi-title {
    font-size: 14px;
    opacity: 0.9;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 32px;
    font-weight: bold;
}
"""

def refresh_dashboard():

    stats = get_dashboard_stats_new.invoke({})

    orders_card = f"""
    <div class='kpi-card'>
        <div class='kpi-title'>
            📦 Orders Today
        </div>

        <div class='kpi-value'>
            {stats['orders']}
        </div>
    </div>
    """

    revenue_card = f"""
    <div class='kpi-card'>
        <div class='kpi-title'>
            💰 Revenue
        </div>

        <div class='kpi-value'>
            ${stats['revenue']}
        </div>
    </div>
    """

    products_card = f"""
    <div class='kpi-card'>
        <div class='kpi-title'>
            🛒 Products
        </div>

        <div class='kpi-value'>
            {stats['products']}
        </div>
    </div>
    """

    return orders_card, revenue_card, products_card
stats = get_dashboard_stats_new.invoke({})

orders_card = f"""
<div class='kpi-card'
style='background:linear-gradient(135deg,#3b82f6,#2563eb);'>
    <div class='kpi-title'>📦 Orders</div>
    <div class='kpi-value'>{stats["orders"]}</div>
</div>
"""

revenue_card = f"""
<div class='kpi-card'
style='background:linear-gradient(135deg,#10b981,#059669);'>
    <div class='kpi-title'>💰 Revenue</div>
    <div class='kpi-value'>${stats["revenue"]}</div>
</div>
"""

products_card = f"""
<div class='kpi-card'
style='background:linear-gradient(135deg,#f59e0b,#d97706);'>
    <div class='kpi-title'>🛒 Products</div>
    <div class='kpi-value'>{stats["products"]}</div>
</div>
"""

def respond(message, history):

    route = get_route(message)
    global chat_memory
    chat_memory.append(
        {
            "role": "user",
            "content": message
        }
    )
    print("ROUTE =", route)

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
    
    elif route == "inventory":

        low_stock = get_low_stock_products.invoke({})

        products = low_stock["products"]

        if not products:
            answer = "No products are currently low or out of stock."

        else:

            lines = []

            for p in products:

                if p["stock"] == 0:
                    status = "Out of Stock"
                else:
                    status = f"Low Stock ({p['stock']} left)"

                lines.append(
                    f"{p['name']} - {status}"
                )

            answer = "\n".join(lines)

    elif route == "general":
        memory_text = "\n".join(
            [
                f"{item['role']}: {item['content']}"
                for item in chat_memory[-10:]
            ]
        )

        result = llm.invoke(
            f"""
You are a helpful assistant.

Conversation History:
{memory_text}

Current Question:
{message}

Answer naturally using the conversation history when relevant.
"""
        )
        answer = result.content
    else:

        result = health_graph.invoke(
            {
                "user_input": message,
                "memory": chat_memory
            }
        )

        answer = result["ceo_report"]

    history.append(
        {
            "role": "user",
            "content": message
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return history, ""

with gr.Blocks(css=CUSTOM_CSS) as demo:

    gr.HTML("""
<div style="
background:linear-gradient(90deg,#4f46e5,#7c3aed);
padding:20px;
border-radius:15px;
margin-bottom:20px;
">
<h1 style="color:white">
🛒 WooCommerce AI Assistant
</h1>
<p style="color:#ddd">
AI-powered Store Manager + Customer Support
</p>
</div>
""")

    with gr.Row():

        # Sidebar
        with gr.Column(scale=1):

            gr.HTML("""
<div class='sidebar'>
<h2 style='color:white'>Navigation</h2>

<hr>

<p style='color:white'>📊 Dashboard</p>
<p style='color:white'>📦 Products</p>
<p style='color:white'>📑 Orders</p>
<p style='color:white'>🎟 Coupons</p>
<p style='color:white'>📞 Support</p>
<p style='color:white'>📈 Analytics</p>

</div>
""")

        # Main
        with gr.Column(scale=4):

            with gr.Row():

                orders_card = gr.HTML()

                revenue_card = gr.HTML()

                products_card = gr.HTML()

            refresh_btn = gr.Button(
                "🔄 Refresh Dashboard"
            )

            chatbot = gr.Chatbot(
                
                height=500,
                label="WooCommerce Assistant"
            )

            with gr.Row():

                msg = gr.Textbox(
                    placeholder="Ask about products, orders, coupons, revenue...",
                    container=False
                )

                send_btn = gr.Button(
                    "Send",
                    variant="primary"
                )

            refresh_btn.click(
                refresh_dashboard,
                outputs=[
                    orders_card,
                    revenue_card,
                    products_card
                ]
            )

            msg.submit(
                respond,
                [msg, chatbot],
                [chatbot, msg]
            )

            send_btn.click(
                respond,
                [msg, chatbot],
                [chatbot, msg]
            )

    demo.load(
        refresh_dashboard,
        outputs=[
            orders_card,
            revenue_card,
            products_card
        ]
    )

demo.launch(
    css=CUSTOM_CSS,
    server_port=7860
) 