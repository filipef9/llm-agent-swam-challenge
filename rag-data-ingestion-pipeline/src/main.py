from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


def main():
    KB_URLS = [
        "https://www.infinitepay.io",
        "https://www.infinitepay.io/maquininha",
        "https://www.infinitepay.io/maquininha-celular",
        "https://www.infinitepay.io/tap-to-pay",
        "https://www.infinitepay.io/pdv",
        "https://www.infinitepay.io/receba-na-hora",
        "https://www.infinitepay.io/gestao-de-cobranca-2",
        "https://www.infinitepay.io/gestao-de-cobranca",
        "https://www.infinitepay.io/link-de-pagamento",
        "https://www.infinitepay.io/loja-online",
        "https://www.infinitepay.io/boleto",
        "https://www.infinitepay.io/conta-digital",
        "https://www.infinitepay.io/conta-pj",
        "https://www.infinitepay.io/pix",
        "https://www.infinitepay.io/pix-parcelado",
        "https://www.infinitepay.io/emprestimo",
        "https://www.infinitepay.io/cartao",
        "https://www.infinitepay.io/rendimento",
    ]
    EMBED_MODEL_ID = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    EXPORT_TYPE = ExportType.MARKDOWN
    COLLECTION_NAME = "infinitepay_kb"

    loader = DoclingLoader(file_path=KB_URLS, export_type=EXPORT_TYPE)

    documents = loader.load()

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header_1"),
            ("##", "Header_2"),
            ("###", "Header_3"),
        ],
        strip_headers=False,
    )

    splits = [
        split for doc in documents for split in splitter.split_text(doc.page_content)
    ]

    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_ID)

    # client = QdrantClient(":memory:")
    client = QdrantClient(url="localhost", port=6333, timeout=60)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )

    vector_store = QdrantVectorStore(
        client=client, collection_name=COLLECTION_NAME, embedding=embedding
    )

    vector_store.add_documents(documents=splits)


if __name__ == "__main__":
    main()
