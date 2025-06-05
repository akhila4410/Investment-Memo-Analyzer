from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

def build_qa_chain(text, llm):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma.from_documents(documents, embeddings)
    retriever = db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain

def hybrid_answer(query, qa_chain, llm):
    rag_result = qa_chain.invoke({"query": query})
    answer = rag_result["result"]
    sources = rag_result.get("source_documents", [])

    needs_fallback = (
        not sources or
        len(answer.strip()) < 20 or
        "i don't know" in answer.lower() or
        "i'm not sure" in answer.lower()
    )

    if needs_fallback:
        fallback_prompt = f"Answer this question clearly and conversationally:\n\n{query}"
        answer = llm.invoke(fallback_prompt)
        return "🌐 Answer (from Groq LLM):", answer
    else:
        return "📄 Answer (from PDF):", answer