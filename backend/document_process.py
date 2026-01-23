import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from docx import Document
from numpy import ndarray
from sentence_transformers import SentenceTransformer
import torch
import faiss
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(current_dir, ".env"))
KNOWLEDGEBASE_PATH = os.getenv("KNOWLEDGEBASE_PATH")
MODEL_PATH = os.getenv("JINA_EMBEDDINGS_V2_BASE_ZH_PATH")
VECTOR_DIMENSION = os.getenv("JINA_EMBEDDINGS_V2_BASE_ZH_DIMENSION")
RAG_INIT_FLAG = os.getenv("RAG_INIT_FLAG")


def documents_init(KNOWLEDGEBASE_PATH) -> list:
    PDFLoader = DirectoryLoader(
        KNOWLEDGEBASE_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader
    )
    PDF_documents = PDFLoader.load()
    print(f"loading pdf documents from {KNOWLEDGEBASE_PATH} now...")
    print(f"loaded {len(PDF_documents)} documents successfully.")
    return PDF_documents


def documents_split(documents) -> Document:
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["。", ",", "\n", " ", "\n\n"],
        chunk_size=400,
        chunk_overlap=100,
        length_function=len,
    )
    PDF_document_splited = []
    for document in documents:
        PDF_document_splited.extend(text_splitter.split_text(document.page_content))
    print(
        f"the PDF_documents has been splited into {len(PDF_document_splited)} pieces successfully."
    )
    return PDF_document_splited


def documents_vectorize(document_splited) -> list:
    device = "cpu"
    if torch.cuda.is_available():
        print("CUDA is available. Using GPU for computations.")
        device = "cuda"
    else:
        print("CUDA is not available. Using CPU for computations.")
    embedding_model = SentenceTransformer(
        MODEL_PATH,
        trust_remote_code=True,
        device=device,
    )
    print(f"start to vectorize {len(document_splited)} pieces of documents now...")
    embeddings_vectors = embedding_model.encode(
        document_splited,
        batch_size=10,
        show_progress_bar=True,
        convert_to_numpy=True,
        convert_to_tensor=False,
    )
    print("documents vectorize successfully.")
    print(f"the shape of embeddings_vectors is {embeddings_vectors[123].shape}")
    return embeddings_vectors, embedding_model


def retrive_init(vectors: ndarray) -> faiss.IndexFlatL2:
    index = faiss.IndexFlatL2(int(VECTOR_DIMENSION))  # 建立索引
    index.add(vectors)  # 添加向量到索引中(这里是文档的向量)
    print(f"the total number of vectors in the index is {index.ntotal}")
    return index


def rag_init():
    pdf_documents = documents_init(KNOWLEDGEBASE_PATH)
    pdf_document_splited = documents_split(pdf_documents)
    pdf_documents_embeddings, embedding_model = documents_vectorize(
        pdf_document_splited
    )
    faiss_index = retrive_init(pdf_documents_embeddings)
    return faiss_index, embedding_model, pdf_document_splited
    # 返回所引，嵌入模型，分割后的文档，用于后续问题的检索与生成


if RAG_INIT_FLAG.lower() == "false":
    FAISS_INDEX, EMBEDDING_MODEL, DOCUMENT_SPLITED = rag_init()
    print("RAG system initialized successfully.")
    os.environ["RAG_INIT_FLAG"] = "true"
else:
    print("RAG system has been initialized already.")
