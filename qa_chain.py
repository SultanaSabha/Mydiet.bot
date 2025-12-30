from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM # Import for the local LLM

# Use the same FREE embedding model
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load your existing vector database
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# Initialize the LOCAL LLM from Ollama
llm = OllamaLLM(model="llama3") # <-- Use the model you downloaded

# Create prompt template
prompt_template = """You are a helpful and friendly AI nutritionist named MyDiet.Bot. 
Use the following pieces of context to answer the user's question. 
If the answer is not in the context, say so. Don't make up an answer.

Context: {context}

Question: {question}
Helpful Answer:"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Create the QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,  # Now we have a valid LLM!
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

def get_qa_chain():
    return qa_chain

if __name__ == "__main__":
    chain = get_qa_chain()
    test_result = chain.invoke({"query": "What are good sources of protein?"})
    print("Answer:", test_result['result'])