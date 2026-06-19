from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_openai import (
    OpenAIEmbeddings,
    ChatOpenAI
)

# Load docs
documents = []

documents.extend(
    TextLoader("docs/faq.txt").load()
)

documents.extend(
    TextLoader("docs/shipping_policy.txt").load()
)

documents.extend(
    TextLoader("docs/return_policy.txt").load()
)

# Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(
    documents
)

# Embeddings
embeddings = OpenAIEmbeddings()

# Vector DB
vectorstore = FAISS.from_documents(
    docs,
    embeddings
)
vectorstore.save_local(
    "faiss_index"
)
retriever = vectorstore.as_retriever()

# User Question
question = "Can I return a used product?"

# Retrieve
results = retriever.invoke(
    question
)

context = "\n".join(
    [doc.page_content for doc in results]
)

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini"
)

prompt = f"""
Answer only from the provided context.

Context:
{context}

Question:
{question}
"""

response = llm.invoke(
    prompt
)

print("\nANSWER:\n")

print(
    response.content
)