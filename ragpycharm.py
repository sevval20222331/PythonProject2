from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

local_path = [
     'veriler/lc10.pdf',
     'veriler/lc11.pdf',
     'veriler/lc12.pdf',
]

all_data = []
for path in local_path:
    loader = PyMuPDFLoader(file_path=path)
    data = loader.load()
    all_data.extend(data)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(all_data)

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="local-rag"
)

llm = OllamaLLM(model=('qwen2.5:1.5b'), temperature=0.3)

RAG_PROMPT = PromptTemplate(

    input_variables=["context", "question"],
    template="""You are a helpful assistant. Use the following pieces of retrieved context to answer the user's question.
If you don't know the answer or if it's not in the context, just say that you don't know. Do not make up information.

Context:
{context}

Question:
{question}

Answer:"""
)

retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10}
)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)

response = chain.invoke(input('\nQuestion: '))
print('\nAnswer:', response)

