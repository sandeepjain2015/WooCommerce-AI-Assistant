# WooCommerce AI Assistant

## Overview

WooCommerce AI Assistant is a Multi-Agent AI system built using LangGraph, FastAPI, Gradio, RAG, and WooCommerce APIs.

The assistant can:

* Answer customer support questions
* Analyze store performance
* Generate marketing campaigns
* Provide CEO-level business recommendations
* Search store policies using RAG
* Access live WooCommerce data

---

# WooCommerce AI Assistant

Multi-Agent AI Assistant built using LangGraph, FastAPI, RAG, DeepSeek, and WooCommerce APIs.

## 🎥 Demo Video

https://www.youtube.com/watch?v=YOUR_VIDEO_ID

## Features

### Customer Support Agent

Handles:

* Return Policy
* Shipping Policy
* FAQs
* Product Questions
* Coupon Questions

Uses:

* RAG
* FAISS Vector Search
* Store Documentation

Example:

"What is your return policy?"

---

### Analytics Agent

Provides:

* Revenue Analysis
* Top Selling Products
* Inventory Analysis
* Business Insights
* Risk Identification

Example:

"Give revenue analysis"

---

### Marketing Agent

Generates:

* Coupon Ideas
* Bundle Ideas
* Email Campaigns
* Facebook Ad Ideas

Example:

"Give me marketing ideas"

---

### CEO Agent

Provides:

* Top Priorities
* Business Risks
* Growth Opportunities
* 7-Day Action Plans

Example:

"Create a 7-day action plan"

---

### Intelligent Router

Uses an LLM Router to automatically select the correct agent.

Supported Routes:

* support
* products
* coupons
* inventory
* analytics
* marketing
* ceo
* general

Example:

"What products do you sell?" → Products Agent

"Show available coupon codes" → Coupons Agent

"Create a 7-day action plan" → CEO Agent

---

### Memory Support

The assistant remembers conversation context.

Example:

User: My name is Sandeep

Assistant: Nice to meet you, Sandeep.

User: What is my name?

Assistant: Your name is Sandeep.

---

## Architecture

User

↓

Gradio UI

↓

FastAPI API

↓

LLM Router

↓

Support Agent | Analytics Agent | Marketing Agent | CEO Agent

↓

WooCommerce APIs + RAG Knowledge Base

↓

OpenAI / DeepSeek LLM

---

## Technology Stack

### AI

* LangGraph
* LangChain
* DeepSeek
* OpenAI Compatible APIs

### Backend

* FastAPI
* Python

### Frontend

* Gradio

### Vector Database

* FAISS

### E-Commerce

* WooCommerce REST API

### Deployment

* Docker (In Progress)

---

## Project Structure

```text
woocommerce_store_assistant/

├── agents/
├── graphs/
├── state/
├── config/
├── docs/
├── faiss_index/
├── api.py
├── main.py
├── woocommerce_tools.py
├── requirements.txt
└── README.md
```

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd woocommerce_store_assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a .env file:

```env
DEEPSEEK_API_KEY=your_key

WC_URL=your_store_url
WC_CONSUMER_KEY=your_key
WC_CONSUMER_SECRET=your_secret
```

### Run Gradio UI

```bash
python main.py
```

### Run FastAPI

```bash
uvicorn api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Demo Questions

### Support

* What is your return policy?
* What payment methods do you support?

### Products

* What products do you sell?
* Which products are out of stock?

### Coupons

* Show available coupon codes
* What is the best discount currently available?

### Analytics

* Give revenue analysis
* What are the biggest risks in my store?

### Marketing

* Give me marketing ideas

### CEO

* Create a 7-day action plan

---

## Future Enhancements

* AWS Bedrock Integration
* Persistent User Memory
* Advanced Inventory Agent
* Multi-Store Support
* Deployment on AWS
* Slack Integration
* WhatsApp Integration

---
## Screenshots

### Products Agent

![Products Agent](screenshots/Products%20Agent.png)

### Coupons Agent

![Coupons Agent](screenshots/Coupons%20Agent.png)

### CEO Agent

![CEO Agent](screenshots/CEO%20Agent.png)

## Author

Sandeep Jain

LinkedIn:
https://www.linkedin.com/in/sandeep-jain-wp/

Portfolio:
https://sandeepjain.in/

Hire Me:
https://sandeepjain.in/hire-me/
