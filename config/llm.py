import os
from langchain_openai import ChatOpenAI

# Using DeepSeek's standard chat model (DeepSeek-V3)
MODEL_NAME = "deepseek-chat"

print("DEEPSEEK_API_KEY")
print(os.getenv("DEEPSEEK_API_KEY"))

llm = ChatOpenAI(
    model=MODEL_NAME,
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)
