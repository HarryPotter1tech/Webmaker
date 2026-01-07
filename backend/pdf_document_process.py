from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from docx import Document
from typing import List
from langchain.embeddings.base import Embeddings
from openai import embeddings

KNOWLEDGEBASE_PATH = r"E:\Research Training\knowledgebase"


def retrive_init():
    PDFLoader = DirectoryLoader(
        KNOWLEDGEBASE_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader
    )
    PDF_documents = PDFLoader.load()
    print(f"loading pdf documents from{KNOWLEDGEBASE_PATH} now...")
    print(f"loaded {len(PDF_documents)} documents successfully.")
    return PDF_documents


def retrive_split(documents) -> Document:
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=6000,
        chunk_overlap=1000,
        length_function=len,
    )
    PDF_document_splited = []
    for document in documents:
        PDF_document_splited.extend(text_splitter.split_text(document.page_content))
    print(
        f"the PDF_documents has been splited into {len(PDF_document_splited)} pieces successfully."
    )
    return PDF_document_splited

def documents_vectorize(document_splited)->list:
    embedding_model=

# 后续要考虑实现流式输出
if __name__ == "__main__":
    pdf_documents = retrive_init()
    pdf_document_splited = retrive_split(pdf_documents)
    print(pdf_document_splited[124])
