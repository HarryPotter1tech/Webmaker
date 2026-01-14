from re import A
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from docx import Document
from sentence_transformers import SentenceTransformer
import torch

KNOWLEDGEBASE_PATH = r"E:\Research Training\knowledgebase"


async def documents_init(KNOWLEDGEBASE_PATH) -> list:
    PDFLoader = DirectoryLoader(
        KNOWLEDGEBASE_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader
    )
    PDF_documents = PDFLoader.load()
    print(f"loading pdf documents from {KNOWLEDGEBASE_PATH} now...")
    print(f"loaded {len(PDF_documents)} documents successfully.")
    return PDF_documents


async def documents_split(documents) -> Document:
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=400,
        chunk_overlap=50,
        length_function=len,
    )
    PDF_document_splited = []
    for document in documents:
        PDF_document_splited.extend(text_splitter.split_text(document.page_content))
    print(
        f"the PDF_documents has been splited into {len(PDF_document_splited)} pieces successfully."
    )
    return PDF_document_splited


async def documents_vectorize(document_splited) -> list:
    device = "cpu"
    if torch.cuda.is_available():
        print("CUDA is available. Using GPU for computations.")
        device = "cuda"
    else:
        print("CUDA is not available. Using CPU for computations.")
    embedding_model = SentenceTransformer(
        r"E:\Research Training\embedding_model\jina-embeddings-v2-base-zh\jina-embeddings-v2-base-zh",
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
    return embeddings_vectors


async def vectors_retrive(vectors, vector_query: str):
    retriver = vectors.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    retrive_results = retriver.get_relevant_documents(vector_query)
    return retrive_results


# 后续要考虑实现流式输出
if __name__ == "__main__":
    pdf_documents = documents_init(KNOWLEDGEBASE_PATH)
    pdf_document_splited = documents_split(pdf_documents)
    print(pdf_document_splited[124])
    pdf_documents_embeddings = documents_vectorize(pdf_document_splited)
    print(pdf_documents_embeddings[124])
