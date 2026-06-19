from langchain_core.prompts import ChatPromptTemplate
from config.llm import llm

prompt = ChatPromptTemplate.from_template("""
You are a router.

Question:
{question}

Choose ONLY one:

- faq
- shipping
- return

Answer with one word only.
""")

router_chain = prompt | llm


def route_question(question):
    result = router_chain.invoke(
        {
            "question": question
        }
    )

    return result.content.strip().lower()
