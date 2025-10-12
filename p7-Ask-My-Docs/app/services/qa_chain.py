from __future__ import annotations

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


def build_qa_chain(llm, retriever, *, return_sources: bool = True) -> RetrievalQA:
    """
    Build a RetrievalQA chain with a custom prompt that:
    - Answers only using the provided context
    - Says “I don’t know” when the answer is not found
    """
    template = (
        "You are a helpful assistant. Answer only using the information in the provided document context.\n"
        "If the answer is not found in the context, say “I don’t know”. Be concise.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n"
        "Answer:"
    )
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=return_sources,
    )
