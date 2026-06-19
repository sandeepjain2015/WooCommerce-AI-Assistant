from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

faq_docs = TextLoader(
    "docs/faq.txt"
).load()

shipping_docs = TextLoader(
    "docs/shipping_policy.txt"
).load()

return_docs = TextLoader(
    "docs/return_policy.txt"
).load()
for doc in faq_docs:
    doc.metadata["source"] = "faq"

for doc in shipping_docs:
    doc.metadata["source"] = "shipping"

for doc in return_docs:
    doc.metadata["source"] = "return"
documents = []

documents.extend(faq_docs)
documents.extend(shipping_docs)
documents.extend(return_docs)
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