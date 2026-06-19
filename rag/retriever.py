from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv

load_dotenv()
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_openai import (
    OpenAIEmbeddings
)

# Load documents
documents = []

documents.extend(
    TextLoader(
        "docs/faq.txt"
    ).load()
)

documents.extend(
    TextLoader(
        "docs/shipping_policy.txt"
    ).load()
)

documents.extend(
    TextLoader(
        "docs/return_policy.txt"
    ).load()
)

# Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(
    documents
)

print(
    f"Loaded {len(docs)} chunks"
)

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create vector database
vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

# Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1}
)

# Test query
results = retriever.invoke(
    "What is your return policy?"
)

print("\nRESULTS:\n")

for result in results:

    print(
        result.page_content
    )

    print(
        "\n-------------------\n"
    )